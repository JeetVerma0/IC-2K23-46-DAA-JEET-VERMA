"""
Program 07: Complete Infix Expression Evaluator
Course: IC-307D Data Structures and Algorithms Lab
Unit 4: Stacks (CO1)

This program builds a full arithmetic Expression Evaluator:
1. Tokenization:
   - Robustly parses arithmetic expressions containing multi-digit integers,
     floating-point values, standard binary operators, and parentheses.
   - Detects and resolves unary negation (e.g. '-5', '3 * -2', '-(4 + 2)').
2. Infix to Postfix Conversion (Shunting-Yard Algorithm):
   - Respects operator precedence:
       * Precedence 4: '^' (Right-Associative Exponentiation)
       * Precedence 3: '*', '/', '//', '%' (Left-Associative Multiplicative)
       * Precedence 2: '+', '-' (Left-Associative Additive)
   - Accurately evaluates nested parentheses '(' and ')'.
3. Stack-Based Postfix Evaluation:
   - Evaluates the generated postfix token sequence using an operand stack.
   - Accurately detects and catches division/modulo by zero and malformed expressions.
   - Fully custom implementation without using Python's built-in eval().
"""

import sys
from typing import List, Union


OPERATOR_TABLE = {
    "^":  (4, False),  # Right-associative exponentiation
    "*":  (3, True),   # Left-associative multiplication
    "/":  (3, True),   # Left-associative division
    "//": (3, True),   # Left-associative floor division
    "%":  (3, True),   # Left-associative modulus
    "+":  (2, True),   # Left-associative addition
    "-":  (2, True),   # Left-associative subtraction
}


