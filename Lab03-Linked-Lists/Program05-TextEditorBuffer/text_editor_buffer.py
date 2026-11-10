"""
Program 05: Text Editor Buffer Using a Doubly Linked List
Course: IC-307D Data Structures and Algorithms Lab
Unit 3: Linked Lists (CO1)

This program models an interactive in-memory Text Editor line buffer using a
Doubly Linked List from first principles:
- Each node represents a distinct line of text with 'prev' and 'next' pointer
  references.
- Doubly linked lists are uniquely suited for text buffers:
    1. O(1) line insertion and deletion at cursor.
    2. O(1) bidirectional cursor navigation (cursor up / cursor down).
    3. No massive array-reallocation or element-shifting costs when editing lines.
- Cursor tracking:
    Maintains a direct reference to the active line node and its 1-based line number.
- Menu-driven interface and automated test suite (--test flag).
- Pure node reference implementation without using Python list as the primary buffer.
"""

import sys
from typing import List, Optional, Tuple


class TextLineNode:
    """
    Represents an individual line of text in the editor buffer.

    Attributes:
        text: The string content of the line.
        prev: Pointer to the preceding line node (or None if first line).
        next: Pointer to the succeeding line node (or None if last line).
    """

    def __init__(self, text: str) -> None:
        self.text: str = str(text)
        self.prev: Optional["TextLineNode"] = None
        self.next: Optional["TextLineNode"] = None

    def __repr__(self) -> str:
        return f"TextLineNode({self.text!r})"


