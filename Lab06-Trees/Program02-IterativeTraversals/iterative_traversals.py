#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 6: Trees
Program 2: Binary Tree — Iterative Traversals (Preorder, Inorder, Postorder)

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
In recursive tree traversals, the operating system manages a hidden Call Stack
of activation records. Each recursive step pushes the current function state,
local variables, and return address onto the runtime call stack.

In ITERATIVE traversals, we eliminate the runtime recursion overhead by
managing our own explicit LIFO Stack data structure. This prevents call stack
overflow (Python's recursion limit, default 1000 frames) on deeply skewed trees
and provides full control over memory allocation and state transitions.

HOW STACKS REPLACE RECURSIVE ACTIVATION RECORDS:

1. Iterative Preorder (Root -> Left -> Right):
   - A single stack holds nodes awaiting visitation.
   - Pop node and visit immediately (Root).
   - Push RIGHT child first, then LEFT child (because LIFO pops Left first).

2. Iterative Inorder (Left -> Root -> Right):
   - Traverse down the left spine, pushing all ancestor nodes onto the stack.
   - When leftmost None is reached, pop the top node from the stack (Root of subproblem),
     visit it, and transition `curr` to its right child.

3. Iterative Postorder (Left -> Right -> Root):
   - Postorder requires visiting both children before visiting the parent.
   - Using the Two-Stack Algorithm:
     * Stack 1 simulates a modified preorder traversal (Root -> Right -> Left).
     * Popping from Stack 1 pushes nodes into Stack 2.
     * When Stack 1 is exhausted, popping Stack 2 reverses the order, yielding
       the exact postorder sequence: Left -> Right -> Root!

COMPLEXITIES:
  - Time Complexity: O(n) for all three iterative methods.
  - Auxiliary Space: O(h) for Preorder and Inorder stack depth, O(n) for Postorder.
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


class IterativeBinaryTree:
    """Provides non-recursive, stack-based tree traversals."""

    def __init__(self, root: Optional[TreeNode] = None) -> None:
        self.root: Optional[TreeNode] = root

    # -------------------------------------------------------------------------
    # 1. Iterative Preorder Traversal (Root -> Left -> Right)
    # -------------------------------------------------------------------------
    def preorder_iterative(self) -> List[Any]:
        """
        Iterative preorder traversal using an explicit LIFO stack.

        Algorithm:
          1. If root is None, return [].
          2. Initialize stack with [root].
          3. While stack is not empty:
             a. Pop node from stack; append node.data to result.
             b. If node.right exists, push node.right onto stack.
             c. If node.left exists, push node.left onto stack.
          4. Return result.
        """
        if self.root is None:
            return []

        result: List[Any] = []
        stack: List[TreeNode] = [self.root]

        while len(stack) > 0:
            node = stack.pop()
            result.append(node.data)

            # Push right first so that left is popped and visited first
            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)

        return result

    # -------------------------------------------------------------------------
    # 2. Iterative Inorder Traversal (Left -> Root -> Right)
    # -------------------------------------------------------------------------
    def inorder_iterative(self) -> List[Any]:
        """
        Iterative inorder traversal using an explicit LIFO stack.

        Algorithm:
          1. Initialize empty stack; curr = root.
          2. While curr is not None or stack is not empty:
             a. While curr is not None:
                  Push curr onto stack; curr = curr.left.
             b. Pop node from stack; append node.data to result.
             c. Set curr = node.right.
          3. Return result.
        """
        result: List[Any] = []
        stack: List[TreeNode] = []
        curr: Optional[TreeNode] = self.root

        while curr is not None or len(stack) > 0:
            # Reach the leftmost node of current subtree
            while curr is not None:
                stack.append(curr)
                curr = curr.left

            # curr is now None, backtrack by popping top node
            node = stack.pop()
            result.append(node.data)

            # We have visited the node and its left subtree; now visit right subtree
            curr = node.right

        return result

    # -------------------------------------------------------------------------
    # 3. Iterative Postorder Traversal (Left -> Right -> Root)
    # -------------------------------------------------------------------------
    def postorder_iterative(self) -> List[Any]:
        """
        Iterative postorder traversal using the Two-Stack Algorithm.

        Algorithm:
          1. If root is None, return [].
          2. Push root to stack1.
          3. While stack1 is not empty:
             a. Pop node from stack1 and push into stack2.
             b. If node.left exists, push node.left to stack1.
             c. If node.right exists, push node.right to stack1.
          4. While stack2 is not empty:
             Pop node from stack2 and append node.data to result.
          5. Return result.
        """
        if self.root is None:
            return []

        result: List[Any] = []
        stack1: List[TreeNode] = [self.root]
        stack2: List[TreeNode] = []

        while len(stack1) > 0:
            node = stack1.pop()
            stack2.append(node)

            # Push left child, then right child to stack1
            if node.left is not None:
                stack1.append(node.left)
            if node.right is not None:
                stack1.append(node.right)

        # Pop all items from stack2 to obtain Postorder sequence
        while len(stack2) > 0:
            node = stack2.pop()
            result.append(node.data)

        return result

    # -------------------------------------------------------------------------
    # Tree Visualization
    # -------------------------------------------------------------------------
    def print_tree_structure(self) -> None:
        """Display ASCII hierarchical tree structure."""
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


