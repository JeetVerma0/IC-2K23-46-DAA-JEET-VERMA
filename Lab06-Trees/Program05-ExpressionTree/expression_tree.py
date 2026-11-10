#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 6: Trees
Program 5: Expression Tree (Construction from Postfix and Evaluation)

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
An Expression Tree is a specialized binary tree used by compilers, interpreters,
and database query planners to represent arithmetic, logical, and relational
expressions:
  - Leaves: Operands (e.g., numbers, constants, or variables).
  - Internal Nodes: Operators (e.g., +, -, *, /, ^).

POSTFIX CONSTRUCTION ALGORITHM:
Using an explicit LIFO stack of tree nodes:
  1. Tokenize the postfix expression into distinct tokens (operands and operators).
  2. For each token:
     - If the token is a numeric operand:
       Create an ExprNode(token) and push it onto the node stack.
     - If the token is an operator (+, -, *, /, ^):
       Pop two nodes from the stack:
         * First pop  -> right_child
         * Second pop -> left_child
       (If stack has fewer than 2 elements, the postfix expression is invalid).
       Create an ExprNode(operator), attach left_child and right_child, and
       push the operator node back onto the stack.
  3. When all tokens are processed, exactly ONE node must remain on the stack:
     this node is the Root of the Expression Tree.
     If the stack has 0 or >1 elements, the postfix expression is malformed.

RECURSIVE EVALUATION (WITHOUT PYTHON eval()):
  - Base case: If node is a leaf (operand), return its numeric float value.
  - Recursive step:
      left_val = evaluate(node.left)
      right_val = evaluate(node.right)
      apply operator (handle division by zero if operator is '/' and right_val == 0).

NOTATION GENERATION VIA TRAVERSALS:
  - Prefix Notation:  Preorder Traversal  (Root -> Left -> Right)
  - Infix Notation:   Inorder Traversal   (Left -> Root -> Right with parentheses)
  - Postfix Notation: Postorder Traversal (Left -> Right -> Root)

COMPLEXITY:
  - Construction: O(n) time, where n is the number of tokens.
  - Evaluation: O(n) time, visiting each node exactly once.
  - Auxiliary Space: O(n) for the node stack and tree hierarchy.
