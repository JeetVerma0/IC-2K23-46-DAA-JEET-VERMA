#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 6: Trees
Program 4: Self-Balancing AVL Tree (Adelson-Velsky and Landis)

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
An AVL tree (named after Georgy Adelson-Velsky and Evgenii Landis, 1962) is a
self-balancing Binary Search Tree. In a regular BST, inserting sorted or nearly
sorted data degenerates the tree into a linked list of height O(n), causing
search, insertion, and deletion to degrade to linear time O(n).

AVL INVARIANT:
For every node in an AVL tree, the heights of its left and right subtrees
differ by AT MOST 1:
    Balance Factor (BF) = Height(Left Subtree) - Height(Right Subtree)
    For all valid nodes: BF in {-1, 0, 1}

If an insertion or deletion causes |BF| > 1, the node becomes unbalanced and
one of four rotations is applied to restore equilibrium.

THE FOUR ROTATION CASES:
1. Left-Left (LL) Heavy:
   - Condition: BF(Node) > 1 and BF(Left Child) >= 0
   - Action: Single Right Rotation on Node
2. Right-Right (RR) Heavy:
   - Condition: BF(Node) < -1 and BF(Right Child) <= 0
   - Action: Single Left Rotation on Node
3. Left-Right (LR) Heavy:
   - Condition: BF(Node) > 1 and BF(Left Child) < 0
   - Action: Left Rotation on Left Child, then Right Rotation on Node
4. Right-Left (RL) Heavy:
   - Condition: BF(Node) < -1 and BF(Right Child) > 0
   - Action: Right Rotation on Right Child, then Left Rotation on Node

WHY AVL TREES GUARANTEE LOGARITHMIC HEIGHT:
The minimum number of nodes N(h) in an AVL tree of height h satisfies the
recurrence: N(h) = 1 + N(h-1) + N(h-2), which is Fibonacci-like.
Solving this recurrence yields:
    Height h < 1.44 * log2(n + 2) - 0.328 = O(log n)
