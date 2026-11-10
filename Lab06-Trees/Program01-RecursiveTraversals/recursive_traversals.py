#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 6: Trees
Program 1: Binary Tree — Recursive Traversals (Preorder, Inorder, Postorder)

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
A Binary Tree is a non-linear, hierarchical data structure where each node
has at most two children, referred to as the left child and right child:
  - Root: The topmost node without a parent.
  - Leaf: A node with no children (left = None and right = None).
  - Internal Node: A node with at least one child.

TREE TRAVERSAL DEFINITIONS:
Traversal is the process of visiting each node in the tree exactly once.
Because trees are non-linear, traversal order determines the sequence in which
values are processed:

1. Preorder Traversal (Root -> Left -> Right):
   - Visit current node (Root)
   - Recursively traverse Left Subtree
   - Recursively traverse Right Subtree
   - Use cases: Copying/serializing trees, expression tree prefix generation.

2. Inorder Traversal (Left -> Root -> Right):
   - Recursively traverse Left Subtree
   - Visit current node (Root)
   - Recursively traverse Right Subtree
   - Use cases: For a Binary Search Tree (BST), inorder produces sorted ascending order.

3. Postorder Traversal (Left -> Right -> Root):
   - Recursively traverse Left Subtree
   - Recursively traverse Right Subtree
   - Visit current node (Root)
   - Use cases: Deleting/freeing tree nodes (bottom-up), postfix expression evaluation.

COMPLEXITIES:
  - Time Complexity: O(n) for all traversals, where n is the number of nodes.
    Each node is visited a constant number of times.
  - Auxiliary Space: O(h) where h is the height of the tree, corresponding to
    the call stack frames:
      * Worst-case (skewed tree): O(n)
      * Best-case (balanced tree): O(log n)
================================================================================
"""

import sys
from typing import Any, List, Optional


class TreeNode:
    """Represents an individual node in a binary tree."""

    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None

    def __repr__(self) -> str:
        return f"TreeNode({self.data})"


class BinaryTree:
    """Represents a binary tree structure providing recursive traversals."""

    def __init__(self, root: Optional[TreeNode] = None) -> None:
        self.root: Optional[TreeNode] = root

    # -------------------------------------------------------------------------
    # 1. Preorder Traversal: Root -> Left -> Right
    # -------------------------------------------------------------------------
    def preorder_traversal(self) -> List[Any]:
        """
        Public method to perform recursive preorder traversal.
        Returns: List of visited node data in preorder sequence.
        """
        result: List[Any] = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """Recursive helper for preorder traversal."""
        if node is not None:
            result.append(node.data)          # 1. Visit Root
            self._preorder(node.left, result)   # 2. Traverse Left Subtree
            self._preorder(node.right, result)  # 3. Traverse Right Subtree

    # -------------------------------------------------------------------------
    # 2. Inorder Traversal: Left -> Root -> Right
    # -------------------------------------------------------------------------
    def inorder_traversal(self) -> List[Any]:
        """
        Public method to perform recursive inorder traversal.
        Returns: List of visited node data in inorder sequence.
        """
        result: List[Any] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """Recursive helper for inorder traversal."""
        if node is not None:
            self._inorder(node.left, result)    # 1. Traverse Left Subtree
            result.append(node.data)          # 2. Visit Root
            self._inorder(node.right, result)   # 3. Traverse Right Subtree

    # -------------------------------------------------------------------------
    # 3. Postorder Traversal: Left -> Right -> Root
    # -------------------------------------------------------------------------
    def postorder_traversal(self) -> List[Any]:
        """
        Public method to perform recursive postorder traversal.
        Returns: List of visited node data in postorder sequence.
        """
        result: List[Any] = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """Recursive helper for postorder traversal."""
        if node is not None:
            self._postorder(node.left, result)   # 1. Traverse Left Subtree
            self._postorder(node.right, result)  # 2. Traverse Right Subtree
            result.append(node.data)           # 3. Visit Root

    # -------------------------------------------------------------------------
    # Tree Visualization & Diagnostics
    # -------------------------------------------------------------------------
    def print_tree_structure(self) -> None:
        """Print an ASCII diagram of the binary tree structure."""
        if self.root is None:
            print("  Tree is empty.")
            return
        self._print_ascii(self.root, prefix="", is_left=True, is_root=True)

    def _print_ascii(self, node: Optional[TreeNode], prefix: str, is_left: bool, is_root: bool = False) -> None:
        if node is None:
            return
        if is_root:
            print(f"  [Root] {node.data}")
        else:
            branch = "|-- (L) " if is_left else "`-- (R) "
            print(f"  {prefix}{branch}{node.data}")

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


def build_sample_tree() -> BinaryTree:
    """
    Construct a clear reference binary tree for testing and demonstrations:

                 1
               /   \\
              2     3
             / \\   / \\
            4   5 6   7

    Traversals for this tree:
      - Preorder  (Root, Left, Right): [1, 2, 4, 5, 3, 6, 7]
      - Inorder   (Left, Root, Right): [4, 2, 5, 1, 6, 3, 7]
      - Postorder (Left, Right, Root): [4, 5, 2, 6, 7, 3, 1]
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)

    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    return BinaryTree(root)