class TextEditorBuffer:
    """
    Text Editor Line Buffer implemented using a Doubly Linked List.

    Indexing Convention:
        Line numbers are 1-based (standard for text editors like Vim and Nano):
        - Line 1 corresponds to head.
        - Line N corresponds to tail.
        - Valid line insertion numbers: 1 <= line_num <= line_count + 1.
        - Valid line access/deletion: 1 <= line_num <= line_count.
    """

    def __init__(self) -> None:
        self.head: Optional[TextLineNode] = None
        self.tail: Optional[TextLineNode] = None
        self.cursor: Optional[TextLineNode] = None
        self.cursor_line: int = 0
        self._line_count: int = 0

    def is_empty(self) -> bool:
        """Checks whether the buffer contains any text lines."""
        return self.head is None

    def line_count(self) -> int:
        """Returns the total number of lines in the buffer."""
        return self._line_count

    def __len__(self) -> int:
        return self._line_count

    def _get_node_at_line(self, line_num: int) -> TextLineNode:
        """
        Traverses to the node at the specified 1-based line number.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        if line_num < 1 or line_num > self._line_count:
            raise IndexError(
                f"Line number {line_num} out of range [1, {self._line_count}]."
            )

        # Optimize traversal direction from head or tail
        if line_num <= self._line_count // 2:
            current = self.head
            for _ in range(line_num - 1):
                assert current is not None
                current = current.next
        else:
            current = self.tail
            for _ in range(self._line_count - line_num):
                assert current is not None
                current = current.prev

        assert current is not None
        return current

    def insert_line(self, line_num: int, text: str) -> None:
        """
        Inserts a new line of text at the specified 1-based line position.
        Updates cursor to point to the newly inserted line.

        Time Complexity: O(n) traversal, O(1) pointer relinking.
        Auxiliary Space Complexity: O(1)
        """
        if not isinstance(line_num, int):
            raise TypeError("Line number must be an integer.")

        if line_num < 1 or line_num > self._line_count + 1:
            raise IndexError(
                f"Cannot insert at line {line_num}. Valid range is [1, {self._line_count + 1}]."
            )

        new_node = TextLineNode(text)

        # 1. Insertion into empty buffer
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        # 2. Insert at beginning (line 1)
        elif line_num == 1:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        # 3. Insert at end (line line_count + 1)
        elif line_num == self._line_count + 1:
            assert self.tail is not None
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        # 4. Insert in the middle
        else:
            target_node = self._get_node_at_line(line_num)
            prev_node = target_node.prev
            assert prev_node is not None

            new_node.next = target_node
            new_node.prev = prev_node
            prev_node.next = new_node
            target_node.prev = new_node

        self._line_count += 1
        self.cursor = new_node
        self.cursor_line = line_num

    def append_line(self, text: str) -> None:
        """Convenience method to append a line to the end of the buffer."""
        self.insert_line(self._line_count + 1, text)

    def delete_line(self, line_num: int) -> str:
        """
        Deletes the line at the specified 1-based line number.
        Adjusts cursor position to the succeeding line, or preceding line if tail was deleted.

        Returns:
            The text content of the deleted line.

        Time Complexity: O(n) traversal, O(1) pointer unlinking.
        Auxiliary Space Complexity: O(1)
        """
        if not isinstance(line_num, int):
            raise TypeError("Line number must be an integer.")

        if self.head is None:
            raise IndexError("Cannot delete from an empty buffer.")

        if line_num < 1 or line_num > self._line_count:
            raise IndexError(
                f"Line number {line_num} out of range [1, {self._line_count}]."
            )

        target = self._get_node_at_line(line_num)
        deleted_text = target.text

        # 1. Only single line in buffer
        if self.head == self.tail:
            self.head = None
            self.tail = None
            self.cursor = None
            self.cursor_line = 0
        # 2. Delete head line
        elif target == self.head:
            self.head = self.head.next
            assert self.head is not None
            self.head.prev = None
            self.cursor = self.head
            self.cursor_line = 1
        # 3. Delete tail line
        elif target == self.tail:
            self.tail = self.tail.prev
            assert self.tail is not None
            self.tail.next = None
            self.cursor = self.tail
            self.cursor_line = self._line_count - 1
        # 4. Delete middle line
        else:
            assert target.prev is not None and target.next is not None
            target.prev.next = target.next
            target.next.prev = target.prev
            self.cursor = target.next
            self.cursor_line = line_num

        self._line_count -= 1
        return deleted_text

    def edit_line(self, line_num: int, new_text: str) -> None:
        """
        Replaces the text of the line at the specified 1-based line number.
        Sets cursor to the edited line.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        if not isinstance(line_num, int):
            raise TypeError("Line number must be an integer.")

        target = self._get_node_at_line(line_num)
        target.text = str(new_text)
        self.cursor = target
        self.cursor_line = line_num

    def move_cursor_next(self) -> bool:
        """
        Advances the cursor to the next line (cursor down).

        Returns:
            True if moved, False if already at the last line or buffer empty.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.cursor is not None and self.cursor.next is not None:
            self.cursor = self.cursor.next
            self.cursor_line += 1
            return True
        return False

    def move_cursor_prev(self) -> bool:
        """
        Moves the cursor to the preceding line (cursor up).

        Returns:
            True if moved, False if already at the first line or buffer empty.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.cursor is not None and self.cursor.prev is not None:
            self.cursor = self.cursor.prev
            self.cursor_line -= 1
            return True
        return False

    def get_cursor_position(self) -> Tuple[int, Optional[str]]:
        """
        Returns (cursor_line_number, cursor_text_content).
        Line number is 0 if buffer is empty.
        """
        if self.cursor is None:
            return 0, None
        return self.cursor_line, self.cursor.text

    def to_list(self) -> List[str]:
        """Returns all lines as a list of strings (for test assertions)."""
        result: List[str] = []
        current = self.head
        while current is not None:
            result.append(current.text)
            current = current.next
        return result

    def display_buffer(self) -> None:
        """
        Prints the complete text buffer formatted with line numbers
        and a cursor pointer indicator ('>' for active cursor line).
        """
        if self.head is None:
            print("\n[Text Editor Buffer is Empty]")
            return

        print("\n" + "-" * 55)
        print(f"  TEXT BUFFER (Total Lines: {self._line_count} | Active Cursor: Line {self.cursor_line})")
        print("-" * 55)

        current = self.head
        line_idx = 1
        while current is not None:
            marker = " >" if current == self.cursor else "  "
            print(f"{marker} {line_idx:3d} | {current.text}")
            current = current.next
            line_idx += 1

        print("-" * 55)


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Executes comprehensive tests covering all TextEditorBuffer operations and edge cases."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Text Editor Buffer (Program 05)")
    print("=" * 65)

    buf = TextEditorBuffer()

    # 1. Empty buffer operations
    assert buf.is_empty() is True
    assert buf.line_count() == 0
    assert buf.get_cursor_position() == (0, None)
    assert buf.move_cursor_next() is False
    assert buf.move_cursor_prev() is False
    print("  [Test 01 Passed] Initialized empty buffer verified.")

    # Boundary deletions on empty buffer
    try:
        buf.delete_line(1)
        assert False, "Should raise IndexError on empty delete"
    except IndexError:
        print("  [Test 02 Passed] Caught delete on empty buffer.")

    # 2. Line insertions
    buf.append_line("First line of text")
    assert buf.line_count() == 1
    assert buf.get_cursor_position() == (1, "First line of text")

    buf.append_line("Third line of text")
    assert buf.line_count() == 2

    # Insert in the middle at line 2
    buf.insert_line(2, "Second line of text")
    assert buf.to_list() == [
        "First line of text",
        "Second line of text",
        "Third line of text"
    ]
    assert buf.get_cursor_position() == (2, "Second line of text")
    print("  [Test 03 Passed] Line insertions (beginning, middle, end) verified.")

    # 3. Cursor navigation
    # Move next to line 3
    assert buf.move_cursor_next() is True
    assert buf.get_cursor_position() == (3, "Third line of text")

    # Cannot move next past tail
    assert buf.move_cursor_next() is False
    assert buf.get_cursor_position() == (3, "Third line of text")

    # Move prev to line 2 then line 1
    assert buf.move_cursor_prev() is True
    assert buf.get_cursor_position() == (2, "Second line of text")
    assert buf.move_cursor_prev() is True
    assert buf.get_cursor_position() == (1, "First line of text")

    # Cannot move prev past head
    assert buf.move_cursor_prev() is False
    assert buf.get_cursor_position() == (1, "First line of text")
    print("  [Test 04 Passed] Bidirectional cursor navigation and bounds verified.")

    # 4. Line editing
    buf.edit_line(2, "Second line of text (UPDATED)")
    assert buf.to_list()[1] == "Second line of text (UPDATED)"
    assert buf.get_cursor_position() == (2, "Second line of text (UPDATED)")
    print("  [Test 05 Passed] Line editing and cursor relocation verified.")

    # 5. Line deletions
    # Delete middle line (line 2)
    del_text = buf.delete_line(2)
    assert del_text == "Second line of text (UPDATED)"
    assert buf.to_list() == ["First line of text", "Third line of text"]
    assert buf.line_count() == 2
    assert buf.get_cursor_position() == (2, "Third line of text")

    # Delete tail line
    del_text = buf.delete_line(2)
    assert del_text == "Third line of text"
    assert buf.to_list() == ["First line of text"]
    assert buf.line_count() == 1
    assert buf.get_cursor_position() == (1, "First line of text")

    # Delete remaining single line
    del_text = buf.delete_line(1)
    assert del_text == "First line of text"
    assert buf.is_empty() is True
    assert buf.get_cursor_position() == (0, None)
    print("  [Test 06 Passed] Deletions at boundaries and single-line reduction verified.")

    print("\nAll Program 05 automated tests PASSED successfully!")


