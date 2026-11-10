#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 6: Trees
Program 7: Compiler Symbol Table using Binary Search Tree (BST)

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
A Symbol Table is a core data structure used by language compilers, interpreters,
and static analyzers to store and track metadata about declared source-code
identifiers (variables, constants, functions, classes).

WHY A BINARY SEARCH TREE?
While hash tables are frequently used in modern production compilers, a BST
offers significant advantages:
  1. Lexicographical Sorting: Inorder traversal immediately yields all symbols
     in alphabetical order without requiring a separate sorting pass.
  2. Range Searches & Prefix Queries: Finding all identifiers starting with a
     given prefix or within a namespace scope is efficient in a BST.
  3. Dynamic Size: BSTs expand dynamically without costly hash table rehashing.

SYMBOL RECORD ATTRIBUTES:
  - Identifier Name: Unique variable/function name (acts as BST search key).
  - Data Type: Type signature (e.g., 'int', 'float', 'string', 'boolean', 'func').
  - Value / Info: Initial or runtime value, memory offset, or signature.
  - Scope: Scope level (e.g., 'global', 'local', 'param').
  - Line Declared: Line number in the source file for compiler diagnostics.

ERROR DETECTION & VALIDATION:
  - Duplicate Declaration Error: Attempting to insert an identifier that is already
    declared raises a ValueError.
  - Undeclared Identifier Error: Attempting to lookup, update, or delete a symbol
    not present in the table raises a KeyError.

COMPLEXITIES:
  - Insert / Lookup / Update / Delete:
      * Average-Case: O(log n) time
      * Worst-Case: O(n) time for skewed trees
  - Display All (Inorder): O(n) time
  - Auxiliary Space: O(n) for tree nodes.
