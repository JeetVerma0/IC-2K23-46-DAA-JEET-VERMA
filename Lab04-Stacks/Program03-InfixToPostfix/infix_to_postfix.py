"""
Program 03: Infix to Postfix Expression Conversion
Course: IC-307D Data Structures and Algorithms Lab
Unit 4: Stacks (CO1)

This program converts standard Infix mathematical expressions to Postfix (Reverse Polish)
notation using a stack-based algorithm (Dijkstra's Shunting-Yard algorithm):
- Supported Operators:
    - Exponentiation: '^' (Precedence 4, Right-Associative)
    - Multiplicative: '*', '/', '//' (floor division), '%' (modulo) (Precedence 3, Left-Associative)
    - Additive: '+', '-' (Precedence 2, Left-Associative)
- Parentheses Handling:
    '(' and ')' override standard precedence.
- Operands:
    Supports multi-digit numbers (integers, floats) and alphanumeric variable names.
- Error Detection:
    Detects and rejects mismatched parentheses and malformed operator sequences.
- Interactive mode and automated test suite (--test flag).
"""

import sys
from typing import List, Tuple


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
    Splits an infix expression into distinct tokens:
    operators ('//', '+', '-', '*', '/', '%', '^'),
    parentheses ('(', ')'), and alphanumeric operands.

    Raises:
        ValueError: If illegal/unrecognized characters are present.
    """
    tokens: List[str] = []
    i = 0
    n = len(expression)

    while i < n:
        char = expression[i]

        # 1. Skip whitespace
        if char.isspace():
            i += 1
            continue

        # 2. Check for two-character operator '//'
        if char == "/" and i + 1 < n and expression[i + 1] == "/":
            tokens.append("//")
            i += 2
            continue

        # 3. Single character operators and parentheses
        if char in ("+", "-", "*", "/", "%", "^", "(", ")"):
            tokens.append(char)
            i += 1
            continue

        # 4. Alphanumeric operands (variable names or numeric constants)
        if char.isalnum() or char == ".":
            start = i
            while i < n and (expression[i].isalnum() or expression[i] == "."):
                i += 1
            tokens.append(expression[start:i])
            continue

        raise ValueError(f"Unrecognized character in expression: '{char}' at index {i}")

    return tokens


def infix_to_postfix(expression: str) -> str:
    """
    Converts an infix expression string into a space-delimited postfix expression string.

    Algorithm:
        1. Tokenize the input string.
        2. Initialize an empty operator stack and an empty output list.
        3. For each token:
           - If operand: append directly to output.
           - If '(': push to operator stack.
           - If ')': pop from stack to output until '(' is encountered. Discard '('.
           - If operator 'op1':
             - While stack top is an operator 'op2' and either:
               a) op1 is left-associative AND prec(op1) <= prec(op2), OR
               b) op1 is right-associative AND prec(op1) < prec(op2):
               pop op2 from stack to output.
             - Push op1 to stack.
        4. Pop all remaining operators from stack to output.

    Raises:
        ValueError: For mismatched parentheses or empty expressions.

    Time Complexity: O(n) where n is token count.
    Auxiliary Space Complexity: O(n) for stack and output buffer.
    """
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("Expression is empty.")

    output: List[str] = []
    operator_stack: List[str] = []

    # Track previous token type to validate structure
    for token in tokens:
        # Case A: Operand (Number or Identifier)
        if token not in OPERATOR_TABLE and token not in ("(", ")"):
            output.append(token)

        # Case B: Left Parenthesis
        elif token == "(":
            operator_stack.append(token)

        # Case C: Right Parenthesis
        elif token == ")":
            found_open = False
            while operator_stack:
                top = operator_stack.pop()
                if top == "(":
                    found_open = True
                    break
                output.append(top)

            if not found_open:
                raise ValueError("Mismatched parentheses: Extraneous closing parenthesis ')'.")

        # Case D: Operator
        elif token in OPERATOR_TABLE:
            prec1, is_left1 = OPERATOR_TABLE[token]

            while operator_stack and operator_stack[-1] in OPERATOR_TABLE:
                top_op = operator_stack[-1]
                prec2, _ = OPERATOR_TABLE[top_op]

                # Precedence / Associativity comparison condition
                if (is_left1 and prec1 <= prec2) or (not is_left1 and prec1 < prec2):
                    output.append(operator_stack.pop())
                else:
                    break

            operator_stack.append(token)

    # Drain remaining operators from stack
    while operator_stack:
        top = operator_stack.pop()
        if top == "(":
            raise ValueError("Mismatched parentheses: Unclosed opening parenthesis '('.")
        output.append(top)

    return " ".join(output)


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Runs comprehensive tests for infix to postfix conversion."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Infix to Postfix (Program 03)")
    print("=" * 65)

    test_cases = [
        # Basic operator precedence
        ("A + B * C", "A B C * +"),
        ("A * B + C", "A B * C +"),
        ("(A + B) * C", "A B + C *"),

        # Associativity tests
        ("A - B - C", "A B - C -"),           # Left-associative: (A-B)-C
        ("A ^ B ^ C", "A B C ^ ^"),           # Right-associative: A^(B^C)
        ("A ^ B ^ C ^ D", "A B C D ^ ^ ^"),   # Right-associative chain

        # Additional operators: // and %
        ("A // B + C % D", "A B // C D % +"),
        ("100 + 200 * 30", "100 200 30 * +"),

        # Complex textbook expression
        ("A + B * (C ^ D - E) ^ (F + G * H) - I",
         "A B C D ^ E - F G H * + ^ * + I -"),

        # Nested parentheses
        ("((A + B) * (C - D)) // (E ^ F)",
         "A B + C D - * E F ^ //")
    ]

    for infix_expr, expected_postfix in test_cases:
        actual = infix_to_postfix(infix_expr)
        assert actual == expected_postfix, f"Failed for {infix_expr}: got '{actual}', expected '{expected_postfix}'"
        print(f"  [Passed] '{infix_expr}' -> '{actual}'")

    # Mismatched parentheses error testing
    print("\n  Testing Error Detection:")
    try:
        infix_to_postfix("(A + B * C")
        assert False, "Should raise ValueError for unclosed '('"
    except ValueError as err:
        print(f"  [Passed] Caught unclosed parenthesis: {err}")

    try:
        infix_to_postfix("A + B) * C")
        assert False, "Should raise ValueError for extraneous ')'"
    except ValueError as err:
        print(f"  [Passed] Caught extraneous parenthesis: {err}")

    try:
        infix_to_postfix("A + @ + B")
        assert False, "Should raise ValueError for illegal character '@'"
    except ValueError as err:
        print(f"  [Passed] Caught invalid character: {err}")

    print("\nAll Program 03 automated tests PASSED successfully!")


def main() -> None:
    """Interactive command-line converter."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("\n==================================================")
    print("      INFIX TO POSTFIX CONVERTER (Program 03)")
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
            postfix = infix_to_postfix(expr)
            print(f"  Infix   : {expr}")
            print(f"  Postfix : {postfix}\n")
        except ValueError as err:
            print(f"  Error: {err}\n")


if __name__ == "__main__":
    main()

