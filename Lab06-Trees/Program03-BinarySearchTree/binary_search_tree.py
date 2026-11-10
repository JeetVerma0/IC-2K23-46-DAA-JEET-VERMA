#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 6: Trees
Program 3: Binary Search Tree (BST) Implementation

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
A Binary Search Tree (BST) is a binary tree with the fundamental ordering property:
For any node N:
  - All keys in N's left subtree are STRICTLY LESS THAN N.key:
      key < N.key
  - All keys in N's right subtree are STRICTLY GREATER THAN N.key:
      key > N.key
  - Both left and right subtrees must also recursively satisfy the BST property.

DUPLICATE POLICY:
In this implementation, duplicate keys are STRICTLY DISALLOWED to maintain
unambiguous set semantics and key uniqueness. Attempting to insert an existing
key raises a ValueError (or is rejected with a descriptive message).

DELETION CASES:
Deleting a node from a BST requires maintaining the BST invariant:
  1. Case 1 (Leaf Node - 0 children):
     Simply detach and return None.
  2. Case 2 (One Child - Left OR Right):
     Bypass the node by returning its non-null child to the parent.
  3. Case 3 (Two Children):
     Find the Inorder Successor (the smallest node in the right subtree).
     Replace the target node's key with the successor's key.
     Recursively delete the successor from the right subtree.

BST VALIDATION:
Validation checks that every node's key falls strictly within the interval
(min_val, max_val), updated dynamically during traversal:
  - For left child: interval becomes (min_val, parent.key)
  - For right child: interval becomes (parent.key, max_val)

COMPLEXITIES:
  - Search / Insert / Delete:
      * Average-case (randomly balanced): O(log n) time
      * Worst-case (skewed degenerate tree): O(n) time
  - Inorder Traversal: O(n) time (produces keys in strictly ascending sorted order)
  - Find Min / Find Max: O(h) time where h is the tree height.
  - Auxiliary Space: O(h) recursion stack frames.