Because height is strictly bounded by O(log n), search, insert, and delete
are GUARANTEED to terminate in O(log n) time in both average and worst cases!
================================================================================
"""

import sys
from typing import Any, List, Optional, Tuple


class AVLNode:
    """Represents a node in a self-balancing AVL tree."""

    def __init__(self, key: Any) -> None:
        self.key: Any = key
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height: int = 1  # 1-based height: leaf has height 1

    def __repr__(self) -> str:
        return f"AVLNode(key={self.key}, h={self.height})"


class AVLTree:
    """Self-balancing AVL tree implementation supporting rotations and balancing."""

    def __init__(self) -> None:
        self.root: Optional[AVLNode] = None
        self.last_rotation: str = "None"

    # -------------------------------------------------------------------------
    # Height and Balance Factor Utilities
    # -------------------------------------------------------------------------
    def get_height(self, node: Optional[AVLNode]) -> int:
        """Return height of node, or 0 if node is None."""
        if node is None:
            return 0
        return node.height

    def get_balance(self, node: Optional[AVLNode]) -> int:
        """Return Balance Factor: Height(Left) - Height(Right)."""
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def _update_height(self, node: AVLNode) -> None:
        """Recalculate height of node from its children."""
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    # -------------------------------------------------------------------------
    # Rotations
    # -------------------------------------------------------------------------
    def _right_rotate(self, y: AVLNode) -> AVLNode:
        """
        Perform a Right Rotation on node y.

              y                               x
             / \\                            / \\
            x   T3   -- Right Rotate ->    T1   y
           / \\                                 / \\
          T1  T2                              T2  T3
        """
        x = y.left
        assert x is not None
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights (y first, then x)
        self._update_height(y)
        self._update_height(x)

        return x

    def _left_rotate(self, x: AVLNode) -> AVLNode:
        """
        Perform a Left Rotation on node x.

            x                                y
           / \\                              / \\
          T1  y      -- Left Rotate ->     x   T3
             / \\                          / \\
            T2  T3                       T1  T2
        """
        y = x.right
        assert y is not None
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights (x first, then y)
        self._update_height(x)
        self._update_height(y)

        return y

    # -------------------------------------------------------------------------
    # Insertion with Automatic Balancing
    # -------------------------------------------------------------------------
    def insert(self, key: Any) -> None:
        """Insert key into AVL tree and restore balance."""
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, node: Optional[AVLNode], key: Any) -> AVLNode:
        # Step 1: Standard BST insertion
        if node is None:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert_recursive(node.left, key)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key)
        else:
            raise ValueError(f"Duplicate key '{key}' rejected: AVL Tree requires unique keys.")

        # Step 2: Update height of this ancestor node
        self._update_height(node)

        # Step 3: Get balance factor to check if node became unbalanced
        balance = self.get_balance(node)

        # Step 4: Rebalance if unbalanced (|BF| > 1)
        # Case 1: Left-Left (LL) -> Single Right Rotation
        if balance > 1 and key < node.left.key:
            self.last_rotation = f"Right Rotation (LL case on node {node.key})"
            return self._right_rotate(node)

        # Case 2: Right-Right (RR) -> Single Left Rotation
        if balance < -1 and key > node.right.key:
            self.last_rotation = f"Left Rotation (RR case on node {node.key})"
            return self._left_rotate(node)

        # Case 3: Left-Right (LR) -> Left Rotate left child, then Right Rotate node
        if balance > 1 and key > node.left.key:
            self.last_rotation = f"Left-Right Rotation (LR case on node {node.key})"
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Case 4: Right-Left (RL) -> Right Rotate right child, then Left Rotate node
        if balance < -1 and key < node.right.key:
            self.last_rotation = f"Right-Left Rotation (RL case on node {node.key})"
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    # -------------------------------------------------------------------------
    # Deletion with Automatic Balancing
    # -------------------------------------------------------------------------
    def delete(self, key: Any) -> None:
        """Delete key from AVL tree and restore balance."""
        if not self.search(key):
            raise KeyError(f"Key '{key}' not found in AVL tree.")
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node: Optional[AVLNode], key: Any) -> Optional[AVLNode]:
        # Step 1: Standard BST deletion
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Node found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children: get inorder successor (min in right subtree)
            successor = self._find_min_node(node.right)
            node.key = successor.key
            node.right = self._delete_recursive(node.right, successor.key)

        if node is None:
            return None

        # Step 2: Update height
        self._update_height(node)

        # Step 3: Check balance factor
        balance = self.get_balance(node)

        # Step 4: Rebalance if unbalanced
        # Case 1: Left-Left (LL)
        if balance > 1 and self.get_balance(node.left) >= 0:
            self.last_rotation = f"Right Rotation (LL on node {node.key})"
            return self._right_rotate(node)

        # Case 2: Left-Right (LR)
        if balance > 1 and self.get_balance(node.left) < 0:
            self.last_rotation = f"Left-Right Rotation (LR on node {node.key})"
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Case 3: Right-Right (RR)
        if balance < -1 and self.get_balance(node.right) <= 0:
            self.last_rotation = f"Left Rotation (RR on node {node.key})"
            return self._left_rotate(node)

        # Case 4: Right-Left (RL)
        if balance < -1 and self.get_balance(node.right) > 0:
            self.last_rotation = f"Right-Left Rotation (RL on node {node.key})"
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _find_min_node(self, node: AVLNode) -> AVLNode:
        curr = node
        while curr.left is not None:
            curr = curr.left
        return curr

    # -------------------------------------------------------------------------
    # Search & Traversal
    # -------------------------------------------------------------------------
    def search(self, key: Any) -> bool:
        """Search for key in AVL tree."""
        curr = self.root
        while curr is not None:
            if key == curr.key:
                return True
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return False

    def inorder_traversal(self) -> List[Any]:
        """Return keys in sorted ascending order."""
        result: List[Any] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[AVLNode], result: List[Any]) -> None:
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------
    def validate_avl(self) -> Tuple[bool, str]:
        """
        Validate both BST ordering property and AVL balance condition (|BF| <= 1).
        """
        is_bst = self._validate_bst(self.root, float("-inf"), float("inf"))
        if not is_bst:
            return False, "Violation: Tree does not satisfy BST ordering."

        is_balanced, bf_violation = self._validate_balance(self.root)
        if not is_balanced:
            return False, f"Violation: AVL balance factor invalid ({bf_violation})."

        return True, "Tree is a strictly balanced, valid AVL Tree."

    def _validate_bst(self, node: Optional[AVLNode], min_val: float, max_val: float) -> bool:
        if node is None:
            return True
        if not (min_val < node.key < max_val):
            return False
        return self._validate_bst(node.left, min_val, node.key) and self._validate_bst(
            node.right, node.key, max_val
        )

    def _validate_balance(self, node: Optional[AVLNode]) -> Tuple[bool, str]:
        if node is None:
            return True, ""
        bf = self.get_balance(node)
        if abs(bf) > 1:
            return False, f"Node {node.key} has Balance Factor {bf}"
        left_ok, left_msg = self._validate_balance(node.left)
        if not left_ok:
            return False, left_msg
        right_ok, right_msg = self._validate_balance(node.right)
        if not right_ok:
            return False, right_msg
        return True, ""

    # -------------------------------------------------------------------------
    # Visualization
    # -------------------------------------------------------------------------
    def print_tree(self) -> None:
        """Display ASCII tree structure with node heights and balance factors."""
        if self.root is None:
            print("  AVL Tree is empty.")
            return
        self._print_ascii(self.root, prefix="", is_left=True, is_root=True)

    def _print_ascii(self, node: Optional[AVLNode], prefix: str, is_left: bool, is_root: bool = False) -> None:
        if node is None:
            return
        bf = self.get_balance(node)
        info = f"{node.key} (h={node.height}, BF={bf:+d})"
        if is_root:
            print(f"  [Root] {info}")
        else:
            branch = "|-- (L) " if is_left else "`-- (R) "
            print(f"  {prefix}{branch}{info}")

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
    """Automated unit verification test suite for AVL Tree and all 4 rotation cases."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Self-Balancing AVL Tree")
    print("=" * 70)

    # Test 1: Case 1 — Left-Left (LL) Rotation Demonstration
    # Insert sequence: 30, 20, 10 -> Root becomes 20, children 10 and 30
    avl_ll = AVLTree()
    avl_ll.insert(30)
    avl_ll.insert(20)
    avl_ll.insert(10)
    assert avl_ll.root.key == 20
    assert avl_ll.root.left.key == 10
    assert avl_ll.root.right.key == 30
    assert avl_ll.validate_avl()[0] is True
    print("[PASS] Test 1: Case 1 (LL Rotation -> Single Right Rotate) verified.")

    # Test 2: Case 2 — Right-Right (RR) Rotation Demonstration
    # Insert sequence: 10, 20, 30 -> Root becomes 20, children 10 and 30
    avl_rr = AVLTree()
    avl_rr.insert(10)
    avl_rr.insert(20)
    avl_rr.insert(30)
    assert avl_rr.root.key == 20
    assert avl_rr.root.left.key == 10
    assert avl_rr.root.right.key == 30
    assert avl_rr.validate_avl()[0] is True
    print("[PASS] Test 2: Case 2 (RR Rotation -> Single Left Rotate) verified.")

    # Test 3: Case 3 — Left-Right (LR) Rotation Demonstration
    # Insert sequence: 30, 10, 20 -> Root becomes 20, children 10 and 30
    avl_lr = AVLTree()
    avl_lr.insert(30)
    avl_lr.insert(10)
    avl_lr.insert(20)
    assert avl_lr.root.key == 20
    assert avl_lr.root.left.key == 10
    assert avl_lr.root.right.key == 30
    assert avl_lr.validate_avl()[0] is True
    print("[PASS] Test 3: Case 3 (LR Rotation -> Double Rotation Left-Right) verified.")

    # Test 4: Case 4 — Right-Left (RL) Rotation Demonstration
    # Insert sequence: 10, 30, 20 -> Root becomes 20, children 10 and 30
    avl_rl = AVLTree()
    avl_rl.insert(10)
    avl_rl.insert(30)
    avl_rl.insert(20)
    assert avl_rl.root.key == 20
    assert avl_rl.root.left.key == 10
    assert avl_rl.root.right.key == 30
    assert avl_rl.validate_avl()[0] is True
    print("[PASS] Test 4: Case 4 (RL Rotation -> Double Rotation Right-Left) verified.")

    # Test 5: Comprehensive insertion, deletion & AVL balance invariant
    avl = AVLTree()
    dataset = [40, 20, 10, 25, 30, 22, 50, 60, 70, 65]
    for x in dataset:
        avl.insert(x)
        valid, msg = avl.validate_avl()
        assert valid is True, f"AVL validation failed during insertion of {x}: {msg}"

    assert avl.inorder_traversal() == sorted(dataset)
    assert avl.search(25) is True
    assert avl.search(999) is False
    print("[PASS] Test 5: Multi-element insertion & continuous balance verified.")

    # Test 6: Deletion with rebalancing
    # Delete multiple nodes triggers deletions across leaf, single child, and 2-child cases
    for x in [10, 20, 40]:
        avl.delete(x)
        valid, msg = avl.validate_avl()
        assert valid is True, f"AVL validation failed after deleting {x}: {msg}"
        assert avl.search(x) is False

    remaining_expected = sorted([25, 30, 22, 50, 60, 70, 65])
    assert avl.inorder_traversal() == remaining_expected
    print("[PASS] Test 6: Deletion with automatic rebalancing verified.")

    print("\nALL 6 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 55)
    print("           SELF-BALANCING AVL TREE MENU")
    print("=" * 55)
    print(" 1. Insert a Key (With Automatic Balancing)")
    print(" 2. Delete a Key (With Automatic Balancing)")
    print(" 3. Search for a Key")
    print(" 4. Display Inorder Traversal (Sorted Keys)")
    print(" 5. Display AVL Tree Structure (Heights & Balance Factors)")
    print(" 6. Validate AVL Balance and BST Ordering")
    print(" 7. Demonstrate 4 Rotation Cases (LL, RR, LR, RL)")
    print(" 8. Run Automated Tests (--test)")
    print(" 9. Exit")
    print("=" * 55)


def demonstrate_rotations() -> None:
    """Run educational demonstration of all four rotation cases."""
    print("\n" + "-" * 60)
    print("DEMONSTRATING ALL FOUR AVL ROTATION CASES:")
    print("-" * 60)

    # 1. LL Case
    print("\n1. Case 1: Left-Left (LL) Case -> Single Right Rotation")
    t1 = AVLTree()
    for k in [30, 20, 10]:
        t1.insert(k)
    t1.print_tree()
    print("  Result: Node 20 rotated to Root; 10 and 30 are balanced children.")

    # 2. RR Case
    print("\n2. Case 2: Right-Right (RR) Case -> Single Left Rotation")
    t2 = AVLTree()
    for k in [10, 20, 30]:
        t2.insert(k)
    t2.print_tree()
    print("  Result: Node 20 rotated to Root; 10 and 30 are balanced children.")

    # 3. LR Case
    print("\n3. Case 3: Left-Right (LR) Case -> Double Rotation (Left then Right)")
    t3 = AVLTree()
    for k in [30, 10, 20]:
        t3.insert(k)
    t3.print_tree()
    print("  Result: Node 20 promoted to Root through LR rotation.")

    # 4. RL Case
    print("\n4. Case 4: Right-Left (RL) Case -> Double Rotation (Right then Left)")
    t4 = AVLTree()
    for k in [10, 30, 20]:
        t4.insert(k)
    t4.print_tree()
    print("  Result: Node 20 promoted to Root through RL rotation.")
    print("-" * 60)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 6 — Self-Balancing AVL Tree Demo")
    print("==========================================================")

    avl = AVLTree()

    while True:
        print_menu()
        choice = input("Enter choice (1-9): ").strip()

        if choice == "1":
            val_str = input("Enter integer key to insert: ").strip()
            try:
                val = int(val_str)
                avl.insert(val)
                print(f"Key {val} inserted. Last rotation: {avl.last_rotation}")
            except ValueError as err:
                print(f"Insertion Error: {err}")

        elif choice == "2":
            val_str = input("Enter integer key to delete: ").strip()
            try:
                val = int(val_str)
                avl.delete(val)
                print(f"Key {val} deleted. Last rotation: {avl.last_rotation}")
            except (ValueError, KeyError) as err:
                print(f"Deletion Error: {err}")

        elif choice == "3":
            val_str = input("Enter key to search: ").strip()
            try:
                val = int(val_str)
                found = avl.search(val)
                print(f"Key {val} {'FOUND' if found else 'NOT FOUND'} in AVL tree.")
            except ValueError:
                print("Invalid integer input!")

        elif choice == "4":
            keys = avl.inorder_traversal()
            print(f"Inorder Traversal: {' -> '.join(map(str, keys)) if keys else '[Empty AVL Tree]'}")

        elif choice == "5":
            print("\nAVL Tree Structure:")
            avl.print_tree()

        elif choice == "6":
            valid, msg = avl.validate_avl()
            print(f"Validation Status: {'VALID' if valid else 'INVALID'}")
            print(f"Details: {msg}")

        elif choice == "7":
            demonstrate_rotations()

        elif choice == "8":
            run_tests()

        elif choice == "9":
            print("Exiting AVL Tree Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 9.")


if __name__ == "__main__":
    main()