================================================================================
"""

import sys
from typing import Any, List, Optional, Tuple


class SymbolRecord:
    """Encapsulates compiler metadata for a single declared identifier."""

    def __init__(
        self,
        name: str,
        data_type: str,
        value: Any,
        scope: str = "global",
        line: int = 1,
    ) -> None:
        self.name: str = name
        self.data_type: str = data_type
        self.value: Any = value
        self.scope: str = scope
        self.line: int = line

    def __repr__(self) -> str:
        return (
            f"Symbol({self.name}: {self.data_type} = {self.value!r}, "
            f"scope={self.scope}, line={self.line})"
        )

    def to_row(self) -> str:
        """Format as a clean table row."""
        return (
            f"| {self.name:<15} | {self.data_type:<10} | {str(self.value):<15} | "
            f"{self.scope:<10} | {self.line:<6} |"
        )


class BSTSymbolNode:
    """Represents a node in the Symbol Table Binary Search Tree."""

    def __init__(self, record: SymbolRecord) -> None:
        self.record: SymbolRecord = record
        self.left: Optional["BSTSymbolNode"] = None
        self.right: Optional["BSTSymbolNode"] = None

    @property
    def key(self) -> str:
        return self.record.name


class SymbolTable:
    """
    Compiler Symbol Table implemented using a Binary Search Tree.
    Does NOT use Python dictionaries for symbol storage.
    """

    def __init__(self) -> None:
        self.root: Optional[BSTSymbolNode] = None
        self._count: int = 0

    def size(self) -> int:
        """Return total number of symbols declared in the table."""
        return self._count

    def is_empty(self) -> bool:
        """Check if symbol table is empty."""
        return self.root is None

    # -------------------------------------------------------------------------
    # Insert Symbol
    # -------------------------------------------------------------------------
    def insert(
        self,
        name: str,
        data_type: str,
        value: Any,
        scope: str = "global",
        line: int = 1,
    ) -> SymbolRecord:
        """
        Insert a new identifier into the symbol table.
        Raises ValueError if identifier is already declared (Duplicate Detection).
        """
        if not name or not name.isidentifier():
            raise ValueError(f"Invalid identifier name '{name}': Must be a valid programming identifier.")

        record = SymbolRecord(name, data_type, value, scope, line)
        self.root = self._insert_recursive(self.root, record)
        self._count += 1
        return record

    def _insert_recursive(self, node: Optional[BSTSymbolNode], record: SymbolRecord) -> BSTSymbolNode:
        if node is None:
            return BSTSymbolNode(record)

        if record.name < node.key:
            node.left = self._insert_recursive(node.left, record)
        elif record.name > node.key:
            node.right = self._insert_recursive(node.right, record)
        else:
            raise ValueError(
                f"Compile Error (Line {record.line}): Redundant declaration of identifier '{record.name}' "
                f"(Already declared on Line {node.record.line})."
            )

        return node

    # -------------------------------------------------------------------------
    # Lookup / Search
    # -------------------------------------------------------------------------
    def lookup(self, name: str) -> Optional[SymbolRecord]:
        """
        Search for an identifier by name.
        Returns the SymbolRecord if found, or None if undeclared.
        """
        curr = self.root
        while curr is not None:
            if name == curr.key:
                return curr.record
            elif name < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return None

    # -------------------------------------------------------------------------
    # Update Symbol
    # -------------------------------------------------------------------------
    def update(
        self,
        name: str,
        new_value: Any,
        new_type: Optional[str] = None,
    ) -> SymbolRecord:
        """
        Update the value and/or data type of an existing symbol.
        Raises KeyError if the identifier has not been declared.
        """
        record = self.lookup(name)
        if record is None:
            raise KeyError(f"Compile Error: Cannot update undeclared identifier '{name}'.")

        record.value = new_value
        if new_type is not None:
            record.data_type = new_type
        return record

    # -------------------------------------------------------------------------
    # Delete Symbol
    # -------------------------------------------------------------------------
    def delete(self, name: str) -> SymbolRecord:
        """
        Delete a symbol from the table (e.g., when exiting a scope block).
        Raises KeyError if identifier is not found.
        """
        target_record = self.lookup(name)
        if target_record is None:
            raise KeyError(f"Compile Error: Cannot delete undeclared identifier '{name}'.")

        self.root = self._delete_recursive(self.root, name)
        self._count -= 1
        return target_record

    def _delete_recursive(self, node: Optional[BSTSymbolNode], name: str) -> Optional[BSTSymbolNode]:
        if node is None:
            return None

        if name < node.key:
            node.left = self._delete_recursive(node.left, name)
        elif name > node.key:
            node.right = self._delete_recursive(node.right, name)
        else:
            # Node found
            # Case 1 & 2: 0 or 1 child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Case 3: 2 children -> replace with inorder successor
            successor = self._find_min_node(node.right)
            node.record = successor.record
            node.right = self._delete_recursive(node.right, successor.key)

        return node

    def _find_min_node(self, node: BSTSymbolNode) -> BSTSymbolNode:
        curr = node
        while curr.left is not None:
            curr = curr.left
        return curr

    # -------------------------------------------------------------------------
    # Inorder Listing (Sorted Alphabetically)
    # -------------------------------------------------------------------------
    def get_all_symbols(self) -> List[SymbolRecord]:
        """Return all declared symbols in sorted alphabetical order."""
        records: List[SymbolRecord] = []
        self._inorder(self.root, records)
        return records

    def _inorder(self, node: Optional[BSTSymbolNode], records: List[SymbolRecord]) -> None:
        if node is not None:
            self._inorder(node.left, records)
            records.append(node.record)
            self._inorder(node.right, records)

    def display(self) -> None:
        """Display formatted table of all declared symbols."""
        symbols = self.get_all_symbols()
        print("\n" + "=" * 68)
        print("                   COMPILER SYMBOL TABLE (BST)")
        print(f"               Total Declared Identifiers: {len(symbols)}")
        print("=" * 68)
        print(f"| {'Identifier':<15} | {'Type':<10} | {'Value':<15} | {'Scope':<10} | {'Line':<6} |")
        print("+" + "-" * 17 + "+" + "-" * 12 + "+" + "-" * 17 + "+" + "-" * 12 + "+" + "-" * 8 + "+")

        if not symbols:
            print(f"| {'[SYMBOL TABLE IS CURRENTLY EMPTY]':^66} |")
        else:
            for rec in symbols:
                print(rec.to_row())

        print("+" + "-" * 17 + "+" + "-" * 12 + "+" + "-" * 17 + "+" + "-" * 12 + "+" + "-" * 8 + "+")


def build_sample_symbol_table() -> SymbolTable:
    """Populate sample programming symbols for demonstration."""
    st = SymbolTable()
    st.insert("counter", "int", 0, "global", line=5)
    st.insert("MAX_BUFFER", "const int", 1024, "global", line=6)
    st.insert("pi", "float", 3.14159, "global", line=7)
    st.insert("username", "string", "admin", "local", line=12)
    st.insert("is_active", "boolean", True, "local", line=13)
    st.insert("calculate_sum", "function", "<func_ptr>", "global", line=20)
    return st


def run_tests() -> None:
    """Automated unit verification test suite for BST Symbol Table."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Compiler Symbol Table (BST)")
    print("=" * 70)

    st = SymbolTable()
    assert st.is_empty() is True
    assert st.size() == 0
    print("[PASS] Test 1: Empty symbol table initialized.")

    # Test 2: Insert symbols
    st.insert("alpha", "int", 10, "global", line=1)
    st.insert("beta", "float", 2.5, "global", line=2)
    st.insert("gamma", "string", "hello", "local", line=3)
    assert st.size() == 3
    print("[PASS] Test 2: Symbol insertions verified.")

    # Test 3: Inorder sorted alphabetical display
    names = [s.name for s in st.get_all_symbols()]
    assert names == ["alpha", "beta", "gamma"]
    print("[PASS] Test 3: Alphabetical ordering (alpha -> beta -> gamma) verified.")

    # Test 4: Duplicate declaration detection
    try:
        st.insert("beta", "int", 99, "local", line=4)
        assert False, "Should raise ValueError on duplicate identifier"
    except ValueError:
        pass
    print("[PASS] Test 4: Duplicate identifier rejection verified.")

    # Test 5: Lookup hit and miss
    rec = st.lookup("gamma")
    assert rec is not None and rec.data_type == "string" and rec.value == "hello"
    assert st.lookup("undeclared_var") is None
    print("[PASS] Test 5: Identifier lookup hit and miss verified.")

    # Test 6: Update symbol value and missing validation
    st.update("alpha", 42)
    assert st.lookup("alpha").value == 42
    try:
        st.update("missing_var", 100)
        assert False, "Should raise KeyError on update of missing identifier"
    except KeyError:
        pass
    print("[PASS] Test 6: Symbol update and missing validation verified.")

    # Test 7: Deletion of symbol and missing validation
    st.delete("beta")
    assert st.size() == 2
    assert st.lookup("beta") is None
    assert [s.name for s in st.get_all_symbols()] == ["alpha", "gamma"]
    try:
        st.delete("beta")
        assert False, "Should raise KeyError on deleting already removed symbol"
    except KeyError:
        pass
    print("[PASS] Test 7: Symbol deletion and missing identifier validation verified.")

    print("\nALL 7 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 55)
    print("          COMPILER SYMBOL TABLE (BST) MENU")
    print("=" * 55)
    print(" 1. Insert New Symbol (Identifier, Type, Value, Scope, Line)")
    print(" 2. Lookup / Search Identifier")
    print(" 3. Update Existing Symbol Value")
    print(" 4. Delete Symbol (Exit Scope)")
    print(" 5. Display All Symbols (Alphabetical Inorder Table)")
    print(" 6. Load Sample Programming Symbols")
    print(" 7. Run Automated Tests (--test)")
    print(" 8. Exit")
    print("=" * 55)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 6 — Compiler Symbol Table (BST) Demo")
    print("==========================================================")

    st = build_sample_symbol_table()
    print("Initialized symbol table with sample program identifiers.")

    while True:
        print_menu()
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            name = input("Enter identifier name: ").strip()
            dtype = input("Enter data type (int, float, string, etc.): ").strip()
            val = input("Enter initial value: ").strip()
            scope = input("Enter scope (global/local/param) [default: global]: ").strip()
            line_str = input("Enter declaration line number [default: 1]: ").strip()

            scope_val = scope if scope else "global"
            line_val = int(line_str) if line_str.isdigit() else 1

            try:
                st.insert(name, dtype, val, scope_val, line_val)
                print(f"Symbol '{name}' inserted successfully.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == "2":
            name = input("Enter identifier name to lookup: ").strip()
            rec = st.lookup(name)
            if rec:
                print("\nSymbol Record Found:")
                print(f"  Identifier: {rec.name}")
                print(f"  Type:       {rec.data_type}")
                print(f"  Value:      {rec.value}")
                print(f"  Scope:      {rec.scope}")
                print(f"  Line:       {rec.line}")
            else:
                print(f"Compile Error: Identifier '{name}' is undeclared.")

        elif choice == "3":
            name = input("Enter identifier name to update: ").strip()
            new_val = input("Enter new value: ").strip()
            try:
                st.update(name, new_val)
                print(f"Symbol '{name}' updated to value '{new_val}'.")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "4":
            name = input("Enter identifier name to delete: ").strip()
            try:
                st.delete(name)
                print(f"Symbol '{name}' removed from table.")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "5":
            st.display()

        elif choice == "6":
            st = build_sample_symbol_table()
            print("Reset to sample programming symbols.")

        elif choice == "7":
            run_tests()

        elif choice == "8":
            print("Exiting Symbol Table Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 8.")


if __name__ == "__main__":
    main()

