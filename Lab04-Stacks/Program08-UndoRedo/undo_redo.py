"""
Program 08: Undo/Redo Feature Using Command/Memento Pattern and Dual Stacks
Course: IC-307D Data Structures and Algorithms Lab
Unit 4: Stacks (CO1)

This program models an interactive text application with Undo and Redo features
using two LIFO stacks:
- The Dual-Stack Architecture:
    1. Undo Stack:
       Stores previous document snapshots/states. Every mutating operation (insert,
       delete, clear) records the pre-mutation state on the undo stack before applying
       the modification.
    2. Redo Stack:
       Stores states that have been undone, enabling the user to step forward again.
- The Golden Rule of Undo/Redo:
    Whenever the user executes a NEW mutating operation (insert, delete), the Redo
    history is invalidated and must be completely CLEARED. This branches document
    history into a new timeline.
- LIFO Principle in Undo/Redo:
    - Undo: Pops the most recently pushed state from undo_stack, pushes the current
      state onto redo_stack, and reverts current_text to the popped state.
    - Redo: Pops the most recently undone state from redo_stack, pushes current_text
      onto undo_stack, and restores current_text to the popped state.
- Interactive menu driver and automated test suite (--test flag).
"""

import sys
from typing import List, Optional


class UndoRedoTextEditor:
    """
    In-memory text editor engine with dual-stack undo/redo capabilities.

    Attributes:
        current_text (str): The active document text.
        undo_stack (List[str]): Stack of historical states available for undo.
        redo_stack (List[str]): Stack of undone states available for redo.
    """

    def __init__(self, initial_text: str = "") -> None:
        self.current_text: str = str(initial_text)
        self.undo_stack: List[str] = []
        self.redo_stack: List[str] = []

    def get_text(self) -> str:
        """Returns the current document text."""
        return self.current_text

    def can_undo(self) -> bool:
        """Checks if an undo operation is possible."""
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        """Checks if a redo operation is possible."""
        return len(self.redo_stack) > 0

    def insert_text(self, text: str) -> None:
        """
        Appends text to the document.
        Saves current state to undo_stack and invalidates/clears redo_stack.

        Time Complexity: O(n) snapshot copy
        Auxiliary Space Complexity: O(n)
        """
        if not text:
            return

        # Snapshot current state
        self.undo_stack.append(self.current_text)
        # Clear redo history on new edit
        self.redo_stack.clear()
        # Mutate document
        self.current_text += text

    def delete_text(self, count: int) -> str:
        """
        Deletes the last 'count' characters from the document.
        Saves current state to undo_stack and clears redo_stack.

        Returns:
            The deleted string substring.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        if count <= 0:
            return ""

        if not self.current_text:
            return ""

        self.undo_stack.append(self.current_text)
        self.redo_stack.clear()

        # Clamp deletion count
        actual_count = min(count, len(self.current_text))
        deleted_part = self.current_text[-actual_count:]
        self.current_text = self.current_text[:-actual_count]
        return deleted_part

    def clear_text(self) -> None:
        """Clears the document text completely."""
        if not self.current_text:
            return

        self.undo_stack.append(self.current_text)
        self.redo_stack.clear()
        self.current_text = ""

    def undo(self) -> bool:
        """
        Reverts the document to its state prior to the most recent operation.
        Pushes current state to redo_stack.

        Returns:
            True if undo succeeded, False if undo_stack was empty.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        if not self.undo_stack:
            return False

        # Save current state for redo
        self.redo_stack.append(self.current_text)
        # Revert state
        self.current_text = self.undo_stack.pop()
        return True

    def redo(self) -> bool:
        """
        Re-applies the most recently undone operation.
        Pushes current state to undo_stack.

        Returns:
            True if redo succeeded, False if redo_stack was empty.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        if not self.redo_stack:
            return False

        # Save current state for undo
        self.undo_stack.append(self.current_text)
        # Advance state
        self.current_text = self.redo_stack.pop()
        return True

    def display_status(self) -> None:
        """Prints formatted editor status, active text, and stack depths."""
        print("-" * 55)
        print(f"  ACTIVE DOCUMENT: \"{self.current_text}\"")
        print(f"  Length: {len(self.current_text)} chars | Undo Stack: {len(self.undo_stack)} | Redo Stack: {len(self.redo_stack)}")
        print("-" * 55)


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Runs comprehensive tests for undo/redo text editor operations."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Undo/Redo Editor (Program 08)")
    print("=" * 65)

    editor = UndoRedoTextEditor()

    # 1. Initial state
    assert editor.get_text() == ""
    assert editor.can_undo() is False
    assert editor.can_redo() is False
    assert editor.undo() is False
    assert editor.redo() is False
    print("  [Test 01 Passed] Initialized empty editor and empty stack handling.")

    # 2. Text insertions
    editor.insert_text("Hello")
    assert editor.get_text() == "Hello"
    assert editor.can_undo() is True
    assert editor.can_redo() is False

    editor.insert_text(" World")
    assert editor.get_text() == "Hello World"
    assert len(editor.undo_stack) == 2  # ["", "Hello"]
    print("  [Test 02 Passed] Text insertion and undo stack tracking verified.")

    # 3. Text deletion
    deleted = editor.delete_text(6)
    assert deleted == " World"
    assert editor.get_text() == "Hello"
    assert len(editor.undo_stack) == 3
    print("  [Test 03 Passed] Text deletion and snapshot verified.")

    # 4. Undo sequence
    # Undo deletion -> restores "Hello World"
    assert editor.undo() is True
    assert editor.get_text() == "Hello World"
    assert editor.can_redo() is True

    # Undo second insertion -> restores "Hello"
    assert editor.undo() is True
    assert editor.get_text() == "Hello"

    # Undo first insertion -> restores ""
    assert editor.undo() is True
    assert editor.get_text() == ""
    assert editor.can_undo() is False
    print("  [Test 04 Passed] Multi-level sequential undo verified.")

    # 5. Redo sequence
    # Redo step 1 -> "Hello"
    assert editor.redo() is True
    assert editor.get_text() == "Hello"

    # Redo step 2 -> "Hello World"
    assert editor.redo() is True
    assert editor.get_text() == "Hello World"

    # Redo step 3 -> "Hello" (the state after deletion)
    assert editor.redo() is True
    assert editor.get_text() == "Hello"
    assert editor.can_redo() is False
    print("  [Test 05 Passed] Multi-level sequential redo verified.")

    # 6. Branching history: new edit after undo MUST clear redo stack
    # Currently at "Hello". Undo back to "Hello World".
    assert editor.undo() is True
    assert editor.get_text() == "Hello World"
    assert editor.can_redo() is True  # Redo has ["Hello"]

    # Now make a brand new edit: insert "!"
    editor.insert_text("!")
    assert editor.get_text() == "Hello World!"
    # Redo stack MUST be completely cleared!
    assert editor.can_redo() is False
    assert len(editor.redo_stack) == 0
    assert editor.redo() is False
    print("  [Test 06 Passed] Branching edit clears redo history verified.")

    # 7. Document clear operation
    editor.clear_text()
    assert editor.get_text() == ""
    assert editor.undo() is True
    assert editor.get_text() == "Hello World!"
    print("  [Test 07 Passed] Clear operation and recovery via undo verified.")

    print("\nAll Program 08 automated tests PASSED successfully!")


def main() -> None:
    """Interactive command-line text editor driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    editor = UndoRedoTextEditor("Hello")

    menu = """
========================================
     UNDO / REDO TEXT EDITOR (CO1)
========================================
1. Display Document Status
2. Insert Text
3. Delete Last N Characters
4. Clear Document Text
5. Undo Last Action
6. Redo Action
7. Run Automated Self-Tests
8. Exit
========================================
"""

    while True:
        print(menu)
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            editor.display_status()

        elif choice == "2":
            text = input("Enter text to insert: ")
            editor.insert_text(text)
            print("Text inserted successfully.")
            editor.display_status()

        elif choice == "3":
            try:
                cnt = int(input("Enter number of characters to delete: ").strip())
                deleted = editor.delete_text(cnt)
                print(f"Deleted {len(deleted)} character(s): '{deleted}'")
                editor.display_status()
            except ValueError:
                print("Error: Please enter a valid integer.")

        elif choice == "4":
            editor.clear_text()
            print("Document cleared.")
            editor.display_status()

        elif choice == "5":
            if editor.undo():
                print("Undo successful.")
            else:
                print("Cannot Undo: Undo stack is empty.")
            editor.display_status()

        elif choice == "6":
            if editor.redo():
                print("Redo successful.")
            else:
                print("Cannot Redo: Redo stack is empty.")
            editor.display_status()

        elif choice == "7":
            run_tests()

        elif choice == "8":
            print("Exiting Text Editor. Goodbye!")
            break

        else:
            print("Invalid selection. Please choose 1-8.")


if __name__ == "__main__":
    main()

