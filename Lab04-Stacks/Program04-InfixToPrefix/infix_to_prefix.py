"""
Program 04: Infix to Prefix Expression Conversion
Course: IC-307D Data Structures and Algorithms Lab
Unit 4: Stacks (CO1)

This program converts Infix expressions to Prefix (Polish) notation using
stack-based algorithms:
- Conversion Logic (Reversal & Modified Shunting-Yard):
    1. Tokenize the infix expression.
    2. Reverse the token stream.
    3. Swap parentheses: '(' becomes ')' and ')' becomes '('.
    4. Process reversed tokens using a modified Shunting-Yard algorithm:
       - Because tokens are evaluated in reverse, operator associativity is inverted:
         * Originally Left-Associative operators (+, -, *, /, //, %) pop operators
           with strictly GREATER precedence (prec1 < prec2).
         * Originally Right-Associative operators (^) pop operators with GREATER OR
           EQUAL precedence (prec1 <= prec2).
    5. Reverse the resulting output tokens to achieve the correct Prefix expression.
- Supported Operators:
    - Exponentiation: '^' (Precedence 4, Right-Associative)
    - Multiplicative: '*', '/', '//', '%' (Precedence 3, Left-Associative)
    - Additive: '+', '-' (Precedence 2, Left-Associative)
- Supports multi-digit numbers and variable names.
- Comprehensive test suite and interactive CLI (--test flag).
"""

import sys
from typing import List


# Precedence and Associativity Table
# associativity: True for Left-Associative, False for Right-Associative
OPERATOR_TABLE = {
    "^":  (4, False),  # Right-associative exponentiation
    "*":  (3, True),   # Left-associative multiplication
    "/":  (3, True),   # Left-associative division
    "//": (3, True),   # Left-associative floor division
    "%":  (3, True),   # Left-associative modulus
    "+":  (2, True),   # Left-associative addition
    "-":  (2, True),   # Left-associative subtraction
}


def tokenize(expression: str) -> List[str]:
    """
    Tokenizes an infix arithmetic string into distinct operator, parenthesis,
    and operand tokens.
    """
    tokens: List[str] = []
    i = 0
    n = len(expression)

    while i < n:
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        # Two-character floor division '//'
        if char == "/" and i + 1 < n and expression[i + 1] == "/":
            tokens.append("//")
            i += 2
            continue

        # Single-character operators and parentheses
        if char in ("+", "-", "*", "/", "%", "^", "(", ")"):
            tokens.append(char)
            i += 1
            continue

        # Multi-digit numbers and alphanumeric variable identifiers
        if char.isalnum() or char == ".":
            start = i
            while i < n and (expression[i].isalnum() or expression[i] == "."):
                i += 1
            tokens.append(expression[start:i])
            continue

        raise ValueError(f"Unrecognized character in expression: '{char}' at index {i}")

    return tokens


def infix_to_prefix(expression: str) -> str:
    """
    Converts an infix expression string into a space-delimited prefix expression string.

    Time Complexity: O(n)
    Auxiliary Space Complexity: O(n)
    """
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("Expression is empty.")

    # 1. Reverse tokens
    rev_tokens = tokens[::-1]

    # 2. Swap parentheses in reversed stream
    for idx, token in enumerate(rev_tokens):
        if token == "(":
            rev_tokens[idx] = ")"
        elif token == ")":
            rev_tokens[idx] = "("

    output: List[str] = []
    operator_stack: List[str] = []

    # 3. Process with inverted associativity rules
    for token in rev_tokens:
        # Operand
        if token not in OPERATOR_TABLE and token not in ("(", ")"):
            output.append(token)

        # Opening parenthesis
        elif token == "(":
            operator_stack.append(token)

        # Closing parenthesis
        elif token == ")":
            found_open = False
            while operator_stack:
                top = operator_stack.pop()
                if top == "(":
                    found_open = True
                    break
                output.append(top)

            if not found_open:
                raise ValueError("Mismatched parentheses: Extraneous parenthesis.")

        # Operator
        elif token in OPERATOR_TABLE:
            prec1, is_left1 = OPERATOR_TABLE[token]

            while operator_stack and operator_stack[-1] in OPERATOR_TABLE:
                top_op = operator_stack[-1]
                prec2, _ = OPERATOR_TABLE[top_op]

                # In reversed token stream:
                # - Originally Left-Associative pops only if prec1 < prec2
                # - Originally Right-Associative pops if prec1 <= prec2
                if (is_left1 and prec1 < prec2) or (not is_left1 and prec1 <= prec2):
                    output.append(operator_stack.pop())
                else:
                    break

            operator_stack.append(token)

    # Drain stack
    while operator_stack:
        top = operator_stack.pop()
        if top == "(":
            raise ValueError("Mismatched parentheses: Unclosed parenthesis.")
        output.append(top)

    # 4. Final reverse gives Prefix
    prefix_tokens = output[::-1]
    return " ".join(prefix_tokens)


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Runs comprehensive tests for infix to prefix conversion."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Infix to Prefix (Program 04)")
    print("=" * 65)

    test_cases = [
        # Basic precedence
        ("A + B * C", "+ A * B C"),
        ("A * B + C", "+ * A B C"),
        ("(A + B) * C", "* + A B C"),
        ("A * (B + C)", "* A + B C"),

        # Associativity verification
        ("A - B - C", "- - A B C"),         # Left-associative: (A-B)-C
        ("A - (B - C)", "- A - B C"),       # Explicit parentheses
        ("A ^ B ^ C", "^ A ^ B C"),         # Right-associative: A^(B^C)
        ("(A ^ B) ^ C", "^ ^ A B C"),       # Overridden associativity

        # Multi-operator mixed expressions
        ("(A + B) * (C - D)", "* + A B - C D"),
        ("A // B + C % D", "+ // A B % C D"),
        ("100 + 200 * 30", "+ 100 * 200 30"),

        # Complex nested expression
        ("((A + B) * C) - (D // (E ^ F))", "- * + A B C // D ^ E F")
    ]

    for infix_expr, expected_prefix in test_cases:
        actual = infix_to_prefix(infix_expr)
        assert actual == expected_prefix, f"Failed for {infix_expr}: got '{actual}', expected '{expected_prefix}'"
        print(f"  [Passed] '{infix_expr}' -> '{actual}'")

    # Error handling tests
    print("\n  Testing Error Detection:")
    try:
        infix_to_prefix("(A + B")
        assert False, "Should raise ValueError for unclosed '('"
    except ValueError as err:
        print(f"  [Passed] Caught unclosed parenthesis: {err}")

    try:
        infix_to_prefix("A + B)")
        assert False, "Should raise ValueError for extraneous ')'"
    except ValueError as err:
        print(f"  [Passed] Caught extraneous parenthesis: {err}")

    print("\nAll Program 04 automated tests PASSED successfully!")


def main() -> None:
    """Interactive command-line converter."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("\n==================================================")
    print("       INFIX TO PREFIX CONVERTER (Program 04)")
    print("==================================================")
    print("Operators supported: +, -, *, /, //, %, ^ (exponentiation)")
    print("Type 'exit' to quit.\n")

    while True:
        expr = input("Enter Infix Expression: ").strip()
        if expr.lower() in ("exit", "quit"):
            print("Exiting converter. Goodbye!")
            break

        if not expr:
            continue

        try:
            prefix = infix_to_prefix(expr)
            print(f"  Infix  : {expr}")
            print(f"  Prefix : {prefix}\n")
        except ValueError as err:
            print(f"  Error: {err}\n")


if __name__ == "__main__":
    main()

