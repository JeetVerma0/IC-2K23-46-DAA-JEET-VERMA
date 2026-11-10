"""
Program 05: Postfix Expression Evaluation Using Stack
Course: IC-307D Data Structures and Algorithms Lab
Unit 4: Stacks (CO1)

This program evaluates Postfix (Reverse Polish) arithmetic expressions using a stack:
- Algorithm:
    1. Parse the space-delimited postfix expression into tokens.
    2. Traverse tokens from left to right:
       - If token is an operand (integer, float, or negative number):
         Push its numeric value onto the operand stack.
       - If token is an operator:
         Pop the top two operands:
           right_operand = pop()
           left_operand = pop()
         Compute: result = left_operand (op) right_operand
         Push result back onto stack.
    3. At the end, the stack must contain exactly one value: the final result.
- Supported Operators:
    '+', '-', '*', '/', '//' (floor division), '%' (modulo), '^' (exponentiation).
- Robust Error Handling:
    - Division / Modulo by Zero detection (ZeroDivisionError).
    - Insufficient operands on stack (ValueError).
    - Excess operands remaining on stack at end (ValueError).
    - Invalid tokens (ValueError).
- Test suite (--test flag) and interactive CLI.
"""

import math
import sys
from typing import List, Union


OPERATORS = {"+", "-", "*", "/", "//", "%", "^"}


def is_number(token: str) -> bool:
    """Checks whether a token represents a valid integer or floating-point number."""
    try:
        float(token)
        return True
    except ValueError:
        return False


def parse_number(token: str) -> Union[int, float]:
    """Parses a string into an int if whole, or float otherwise."""
    f = float(token)
    if f.is_integer():
        return int(f)
    return f


def apply_operator(op: str, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Applies the binary operator 'op' to operands 'a' (left) and 'b' (right):
    result = a (op) b
    """
    if op == "+":
        res = a + b
    elif op == "-":
        res = a - b
    elif op == "*":
        res = a * b
    elif op == "/":
        if b == 0:
            raise ZeroDivisionError("Division by zero in '/' operation.")
        res = a / b
    elif op == "//":
        if b == 0:
            raise ZeroDivisionError("Division by zero in '//' floor division.")
        res = a // b
    elif op == "%":
        if b == 0:
            raise ZeroDivisionError("Modulo by zero in '%' operation.")
        res = a % b
    elif op == "^":
        # Handle fractional powers of negative numbers if complex
        try:
            res = a ** b
        except ValueError as err:
            raise ValueError(f"Invalid exponentiation {a} ^ {b}: {err}")
    else:
        raise ValueError(f"Unsupported operator: '{op}'")

    if isinstance(res, float) and res.is_integer():
        return int(res)
    return res


def evaluate_postfix(expression: str) -> Union[int, float]:
    """
    Evaluates a postfix expression string. Tokens should be space-delimited.

    Time Complexity: O(n) where n is token count.
    Auxiliary Space Complexity: O(n) for the operand stack.
    """
    tokens = expression.strip().split()
    if not tokens:
        raise ValueError("Expression is empty.")

    stack: List[Union[int, float]] = []

    for token in tokens:
        # 1. Number operand
        if is_number(token):
            stack.append(parse_number(token))

        # 2. Operator
        elif token in OPERATORS:
            if len(stack) < 2:
                raise ValueError(
                    f"Malformed postfix expression: Insufficient operands for operator '{token}'."
                )
            b = stack.pop()  # Right operand
            a = stack.pop()  # Left operand

            result = apply_operator(token, a, b)
            stack.append(result)

        else:
            raise ValueError(f"Invalid token encountered: '{token}'")

    if len(stack) != 1:
        raise ValueError(
            f"Malformed postfix expression: Too many operands without operators (Stack: {stack})."
        )

    return stack[0]


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Runs comprehensive tests for postfix expression evaluation."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Postfix Evaluation (Program 05)")
    print("=" * 65)

    test_cases = [
        # Basic arithmetic
        ("10 20 +", 30),
        ("50 20 -", 30),
        ("6 7 *", 42),
        ("100 4 /", 25),
        ("17 5 //", 3),
        ("17 5 %", 2),
        ("2 3 ^", 8),

        # Multi-operation sequences
        ("10 20 + 3 *", 90),           # (10 + 20) * 3
        ("10 20 3 * +", 70),           # 10 + (20 * 3)
        ("2 3 2 ^ ^", 512),            # 2 ^ (3 ^ 2) = 2 ^ 9 = 512

        # Negative and floating-point operands
        ("-5 3 +", -2),
        ("10 -2 *", -20),
        ("2.5 4.0 *", 10),
        ("7.5 2.5 -", 5),
        ("15 -3 //", -5),

        # Complex expression: ((15 / (7 - (1 + 1))) * 3) - (2 + (1 + 1)) = 5
        ("15 7 1 1 + - / 3 * 2 1 1 + + -", 5)
    ]

    for expr, expected in test_cases:
        actual = evaluate_postfix(expr)
        assert actual == expected, f"Failed for '{expr}': got {actual}, expected {expected}"
        print(f"  [Passed] '{expr}' = {actual}")

    # Error handling tests
    print("\n  Testing Error Detection:")
    # Division by zero
    try:
        evaluate_postfix("10 0 /")
        assert False, "Should raise ZeroDivisionError"
    except ZeroDivisionError as err:
        print(f"  [Passed] Caught division by zero: {err}")

    try:
        evaluate_postfix("10 0 //")
        assert False, "Should raise ZeroDivisionError"
    except ZeroDivisionError as err:
        print(f"  [Passed] Caught floor division by zero: {err}")

    try:
        evaluate_postfix("10 0 %")
        assert False, "Should raise ZeroDivisionError"
    except ZeroDivisionError as err:
        print(f"  [Passed] Caught modulo by zero: {err}")

    # Insufficient operands
    try:
        evaluate_postfix("5 +")
        assert False, "Should raise ValueError for insufficient operands"
    except ValueError as err:
        print(f"  [Passed] Caught insufficient operands: {err}")

    # Excess operands
    try:
        evaluate_postfix("5 4 3 +")
        assert False, "Should raise ValueError for excess operands"
    except ValueError as err:
        print(f"  [Passed] Caught excess operands: {err}")

    print("\nAll Program 05 automated tests PASSED successfully!")


def main() -> None:
    """Interactive command-line evaluator."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("\n==================================================")
    print("      POSTFIX EXPRESSION EVALUATOR (Program 05)")
    print("==================================================")
    print("Enter space-separated postfix tokens (e.g., '10 20 + 3 *')")
    print("Operators supported: +, -, *, /, //, %, ^")
    print("Type 'exit' to quit.\n")

    while True:
        expr = input("Enter Postfix Expression: ").strip()
        if expr.lower() in ("exit", "quit"):
            print("Exiting evaluator. Goodbye!")
            break

        if not expr:
            continue

        try:
            val = evaluate_postfix(expr)
            print(f"  Result = {val}\n")
        except (ValueError, ZeroDivisionError) as err:
            print(f"  Evaluation Error: {err}\n")


if __name__ == "__main__":
    main()