def run_tests() -> None:
    """Automated unit verification test suite for recursive tree traversals."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Binary Tree Recursive Traversals")
    print("=" * 70)

    # Test 1: Empty tree
    empty_tree = BinaryTree()
    assert empty_tree.preorder_traversal() == []
    assert empty_tree.inorder_traversal() == []
    assert empty_tree.postorder_traversal() == []
    print("[PASS] Test 1: Empty tree traversals handled correctly.")

    # Test 2: Single node tree
    single_node_tree = BinaryTree(TreeNode("RootOnly"))
    assert single_node_tree.preorder_traversal() == ["RootOnly"]
    assert single_node_tree.inorder_traversal() == ["RootOnly"]
    assert single_node_tree.postorder_traversal() == ["RootOnly"]
    print("[PASS] Test 2: Single-node tree traversals verified.")

    # Test 3: Standard 7-node complete binary tree
    tree = build_sample_tree()
    pre_res = tree.preorder_traversal()
    in_res = tree.inorder_traversal()
    post_res = tree.postorder_traversal()

    expected_pre = [1, 2, 4, 5, 3, 6, 7]
    expected_in = [4, 2, 5, 1, 6, 3, 7]
    expected_post = [4, 5, 2, 6, 7, 3, 1]

    assert pre_res == expected_pre, f"Preorder mismatch: got {pre_res}, expected {expected_pre}"
    assert in_res == expected_in, f"Inorder mismatch: got {in_res}, expected {expected_in}"
    assert post_res == expected_post, f"Postorder mismatch: got {post_res}, expected {expected_post}"
    print(f"[PASS] Test 3: Preorder verified  -> {pre_res}")
    print(f"[PASS] Test 4: Inorder verified   -> {in_res}")
    print(f"[PASS] Test 5: Postorder verified -> {post_res}")

    print("\nALL 5 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 55)
    print("     BINARY TREE RECURSIVE TRAVERSALS MENU")
    print("=" * 55)
    print(" 1. Display Current Tree Structure (ASCII)")
    print(" 2. Perform Preorder Traversal  (Root -> Left -> Right)")
    print(" 3. Perform Inorder Traversal   (Left -> Root -> Right)")
    print(" 4. Perform Postorder Traversal (Left -> Right -> Root)")
    print(" 5. Build New Custom Small Tree")
    print(" 6. Reset to Sample 7-Node Reference Tree")
    print(" 7. Run Automated Tests (--test)")
    print(" 8. Exit")
    print("=" * 55)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 6 — Binary Tree Recursive Traversals")
    print("==========================================================")

    tree = build_sample_tree()
    print("Initialized default sample 7-node binary tree.")

    while True:
        print_menu()
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            print("\nTree Structure:")
            tree.print_tree_structure()

        elif choice == "2":
            res = tree.preorder_traversal()
            print("\nPreorder Traversal (Root -> Left -> Right):")
            print("  Order of visitation: Visit node before its subtrees.")
            print(f"  Result: {' -> '.join(map(str, res)) if res else '[Empty Tree]'}")

        elif choice == "3":
            res = tree.inorder_traversal()
            print("\nInorder Traversal (Left -> Root -> Right):")
            print("  Order of visitation: Visit left subtree, current node, then right subtree.")
            print(f"  Result: {' -> '.join(map(str, res)) if res else '[Empty Tree]'}")

        elif choice == "4":
            res = tree.postorder_traversal()
            print("\nPostorder Traversal (Left -> Right -> Root):")
            print("  Order of visitation: Visit both subtrees before processing current node.")
            print(f"  Result: {' -> '.join(map(str, res)) if res else '[Empty Tree]'}")

        elif choice == "5":
            print("\nBuilding a 3-node custom tree (Root with Left and Right children):")
            r_val = input("Enter root value: ").strip()
            l_val = input("Enter left child value: ").strip()
            rg_val = input("Enter right child value: ").strip()
            new_root = TreeNode(r_val)
            if l_val:
                new_root.left = TreeNode(l_val)
            if rg_val:
                new_root.right = TreeNode(rg_val)
            tree = BinaryTree(new_root)
            print("Custom tree created successfully.")

        elif choice == "6":
            tree = build_sample_tree()
            print("Reset to standard sample 7-node tree.")

        elif choice == "7":
            run_tests()

        elif choice == "8":
            print("Exiting Recursive Traversals Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 8.")


if __name__ == "__main__":
    main()