def build_sample_tree() -> IterativeBinaryTree:
    """
    Constructs the exact same 7-node reference tree as Program 1:

                 1
               /   \\
              2     3
             / \\   / \\
            4   5 6   7
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)

    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    return IterativeBinaryTree(root)


def run_tests() -> None:
    """Automated unit verification test suite for iterative tree traversals."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Binary Tree Iterative Traversals")
    print("=" * 70)

    # Test 1: Empty tree
    empty_tree = IterativeBinaryTree()
    assert empty_tree.preorder_iterative() == []
    assert empty_tree.inorder_iterative() == []
    assert empty_tree.postorder_iterative() == []
    print("[PASS] Test 1: Empty tree handled correctly.")

    # Test 2: Single node tree
    single_node_tree = IterativeBinaryTree(TreeNode(42))
    assert single_node_tree.preorder_iterative() == [42]
    assert single_node_tree.inorder_iterative() == [42]
    assert single_node_tree.postorder_iterative() == [42]
    print("[PASS] Test 2: Single-node tree handled correctly.")

    # Test 3: Match results against identical sample tree
    tree = build_sample_tree()
    pre_res = tree.preorder_iterative()
    in_res = tree.inorder_iterative()
    post_res = tree.postorder_iterative()

    expected_pre = [1, 2, 4, 5, 3, 6, 7]
    expected_in = [4, 2, 5, 1, 6, 3, 7]
    expected_post = [4, 5, 2, 6, 7, 3, 1]

    assert pre_res == expected_pre, f"Preorder mismatch: got {pre_res}, expected {expected_pre}"
    assert in_res == expected_in, f"Inorder mismatch: got {in_res}, expected {expected_in}"
    assert post_res == expected_post, f"Postorder mismatch: got {post_res}, expected {expected_post}"

    print(f"[PASS] Test 3: Iterative Preorder matches reference  -> {pre_res}")
    print(f"[PASS] Test 4: Iterative Inorder matches reference   -> {in_res}")
    print(f"[PASS] Test 5: Iterative Postorder matches reference -> {post_res}")

    print("\nALL 5 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 55)
    print("     BINARY TREE ITERATIVE TRAVERSALS MENU")
    print("        (Explicit Stack Implementations)")
    print("=" * 55)
    print(" 1. Display Current Tree Structure (ASCII)")
    print(" 2. Perform Iterative Preorder Traversal")
    print(" 3. Perform Iterative Inorder Traversal")
    print(" 4. Perform Iterative Postorder Traversal")
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
    print("  IC-307D: Unit 6 — Binary Tree Iterative Traversals")
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
            res = tree.preorder_iterative()
            print("\nIterative Preorder Traversal (Root -> Left -> Right):")
            print("  Mechanism: Single stack; pop node, push right child, then left child.")
            print(f"  Result: {' -> '.join(map(str, res)) if res else '[Empty Tree]'}")

        elif choice == "3":
            res = tree.inorder_iterative()
            print("\nIterative Inorder Traversal (Left -> Root -> Right):")
            print("  Mechanism: Stack records path; traverse left spine, pop and visit, go right.")
            print(f"  Result: {' -> '.join(map(str, res)) if res else '[Empty Tree]'}")

        elif choice == "4":
            res = tree.postorder_iterative()
            print("\nIterative Postorder Traversal (Left -> Right -> Root):")
            print("  Mechanism: Two-stack algorithm inverts modified preorder sequence.")
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
            tree = IterativeBinaryTree(new_root)
            print("Custom tree created successfully.")

        elif choice == "6":
            tree = build_sample_tree()
            print("Reset to standard sample 7-node tree.")

        elif choice == "7":
            run_tests()

        elif choice == "8":
            print("Exiting Iterative Traversals Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 8.")


if __name__ == "__main__":
    main()