================================================================================
"""

import sys
from typing import Any, List, Optional, Tuple


class BSTNode:
    """Represents a node in a Binary Search Tree."""

    def __init__(self, key: Any) -> None:
        self.key: Any = key
        self.left: Optional["BSTNode"] = None
        self.right: Optional["BSTNode"] = None

    def __repr__(self) -> str:
        return f"BSTNode({self.key})"


class BinarySearchTree:
    """Implementation of a Binary Search Tree supporting key operations."""

    def __init__(self) -> None:
        self.root: Optional[BSTNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """Return True if tree contains no nodes."""
        return self.root is None

    def size(self) -> int:
        """Return the count of nodes currently in the BST."""
        return self._size

    # -------------------------------------------------------------------------
    # Insertion
    # -------------------------------------------------------------------------
    def insert(self, key: Any) -> None:
        """
        Insert key into the BST.
        Raises ValueError if key already exists (Duplicate Policy).
        """
        self.root = self._insert_recursive(self.root, key)
        self._size += 1

    def _insert_recursive(self, node: Optional[BSTNode], key: Any) -> BSTNode:
        if node is None:
            return BSTNode(key)

        if key < node.key:
            node.left = self._insert_recursive(node.left, key)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key)
        else:
            raise ValueError(f"Duplicate key '{key}' rejected: BST requires unique keys.")

        return node

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------
    def search(self, key: Any) -> bool:
        """Return True if key exists in the BST, False otherwise."""
        return self._search_recursive(self.root, key) is not None

    def _search_recursive(self, node: Optional[BSTNode], key: Any) -> Optional[BSTNode]:
        if node is None or node.key == key:
            return node

        if key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    # -------------------------------------------------------------------------
    # Deletion
    # -------------------------------------------------------------------------
    def delete(self, key: Any) -> None:
        """
        Delete key from the BST.
        Raises KeyError if key is not present.
        """
        if not self.search(key):
            raise KeyError(f"Key '{key}' not found in the BST.")
        self.root = self._delete_recursive(self.root, key)
        self._size -= 1

    def _delete_recursive(self, node: Optional[BSTNode], key: Any) -> Optional[BSTNode]:
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Node to delete found!
            # Case 1: Leaf node (no children)
            if node.left is None and node.right is None:
                return None

            # Case 2: One child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Case 3: Two children
            # Find inorder successor (minimum key in right subtree)
            successor = self._find_min_node(node.right)
            node.key = successor.key
            # Delete successor from right subtree
            node.right = self._delete_recursive(node.right, successor.key)

        return node

    # -------------------------------------------------------------------------
    # Min & Max
    # -------------------------------------------------------------------------
    def find_min(self) -> Any:
        """Return the minimum key in the BST."""
        if self.is_empty():
            raise IndexError("Cannot find_min on an empty BST.")
        assert self.root is not None
        return self._find_min_node(self.root).key

    def _find_min_node(self, node: BSTNode) -> BSTNode:
        curr = node
        while curr.left is not None:
            curr = curr.left
        return curr

    def find_max(self) -> Any:
        """Return the maximum key in the BST."""
        if self.is_empty():
            raise IndexError("Cannot find_max on an empty BST.")
        assert self.root is not None
        curr = self.root
        while curr.right is not None:
            curr = curr.right
        return curr.key

    # -------------------------------------------------------------------------
    # Traversals
    # -------------------------------------------------------------------------
    def inorder_traversal(self) -> List[Any]:
        """Return list of keys in sorted ascending order."""
        result: List[Any] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[BSTNode], result: List[Any]) -> None:
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    # -------------------------------------------------------------------------
    # BST Validation
    # -------------------------------------------------------------------------
    def validate_bst(self) -> bool:
        """
        Validate whether the current tree structure strictly conforms to BST ordering.
        Algorithm: Recursively verifies min_val < node.key < max_val.
        """
        return self._validate_recursive(self.root, float("-inf"), float("inf"))

    def _validate_recursive(self, node: Optional[BSTNode], min_val: float, max_val: float) -> bool:
        if node is None:
            return True

        if not (min_val < node.key < max_val):
            return False

        # Left subtree keys must be < node.key
        # Right subtree keys must be > node.key
        return (
            self._validate_recursive(node.left, min_val, node.key)
            and self._validate_recursive(node.right, node.key, max_val)
        )

    # -------------------------------------------------------------------------
    # Tree Visualization
    # -------------------------------------------------------------------------
    def print_tree(self) -> None:
        """Print an ASCII visualization of the BST."""
        if self.root is None:
            print("  BST is empty.")
            return
        self._print_ascii(self.root, prefix="", is_left=True, is_root=True)

    def _print_ascii(self, node: Optional[BSTNode], prefix: str, is_left: bool, is_root: bool = False) -> None:
        if node is None:
            return
        if is_root:
            print(f"  [Root] {node.key}")
        else:
            branch = "|-- (L) " if is_left else "`-- (R) "
            print(f"  {prefix}{branch}{node.key}")

        extension = "|   " if is_left else "    "
        new_prefix = prefix + ("" if is_root else extension)
        if node.left or node.right:
            if node.left:
                self._print_ascii(node.left, new_prefix, is_left=True)
            else:
                print(f"  {new_prefix}|-- (L) None")
            if node.right:
                self._print_ascii(node.right, new_prefix, is_left=False)
            else:
                print(f"  {new_prefix}`-- (R) None")


def run_tests() -> None:
    """Automated unit verification test suite for Binary Search Tree."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Binary Search Tree (BST)")
    print("=" * 70)

    bst = BinarySearchTree()
    assert bst.is_empty() is True
    assert bst.validate_bst() is True
    print("[PASS] Test 1: Initial empty tree state and validation verified.")

    # Test 2: Insertions and Inorder sorting
    # Insert sequence: 50, 30, 70, 20, 40, 60, 80
    keys = [50, 30, 70, 20, 40, 60, 80]
    for k in keys:
        bst.insert(k)

    assert bst.size() == 7
    assert bst.inorder_traversal() == [20, 30, 40, 50, 60, 70, 80]
    assert bst.find_min() == 20
    assert bst.find_max() == 80
    assert bst.validate_bst() is True
    print("[PASS] Test 2: Insertions, min, max, and sorted inorder verified.")

    # Test 3: Search functionality
    assert bst.search(40) is True
    assert bst.search(70) is True
    assert bst.search(99) is False
    assert bst.search(10) is False
    print("[PASS] Test 3: Search hits and misses verified.")

    # Test 4: Duplicate Policy enforcement
    try:
        bst.insert(30)
        assert False, "Should raise ValueError on duplicate key insert"
    except ValueError:
        pass
    print("[PASS] Test 4: Duplicate insertion rejection verified.")

    # Test 5: Deletion Case 1 — Leaf node (delete 20)
    bst.delete(20)
    assert bst.search(20) is False
    assert bst.inorder_traversal() == [30, 40, 50, 60, 70, 80]
    assert bst.validate_bst() is True
    print("[PASS] Test 5: Deletion Case 1 (Leaf node deletion) verified.")

    # Test 6: Deletion Case 2 — One child (delete 30, which now has only right child 40)
    bst.delete(30)
    assert bst.search(30) is False
    assert bst.inorder_traversal() == [40, 50, 60, 70, 80]
    assert bst.validate_bst() is True
    print("[PASS] Test 6: Deletion Case 2 (One child node deletion) verified.")

    # Test 7: Deletion Case 3 — Two children (delete root 50, successor is 60)
    bst.delete(50)
    assert bst.search(50) is False
    assert bst.inorder_traversal() == [40, 60, 70, 80]
    assert bst.validate_bst() is True
    assert bst.root.key == 60  # Root replaced by inorder successor
    print("[PASS] Test 7: Deletion Case 3 (Two children node deletion) verified.")

    # Test 8: Deletion error handling on non-existent key
    try:
        bst.delete(999)
        assert False, "Should raise KeyError on non-existent key"
    except KeyError:
        pass
    print("[PASS] Test 8: Non-existent key deletion error handling verified.")

    print("\nALL 8 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 55)
    print("          BINARY SEARCH TREE (BST) MENU")
    print("=" * 55)
    print(" 1. Insert a Key")
    print(" 2. Search for a Key")
    print(" 3. Delete a Key (Handles Leaf, 1-Child, 2-Child Cases)")
    print(" 4. Find Minimum Key")
    print(" 5. Find Maximum Key")
    print(" 6. Display Inorder Traversal (Sorted Keys)")
    print(" 7. Display BST Structure (ASCII)")
    print(" 8. Validate BST Property")
    print(" 9. Populate with Sample Set [50, 30, 70, 20, 40, 60, 80]")
    print(" 10. Run Automated Tests (--test)")
    print(" 11. Exit")
    print("=" * 55)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 6 — Binary Search Tree (BST) Demo")
    print("==========================================================")

    bst = BinarySearchTree()

    while True:
        print_menu()
        choice = input("Enter choice (1-11): ").strip()

        if choice == "1":
            val_str = input("Enter integer key to insert: ").strip()
            try:
                val = int(val_str)
                bst.insert(val)
                print(f"Key {val} inserted successfully.")
            except ValueError as err:
                print(f"Insertion Error: {err}")

        elif choice == "2":
            val_str = input("Enter key to search: ").strip()
            try:
                val = int(val_str)
                found = bst.search(val)
                if found:
                    print(f"Key {val} FOUND in the BST.")
                else:
                    print(f"Key {val} NOT FOUND in the BST.")
            except ValueError:
                print("Invalid integer input!")

        elif choice == "3":
            val_str = input("Enter key to delete: ").strip()
            try:
                val = int(val_str)
                bst.delete(val)
                print(f"Key {val} deleted successfully.")
            except (ValueError, KeyError) as err:
                print(f"Deletion Error: {err}")

        elif choice == "4":
            try:
                print(f"Minimum Key in BST: {bst.find_min()}")
            except IndexError as err:
                print(f"Error: {err}")

        elif choice == "5":
            try:
                print(f"Maximum Key in BST: {bst.find_max()}")
            except IndexError as err:
                print(f"Error: {err}")

        elif choice == "6":
            keys = bst.inorder_traversal()
            print(f"Inorder Traversal: {' -> '.join(map(str, keys)) if keys else '[Empty BST]'}")

        elif choice == "7":
            print("\nBST Structure:")
            bst.print_tree()

        elif choice == "8":
            valid = bst.validate_bst()
            print(f"Is Valid BST? {valid}")

        elif choice == "9":
            bst = BinarySearchTree()
            for k in [50, 30, 70, 20, 40, 60, 80]:
                bst.insert(k)
            print("Loaded sample set [50, 30, 70, 20, 40, 60, 80].")

        elif choice == "10":
            run_tests()

        elif choice == "11":
            print("Exiting BST Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 11.")


if __name__ == "__main__":
    main()