================================================================================
"""

import math
import sys
from typing import Any, List, Optional, Union


class ExprNode:
    """Represents a node in an arithmetic expression tree."""

    def __init__(self, value: str) -> None:
        self.value: str = value
        self.left: Optional["ExprNode"] = None
        self.right: Optional["ExprNode"] = None

    def is_leaf(self) -> bool:
        """Return True if node is an operand leaf (no children)."""
        return self.left is None and self.right is None

    def __repr__(self) -> str:
        return f"ExprNode('{self.value}')"


class ExpressionTree:
    """Expression Tree supporting construction, conversions, and evaluation."""

    OPERATORS = {"+", "-", "*", "/", "^"}

    def __init__(self, root: Optional[ExprNode] = None) -> None:
        self.root: Optional[ExprNode] = root

    @classmethod
    def from_postfix(cls, postfix_expr: str) -> "ExpressionTree":
        """
        Build an Expression Tree from a whitespace-separated postfix string.
        Raises ValueError on malformed or empty expressions.
        """
        tokens = postfix_expr.strip().split()
        if not tokens:
            raise ValueError("Cannot build expression tree from an empty expression.")

        stack: List[ExprNode] = []

        for token in tokens:
            if token in cls.OPERATORS:
                if len(stack) < 2:
                    raise ValueError(
                        f"Malformed Postfix Expression: Insufficient operands for operator '{token}'."
                    )
                right_child = stack.pop()
                left_child = stack.pop()

                op_node = ExprNode(token)
                op_node.left = left_child
                op_node.right = right_child
                stack.append(op_node)
            else:
                # Validate numeric operand
                try:
                    float(token)
                except ValueError:
                    raise ValueError(f"Invalid token '{token}': Must be a number or operator {cls.OPERATORS}.")
                operand_node = ExprNode(token)
                stack.append(operand_node)

        if len(stack) != 1:
            raise ValueError(
                f"Malformed Postfix Expression: Too many operands without corresponding operators (Remaining: {len(stack)})."
            )

        return cls(stack.pop())

    # -------------------------------------------------------------------------
    # Conversions to Notations
    # -------------------------------------------------------------------------
    def to_infix(self) -> str:
        """Generate fully-parenthesized infix notation."""
        if self.root is None:
            return ""
        return self._to_infix_recursive(self.root)

    def _to_infix_recursive(self, node: Optional[ExprNode]) -> str:
        if node is None:
            return ""
        if node.is_leaf():
            return node.value
        left_str = self._to_infix_recursive(node.left)
        right_str = self._to_infix_recursive(node.right)
        return f"({left_str} {node.value} {right_str})"

    def to_prefix(self) -> str:
        """Generate prefix notation (Preorder Traversal)."""
        tokens: List[str] = []
        self._preorder(self.root, tokens)
        return " ".join(tokens)

    def _preorder(self, node: Optional[ExprNode], tokens: List[str]) -> None:
        if node is not None:
            tokens.append(node.value)
            self._preorder(node.left, tokens)
            self._preorder(node.right, tokens)

    def to_postfix(self) -> str:
        """Generate postfix notation (Postorder Traversal)."""
        tokens: List[str] = []
        self._postorder(self.root, tokens)
        return " ".join(tokens)

    def _postorder(self, node: Optional[ExprNode], tokens: List[str]) -> None:
        if node is not None:
            self._postorder(node.left, tokens)
            self._postorder(node.right, tokens)
            tokens.append(node.value)

    # -------------------------------------------------------------------------
    # Recursive Evaluation (Without Python eval())
    # -------------------------------------------------------------------------
    def evaluate(self) -> float:
        """
        Evaluate the expression tree recursively.
        Returns: Numerical result as a float.
        Raises: ZeroDivisionError, ValueError.
        """
        if self.root is None:
            raise ValueError("Cannot evaluate an empty expression tree.")
        return self._evaluate_recursive(self.root)

    def _evaluate_recursive(self, node: ExprNode) -> float:
        if node.is_leaf():
            return float(node.value)

        assert node.left is not None and node.right is not None
        left_val = self._evaluate_recursive(node.left)
        right_val = self._evaluate_recursive(node.right)

        op = node.value
        if op == "+":
            return left_val + right_val
        elif op == "-":
            return left_val - right_val
        elif op == "*":
            return left_val * right_val
        elif op == "/":
            if right_val == 0.0:
                raise ZeroDivisionError("Math Error: Division by zero encountered during evaluation.")
            return left_val / right_val
        elif op == "^":
            return math.pow(left_val, right_val)
        else:
            raise ValueError(f"Unknown operator: {op}")

    # -------------------------------------------------------------------------
    # Visualization
    # -------------------------------------------------------------------------
    def print_tree(self) -> None:
        """Display ASCII hierarchical tree structure."""
        if self.root is None:
            print("  Tree is empty.")
            return
        self._print_ascii(self.root, prefix="", is_left=True, is_root=True)

    def _print_ascii(self, node: Optional[ExprNode], prefix: str, is_left: bool, is_root: bool = False) -> None:
        if node is None:
            return
        tag = "[Op]" if node.value in self.OPERATORS else "[Num]"
        label = f"{node.value} {tag}"
        if is_root:
            print(f"  [Root] {label}")
        else:
            branch = "|-- (L) " if is_left else "`-- (R) "
            print(f"  {prefix}{branch}{label}")

        extension = "|   " if is_left else "    "
        new_prefix = prefix + ("" if is_root else extension)
        if node.left or node.right:
            if node.left:
                self._print_ascii(node.left, new_prefix, is_left=True)
            if node.right:
                self._print_ascii(node.right, new_prefix, is_left=False)


def run_tests() -> None:
    """Automated unit verification test suite for Expression Tree."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Expression Tree")
    print("=" * 70)

    # Test 1: Standard expression: (10 + 20) * 3  -> Postfix: "10 20 + 3 *"
    t1 = ExpressionTree.from_postfix("10 20 + 3 *")
    assert t1.to_infix() == "((10 + 20) * 3)"
    assert t1.to_prefix() == "* + 10 20 3"
    assert t1.to_postfix() == "10 20 + 3 *"
    assert t1.evaluate() == 90.0
    print("[PASS] Test 1: Standard arithmetic '(10 + 20) * 3' verified.")

    # Test 2: Power and division: "5 3 + 2 ^ 4 /" -> ((5 + 3) ^ 2) / 4 = 64 / 4 = 16
    t2 = ExpressionTree.from_postfix("5 3 + 2 ^ 4 /")
    assert t2.to_infix() == "(((5 + 3) ^ 2) / 4)"
    assert t2.evaluate() == 16.0
    print("[PASS] Test 2: Exponentiation and division '((5 + 3) ^ 2) / 4' verified.")

    # Test 3: Floating point operands: "7.5 2.5 + 2 *" -> (7.5 + 2.5) * 2 = 20.0
    t3 = ExpressionTree.from_postfix("7.5 2.5 + 2 *")
    assert t3.evaluate() == 20.0
    print("[PASS] Test 3: Floating point operands verified.")

    # Test 4: Division by zero error handling
    t_div_zero = ExpressionTree.from_postfix("10 0 /")
    try:
        t_div_zero.evaluate()
        assert False, "Should raise ZeroDivisionError"
    except ZeroDivisionError:
        pass
    print("[PASS] Test 4: Division by zero caught cleanly.")

    # Test 5: Malformed postfix (insufficient operands)
    try:
        ExpressionTree.from_postfix("10 +")
        assert False, "Should raise ValueError on insufficient operands"
    except ValueError:
        pass
    print("[PASS] Test 5: Malformed expression (insufficient operands) caught.")

    # Test 6: Malformed postfix (excess operands left on stack)
    try:
        ExpressionTree.from_postfix("10 20 30 +")
        assert False, "Should raise ValueError on excess operands"
    except ValueError:
        pass
    print("[PASS] Test 6: Malformed expression (leftover operands) caught.")

    # Test 7: Invalid token
    try:
        ExpressionTree.from_postfix("10 foo +")
        assert False, "Should raise ValueError on unrecognized token"
    except ValueError:
        pass
    print("[PASS] Test 7: Invalid alphanumeric token rejected.")

    print("\nALL 7 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 55)
    print("            EXPRESSION TREE MENU")
    print("=" * 55)
    print(" 1. Build Expression Tree from Postfix")
    print(" 2. Display Fully Parenthesized Infix Notation")
    print(" 3. Display Prefix Notation (Preorder)")
    print(" 4. Display Postfix Notation (Postorder)")
    print(" 5. Evaluate Expression Tree (Without eval())")
    print(" 6. Display Expression Tree Structure (ASCII)")
    print(" 7. Load Sample: '5 3 + 2 ^ 4 /'")
    print(" 8. Run Automated Tests (--test)")
    print(" 9. Exit")
    print("=" * 55)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 6 — Expression Tree Demo")
    print("==========================================================")

    tree: Optional[ExpressionTree] = ExpressionTree.from_postfix("5 3 + 2 ^ 4 /")
    print("Initialized default sample tree from: '5 3 + 2 ^ 4 /'")

    while True:
        print_menu()
        choice = input("Enter choice (1-9): ").strip()

        if choice == "1":
            expr_str = input("Enter postfix expression (space-separated, e.g. '10 20 + 3 *'): ").strip()
            try:
                tree = ExpressionTree.from_postfix(expr_str)
                print("Expression tree constructed successfully!")
            except ValueError as err:
                print(f"Construction Error: {err}")

        elif choice == "2":
            if tree:
                print(f"Infix Notation:  {tree.to_infix()}")
            else:
                print("No tree currently built.")

        elif choice == "3":
            if tree:
                print(f"Prefix Notation: {tree.to_prefix()}")
            else:
                print("No tree currently built.")

        elif choice == "4":
            if tree:
                print(f"Postfix Notation: {tree.to_postfix()}")
            else:
                print("No tree currently built.")

        elif choice == "5":
            if tree:
                try:
                    res = tree.evaluate()
                    print(f"Evaluation Result: {res}")
                except (ZeroDivisionError, ValueError) as err:
                    print(f"Evaluation Error: {err}")
            else:
                print("No tree currently built.")

        elif choice == "6":
            if tree:
                print("\nExpression Tree Hierarchy:")
                tree.print_tree()
            else:
                print("No tree currently built.")

        elif choice == "7":
            tree = ExpressionTree.from_postfix("5 3 + 2 ^ 4 /")
            print("Loaded sample: '5 3 + 2 ^ 4 /' -> ((5 + 3) ^ 2) / 4 = 16.0")

        elif choice == "8":
            run_tests()

        elif choice == "9":
            print("Exiting Expression Tree Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 9.")


if __name__ == "__main__":
    main()