def tokenize_expression(expression: str) -> List[str]:
    """
    Splits an infix arithmetic string into normalized tokens.
    Handles multi-digit numbers, floats, unary minus, and binary operators.

    Raises:
        ValueError: For illegal characters.
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

        # Unary negation detection:
        # A '-' is unary if it is the first token or follows an operator / open parenthesis
        if char == "-":
            is_unary = (len(tokens) == 0 or tokens[-1] in OPERATOR_TABLE or tokens[-1] == "(")
            if is_unary:
                # Lookahead to see if immediately followed by number or decimal point
                next_i = i + 1
                while next_i < n and expression[next_i].isspace():
                    next_i += 1

                if next_i < n and (expression[next_i].isdigit() or expression[next_i] == "."):
                    start = i
                    i = next_i
                    while i < n and (expression[i].isdigit() or expression[i] == "."):
                        i += 1
                    tokens.append(expression[start:i])
                    continue
                else:
                    # Unary minus preceding a parenthesis e.g. -(a + b) -> treat as (0 - ...)
                    tokens.append("0")
                    tokens.append("-")
                    i += 1
                    continue

        # Single character operators and parentheses
        if char in ("+", "-", "*", "/", "%", "^", "(", ")"):
            tokens.append(char)
            i += 1
            continue

        # Positive numbers
        if char.isdigit() or char == ".":
            start = i
            while i < n and (expression[i].isdigit() or expression[i] == "."):
                i += 1
            tokens.append(expression[start:i])
            continue

        raise ValueError(f"Unrecognized character in expression: '{char}' at position {i}")

    return tokens


def is_number(token: str) -> bool:
    """Checks whether token can be converted to float."""
    try:
        float(token)
        return True
    except ValueError:
        return False


def parse_number(token: str) -> Union[int, float]:
    """Converts a token to int if whole, or float otherwise."""
    f = float(token)
    if f.is_integer():
        return int(f)
    return f


def infix_to_postfix_tokens(tokens: List[str]) -> List[str]:
    """
    Converts tokenized infix list to postfix token list using Shunting-Yard algorithm.
    """
    if not tokens:
        raise ValueError("Expression is empty.")

    output: List[str] = []
    operator_stack: List[str] = []

    for token in tokens:
        # Number operand
        if is_number(token):
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
                raise ValueError("Mismatched parentheses: Missing matching opening '('.")

        # Operator
        elif token in OPERATOR_TABLE:
            prec1, is_left1 = OPERATOR_TABLE[token]

            while operator_stack and operator_stack[-1] in OPERATOR_TABLE:
                top_op = operator_stack[-1]
                prec2, _ = OPERATOR_TABLE[top_op]

                if (is_left1 and prec1 <= prec2) or (not is_left1 and prec1 < prec2):
                    output.append(operator_stack.pop())
                else:
                    break

            operator_stack.append(token)

        else:
            raise ValueError(f"Unexpected token: '{token}'")

    while operator_stack:
        top = operator_stack.pop()
        if top == "(":
            raise ValueError("Mismatched parentheses: Missing matching closing ')'.")
        output.append(top)

    return output


def evaluate_postfix_tokens(postfix_tokens: List[str]) -> Union[int, float]:
    """
    Evaluates a postfix token list using an operand stack.
    """
    stack: List[Union[int, float]] = []

    for token in postfix_tokens:
        if is_number(token):
            stack.append(parse_number(token))

        elif token in OPERATOR_TABLE:
            if len(stack) < 2:
                raise ValueError(
                    f"Malformed expression: Insufficient operands for operator '{token}'."
                )
            b = stack.pop()
            a = stack.pop()

            if token == "+":
                res = a + b
            elif token == "-":
                res = a - b
            elif token == "*":
                res = a * b
            elif token == "/":
                if b == 0:
                    raise ZeroDivisionError("Division by zero in '/' operation.")
                res = a / b
            elif token == "//":
                if b == 0:
                    raise ZeroDivisionError("Division by zero in '//' floor division.")
                res = a // b
            elif token == "%":
                if b == 0:
                    raise ZeroDivisionError("Modulo by zero in '%' operation.")
                res = a % b
            elif token == "^":
                res = a ** b

            if isinstance(res, float) and res.is_integer():
                res = int(res)
            stack.append(res)

        else:
            raise ValueError(f"Unexpected token in postfix evaluation: '{token}'")

    if len(stack) != 1:
        raise ValueError("Malformed expression: Unbalanced operators and operands.")

    return stack[0]


def evaluate_expression(expression: str) -> Union[int, float]:
    """
    Full pipeline: Infix String -> Tokenization -> Postfix Tokens -> Evaluated Numeric Result.

    Time Complexity: O(n)
    Auxiliary Space Complexity: O(n)
    """
    tokens = tokenize_expression(expression)
    postfix_tokens = infix_to_postfix_tokens(tokens)
    return evaluate_postfix_tokens(postfix_tokens)


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Executes comprehensive verification covering expression evaluation and error detection."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Expression Evaluator (Program 07)")
    print("=" * 65)

    test_cases = [
        # Basic arithmetic and precedence
        ("10 + 20 * 3", 70),
        ("(10 + 20) * 3", 90),
        ("50 - 20 - 10", 20),           # Left-associative subtraction: (50-20)-10 = 20
        ("100 / 4 * 2", 50),            # (100 / 4) * 2 = 50
        ("17 // 5 + 17 % 5", 5),        # 3 + 2 = 5

        # Right-associative exponentiation
        ("2 ^ 3 ^ 2", 512),             # 2 ^ (3 ^ 2) = 2 ^ 9 = 512
        ("(2 ^ 3) ^ 2", 64),            # (8) ^ 2 = 64

        # Floating-point numbers
        ("2.5 * 4.0 + 1.5", 11.5),
        ("15.5 - 5.5", 10),

        # Unary negation
        ("-5 + 15", 10),
        ("3 * -4", -12),
        ("-(4 + 2) * 3", -18),
        ("10 - -5", 15),

        # Complex nested parentheses
        ("((15 / (7 - (1 + 1))) * 3) - (2 + (1 + 1))", 5),
        ("(10 + 20) * 3 - 50 // 2", 65)
    ]

    for expr, expected in test_cases:
        actual = evaluate_expression(expr)
        assert actual == expected, f"Failed for '{expr}': got {actual}, expected {expected}"
        print(f"  [Passed] '{expr}' = {actual}")

    # Error handling tests
    print("\n  Testing Error Detection:")
    # Division by zero
    try:
        evaluate_expression("(10 + 5) / 0")
        assert False, "Should raise ZeroDivisionError"
    except ZeroDivisionError as err:
        print(f"  [Passed] Caught division by zero: {err}")

    # Mismatched parentheses
    try:
        evaluate_expression("(10 + 20 * 3")
        assert False, "Should raise ValueError for missing ')'"
    except ValueError as err:
        print(f"  [Passed] Caught missing ')': {err}")

    try:
        evaluate_expression("10 + 20) * 3")
        assert False, "Should raise ValueError for extraneous ')'"
    except ValueError as err:
        print(f"  [Passed] Caught extraneous ')': {err}")

    # Malformed expressions
    try:
        evaluate_expression("10 + * 20")
        assert False, "Should raise ValueError for malformed operator sequence"
    except ValueError as err:
        print(f"  [Passed] Caught malformed operator sequence: {err}")

    print("\nAll Program 07 automated tests PASSED successfully!")


def main() -> None:
    """Interactive command-line expression evaluator."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("\n==================================================")
    print("      INFIX EXPRESSION EVALUATOR (Program 07)")
    print("==================================================")
    print("Supports: +, -, *, /, //, %, ^, parentheses, floats, unary '-'")
    print("Type 'exit' to quit.\n")

    while True:
        expr = input("Enter Infix Arithmetic Expression: ").strip()
        if expr.lower() in ("exit", "quit"):
            print("Exiting evaluator. Goodbye!")
            break

        if not expr:
            continue

        try:
            tokens = tokenize_expression(expr)
            postfix = infix_to_postfix_tokens(tokens)
            res = evaluate_postfix_tokens(postfix)
            print(f"  Tokens  : {tokens}")
            print(f"  Postfix : {' '.join(postfix)}")
            print(f"  Result  = {res}\n")
        except (ValueError, ZeroDivisionError) as err:
            print(f"  Error: {err}\n")


if __name__ == "__main__":
    main()