def main() -> None:
    """Interactive command-line menu driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    buf = TextEditorBuffer()

    # Pre-populate initial sample document
    buf.append_line("The Zen of Python, by Tim Peters")
    buf.append_line("Beautiful is better than ugly.")
    buf.append_line("Explicit is better than implicit.")
    buf.append_line("Simple is better than complex.")

    menu = """
========================================
     TEXT EDITOR BUFFER (CO1 Lab)
========================================
1. Display All Lines (with Cursor)
2. Insert Line at Position
3. Append Line at End
4. Edit an Existing Line
5. Delete a Line
6. Move Cursor to Next Line (Down)
7. Move Cursor to Previous Line (Up)
8. Display Current Cursor Position
9. Run Automated Self-Tests
10. Exit
========================================
"""

    while True:
        print(menu)
        choice = input("Enter choice (1-10): ").strip()

        if choice == "1":
            buf.display_buffer()

        elif choice == "2":
            try:
                pos = int(input(f"Enter line position [1 to {buf.line_count() + 1}]: ").strip())
                text = input("Enter line text: ")
                buf.insert_line(pos, text)
                print(f"Inserted at Line {pos} successfully.")
            except (ValueError, IndexError, TypeError) as err:
                print(f"Error: {err}")

        elif choice == "3":
            text = input("Enter line text to append: ")
            buf.append_line(text)
            print("Appended line successfully.")

        elif choice == "4":
            try:
                pos = int(input(f"Enter line number to edit [1 to {buf.line_count()}]: ").strip())
                new_text = input("Enter replacement text: ")
                buf.edit_line(pos, new_text)
                print(f"Line {pos} updated successfully.")
            except (ValueError, IndexError, TypeError) as err:
                print(f"Error: {err}")

        elif choice == "5":
            try:
                pos = int(input(f"Enter line number to delete [1 to {buf.line_count()}]: ").strip())
                deleted = buf.delete_line(pos)
                print(f"Deleted Line {pos}: '{deleted}'")
            except (ValueError, IndexError, TypeError) as err:
                print(f"Error: {err}")

        elif choice == "6":
            if buf.move_cursor_next():
                pos, text = buf.get_cursor_position()
                print(f"Cursor moved down to Line {pos}: '{text}'")
            else:
                print("Cursor already at end of buffer.")

        elif choice == "7":
            if buf.move_cursor_prev():
                pos, text = buf.get_cursor_position()
                print(f"Cursor moved up to Line {pos}: '{text}'")
            else:
                print("Cursor already at first line of buffer.")

        elif choice == "8":
            pos, text = buf.get_cursor_position()
            if pos == 0:
                print("Buffer is currently empty.")
            else:
                print(f"Current Cursor: Line {pos} -> '{text}'")

        elif choice == "9":
            run_tests()

        elif choice == "10":
            print("Exiting Text Editor Buffer. Goodbye!")
            break

        else:
            print("Invalid selection. Please choose 1-10.")


if __name__ == "__main__":
    main()

