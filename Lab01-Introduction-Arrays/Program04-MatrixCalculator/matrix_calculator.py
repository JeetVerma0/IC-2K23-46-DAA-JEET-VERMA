"""
Program 04: Matrix Calculator
Course: IC-307D Data Structures and Algorithms Lab
Unit 1: Introduction to Data Structures & Arrays (CO1)

This program implements a robust, menu-driven Matrix Calculator supporting:
1. Matrix Addition (with strict dimension matching validation).
2. Matrix Multiplication (with compatibility check: cols(A) == rows(B)).
3. Matrix Transpose (swapping rows and columns).
4. Matrix Determinant for square matrices using Laplace Cofactor Expansion:
   - Base cases: 1x1, 2x2, 3x3.
   - Recursive cofactor expansion for small general n x n matrices.
   - Correctly handles singular matrices (determinant = 0).
   - Rejects non-square matrices with clear error reporting.
5. Interactive menu-driven interface and automated self-tests without external libraries.
"""

import sys
from typing import Any, List, Optional, Tuple, Union

Number = Union[int, float]


# ---------------------------------------------------------------------------
# Validation Helpers
# ---------------------------------------------------------------------------

def validate_matrix(matrix: List[List[Number]]) -> Tuple[int, int]:
    """
    Validates that a nested list is a valid rectangular matrix.

    Args:
        matrix: 2D list of numbers.

    Returns:
        (num_rows, num_cols)

    Raises:
        ValueError: If matrix is empty or has inconsistent row lengths.
        TypeError: If elements are not lists or contain non-numeric data.
    """
    if not isinstance(matrix, list) or len(matrix) == 0:
        raise ValueError("Matrix cannot be empty.")

    if not isinstance(matrix[0], list) or len(matrix[0]) == 0:
        raise ValueError("Matrix rows cannot be empty.")

    num_cols = len(matrix[0])
    num_rows = len(matrix)

    for r_idx, row in enumerate(matrix):
        if not isinstance(row, list):
            raise TypeError(f"Row {r_idx} must be a list.")
        if len(row) != num_cols:
            raise ValueError(
                f"Irregular matrix detected: Row 0 has {num_cols} columns, "
                f"while Row {r_idx} has {len(row)} columns."
            )
        for c_idx, val in enumerate(row):
            if not isinstance(val, (int, float)):
                raise TypeError(
                    f"Element at ({r_idx}, {c_idx}) must be numeric (int/float), got {type(val).__name__}."
                )

    return num_rows, num_cols


# ---------------------------------------------------------------------------
# Matrix Operations
# ---------------------------------------------------------------------------

def matrix_addition(a: List[List[Number]], b: List[List[Number]]) -> List[List[Number]]:
    """
    Performs element-wise addition of two matrices: C = A + B.

    Dimensional Requirement:
        Matrix A and Matrix B must have identical dimensions (rows_a == rows_b and cols_a == cols_b).

    Formula:
        C[i][j] = A[i][j] + B[i][j]

    Time Complexity: O(R * C)
    Space Complexity: O(R * C) for the result matrix.

    Args:
        a: First operand matrix.
        b: Second operand matrix.

    Returns:
        The sum matrix of dimensions R x C.

    Raises:
        ValueError: If dimensions do not match.
    """
    rows_a, cols_a = validate_matrix(a)
    rows_b, cols_b = validate_matrix(b)

    if rows_a != rows_b or cols_a != cols_b:
        raise ValueError(
            f"Cannot add matrices: Dimension mismatch! "
            f"Matrix A is {rows_a}x{cols_a}, but Matrix B is {rows_b}x{cols_b}."
        )

    result: List[List[Number]] = []
    for r in range(rows_a):
        row_sum: List[Number] = []
        for c in range(cols_a):
            sum_val = a[r][c] + b[r][c]
            # Format cleanly if integer
            if isinstance(sum_val, float) and sum_val.is_integer():
                sum_val = int(sum_val)
            row_sum.append(sum_val)
        result.append(row_sum)

    return result


def matrix_multiplication(a: List[List[Number]], b: List[List[Number]]) -> List[List[Number]]:
    """
    Multiplies two matrices: C = A x B.

    Dimensional Requirement:
        The number of columns in Matrix A must equal the number of rows in Matrix B.
        If A is of size (m x k) and B is of size (k x n), the result C will be (m x n).

    Formula:
        C[i][j] = sum(A[i][k] * B[k][j] for k in range(cols_a))

    Time Complexity: O(m * k * n) where A is (m x k) and B is (k x n).
    Space Complexity: O(m * n) for the result matrix.

    Args:
        a: First operand matrix (size m x k).
        b: Second operand matrix (size k x n).

    Returns:
        The product matrix (size m x n).

    Raises:
        ValueError: If cols_a != rows_b.
    """
    rows_a, cols_a = validate_matrix(a)
    rows_b, cols_b = validate_matrix(b)

    if cols_a != rows_b:
        raise ValueError(
            f"Cannot multiply matrices: Inner dimension mismatch! "
            f"Matrix A has {cols_a} columns, but Matrix B has {rows_b} rows. "
            f"(Condition cols(A) == rows(B) violated)."
        )

    result: List[List[Number]] = []
    for i in range(rows_a):
        row_res: List[Number] = []
        for j in range(cols_b):
            dot_product = 0
            for k in range(cols_a):
                dot_product += a[i][k] * b[k][j]
            if isinstance(dot_product, float) and dot_product.is_integer():
                dot_product = int(dot_product)
            row_res.append(dot_product)
        result.append(row_res)

    return result


def matrix_transpose(a: List[List[Number]]) -> List[List[Number]]:
    """
    Computes the transpose of a matrix: T = A^T.

    Concept:
        Rows of matrix A become columns of transpose T, and columns become rows.
        If A has dimensions (R x C), T has dimensions (C x R).

    Formula:
        T[j][i] = A[i][j]

    Time Complexity: O(R * C)
    Space Complexity: O(R * C)

    Args:
        a: The input matrix.

    Returns:
        The transposed matrix of size C x R.
    """
    rows, cols = validate_matrix(a)

    transposed: List[List[Number]] = []
    for c in range(cols):
        new_row: List[Number] = []
        for r in range(rows):
            new_row.append(a[r][c])
        transposed.append(new_row)

    return transposed


def get_submatrix(matrix: List[List[Number]], drop_row: int, drop_col: int) -> List[List[Number]]:
    """
    Constructs the minor submatrix by excluding a specified row and column.

    Used by Laplace cofactor expansion for determinant calculation.

    Time Complexity: O(n^2) where n is matrix dimension.
    Space Complexity: O(n^2) for the submatrix.

    Args:
        matrix: Square matrix of dimension n x n.
        drop_row: Row index to omit (0 <= drop_row < n).
        drop_col: Column index to omit (0 <= drop_col < n).

    Returns:
        Submatrix of dimension (n-1) x (n-1).
    """
    return [
        [matrix[r][c] for c in range(len(matrix[r])) if c != drop_col]
        for r in range(len(matrix)) if r != drop_row
    ]


def matrix_determinant(matrix: List[List[Number]]) -> Number:
    """
    Computes the determinant of a square matrix using Laplace Cofactor Expansion.

    Mathematical Concept:
        - Determinant is defined exclusively for square matrices (n x n).
        - Base Cases:
            - 1x1 Matrix: det([a]) = a
            - 2x2 Matrix: det([[a, b], [c, d]]) = a*d - b*c
            - 3x3 Matrix:
                det(A) = a00*(a11*a22 - a12*a21) - a01*(a10*a22 - a12*a20) + a02*(a10*a21 - a11*a20)
        - General n x n Laplace Expansion along Row 0:
            det(A) = sum((-1)^j * A[0][j] * det(M_0j) for j in 0..n-1)
            where M_0j is the submatrix obtained by deleting row 0 and column j.
        - Singular Matrix:
            If det(A) == 0, the matrix is singular (non-invertible, linearly dependent).

    Time Complexity:
        - 1x1: O(1)
        - 2x2: O(1)
        - 3x3: O(1)
        - General n x n: O(n!) - perfectly suited and exact for small educational matrices.
    Space Complexity:
        - O(n) call stack and submatrix memory.

    Args:
        matrix: Square matrix (n x n).

    Returns:
        The determinant value (int or float).

    Raises:
        ValueError: If matrix is not square (rows != cols).
    """
    rows, cols = validate_matrix(matrix)

    if rows != cols:
        raise ValueError(
            f"Determinant is only defined for square matrices (n x n). "
            f"Provided matrix has dimensions {rows}x{cols}."
        )

    n = rows

    # Base Case 1: 1x1 Matrix
    if n == 1:
        return matrix[0][0]

    # Base Case 2: 2x2 Matrix
    if n == 2:
        val = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        return int(val) if isinstance(val, float) and val.is_integer() else val

    # Base Case 3: 3x3 Direct Formula (Fast path optimization)
    if n == 3:
        a = matrix[0][0]
        b = matrix[0][1]
        c = matrix[0][2]

        d = matrix[1][0]
        e = matrix[1][1]
        f = matrix[1][2]

        g = matrix[2][0]
        h = matrix[2][1]
        i = matrix[2][2]

        det_val = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
        return int(det_val) if isinstance(det_val, float) and det_val.is_integer() else det_val

    # General n x n Recursive Laplace Expansion along Row 0
    det_sum = 0
    sign = 1
    for c in range(n):
        elem = matrix[0][c]
        if elem != 0:  # Optimization: skip 0 coefficients
            sub = get_submatrix(matrix, drop_row=0, drop_col=c)
            sub_det = matrix_determinant(sub)
            det_sum += sign * elem * sub_det
        sign = -sign

    if isinstance(det_sum, float) and det_sum.is_integer():
        det_sum = int(det_sum)

    return det_sum


# ---------------------------------------------------------------------------
# Display & Input Helpers
# ---------------------------------------------------------------------------

def display_matrix(matrix: List[List[Number]], name: str = "Matrix") -> None:
    """Formats and prints a matrix with clean alignment."""
    try:
        rows, cols = validate_matrix(matrix)
    except (ValueError, TypeError) as err:
        print(f"\n{name} cannot be displayed: {err}")
        return

    print(f"\n{name} ({rows} x {cols}):")
    # Determine maximum number length for consistent column width
    max_len = 5
    for row in matrix:
        for val in row:
            max_len = max(max_len, len(str(val)))
    col_w = max_len + 3

    divider = "-" * (cols * col_w + 6)
    print(divider)
    for r in range(rows):
        row_str = " | " + "".join(f"{str(matrix[r][c]):>{col_w}}" for c in range(cols)) + " |"
        print(row_str)
    print(divider)


def parse_numeric(s: str) -> Number:
    """Parses a string into an int or float."""
    token = s.strip()
    try:
        return int(token)
    except ValueError:
        return float(token)


def prompt_matrix(label: str = "Matrix") -> List[List[Number]]:
    """Prompts user to input matrix dimensions and row values with full validation."""
    print(f"\n--- Enter {label} ---")
    r_in = int(input(f"Enter number of rows for {label}: ").strip())
    c_in = int(input(f"Enter number of columns for {label}: ").strip())
    if r_in <= 0 or c_in <= 0:
        raise ValueError("Matrix dimensions must be positive integers.")

    print(f"Enter {c_in} space-separated numbers for each of the {r_in} rows:")
    mat: List[List[Number]] = []
    for r in range(r_in):
        line = input(f"Row {r}: ").strip().split()
        if len(line) != c_in:
            raise ValueError(f"Expected {c_in} numbers, but got {len(line)}.")
        mat.append([parse_numeric(v) for v in line])

    return mat


# ---------------------------------------------------------------------------
# Built-in Self-Tests
# ---------------------------------------------------------------------------

def run_self_tests() -> None:
    """Automated test cases verifying all matrix operations, boundary cases, and errors."""
    print("\n==========================================")
    print("Running Self-Tests for Program 4 (Matrix Calculator)")
    print("==========================================")

    # 1. Addition Tests
    print("\n[Test 1] Matrix Addition (Compatible 2x2):")
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    sum_ab = matrix_addition(a, b)
    expected_sum = [[6, 8], [10, 12]]
    assert sum_ab == expected_sum, f"Expected {expected_sum}, got {sum_ab}"
    print(f"  Passed: Addition correct -> {sum_ab}")

    print("[Test 2] Matrix Addition (Incompatible dimensions):")
    c_incompatible = [[1, 2, 3], [4, 5, 6]]
    try:
        matrix_addition(a, c_incompatible)
        assert False, "Should raise ValueError for mismatched dimensions"
    except ValueError as e:
        print(f"  Passed: Dimension mismatch caught ({e})")

    # 2. Multiplication Tests
    print("\n[Test 3] Matrix Multiplication (Compatible 2x3 and 3x2 -> 2x2):")
    m1 = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    m2 = [
        [7, 8],
        [9, 1],
        [2, 3]
    ]
    # Row 0 dot Col 0: 1*7 + 2*9 + 3*2 = 7 + 18 + 6 = 31
    # Row 0 dot Col 1: 1*8 + 2*1 + 3*3 = 8 + 2 + 9 = 19
    # Row 1 dot Col 0: 4*7 + 5*9 + 6*2 = 28 + 45 + 12 = 85
    # Row 1 dot Col 1: 4*8 + 5*1 + 6*3 = 32 + 5 + 18 = 55
    prod = matrix_multiplication(m1, m2)
    expected_prod = [[31, 19], [85, 55]]
    assert prod == expected_prod, f"Expected {expected_prod}, got {prod}"
    print(f"  Passed: Multiplication correct -> {prod}")

    print("[Test 4] Matrix Multiplication (Incompatible dimensions):")
    try:
        # m1 is 2x3, b is 2x2: cols(m1)=3 != rows(b)=2
        matrix_multiplication(m1, b)
        assert False, "Should raise ValueError when cols(A) != rows(B)"
    except ValueError as e:
        print(f"  Passed: Incompatible multiplication caught ({e})")

    # 3. Transpose Tests
    print("\n[Test 5] Transpose (Rectangular 2x3 -> 3x2):")
    trans_m1 = matrix_transpose(m1)
    expected_trans = [
        [1, 4],
        [2, 5],
        [3, 6]
    ]
    assert trans_m1 == expected_trans, f"Expected {expected_trans}, got {trans_m1}"
    print(f"  Passed: Transpose of 2x3 -> 3x2 matches: {trans_m1}")

    # 4. Determinant Tests
    print("\n[Test 6] Determinant 1x1 Matrix:")
    d1 = matrix_determinant([[42]])
    assert d1 == 42, f"Expected 42, got {d1}"
    print("  Passed: det([[42]]) = 42")

    print("[Test 7] Determinant 2x2 Matrix:")
    d2 = matrix_determinant([[1, 2], [3, 4]])
    assert d2 == -2, f"Expected -2, got {d2}"
    print("  Passed: det([[1, 2], [3, 4]]) = -2")

    print("[Test 8] Determinant 3x3 Matrix (Non-singular):")
    m3 = [
        [6, 1, 1],
        [4, -2, 5],
        [2, 8, 7]
    ]
    d3 = matrix_determinant(m3)
    assert d3 == -306, f"Expected -306, got {d3}"
    print(f"  Passed: det(3x3) = {d3}")

    print("[Test 9] Determinant of Singular Matrix (det = 0):")
    singular = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    d_sing = matrix_determinant(singular)
    assert d_sing == 0, f"Expected 0 for singular matrix, got {d_sing}"
    print("  Passed: Singular matrix correctly identified with determinant = 0")

    print("[Test 10] Determinant of Non-Square Matrix Rejection:")
    try:
        matrix_determinant([[1, 2, 3], [4, 5, 6]])
        assert False, "Should raise ValueError for non-square matrix"
    except ValueError as e:
        print(f"  Passed: Non-square determinant rejected ({e})")

    print("\nAll Program 4 self-tests PASSED successfully!")


# ---------------------------------------------------------------------------
# Menu-Driven User Interface
# ---------------------------------------------------------------------------

def main() -> None:
    """Main interactive driver for Program 4."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_self_tests()
        sys.exit(0)

    menu = """
========================================
       MATRIX CALCULATOR MENU (CO1)
========================================
1. Matrix Addition (A + B)
2. Matrix Multiplication (A x B)
3. Matrix Transpose (A^T)
4. Matrix Determinant (det(A))
5. Run Automated Self-Tests
6. Exit
========================================
"""

    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            try:
                print("\n[Matrix Addition: C = A + B]")
                mat_a = prompt_matrix("Matrix A")
                mat_b = prompt_matrix("Matrix B")
                display_matrix(mat_a, "Matrix A")
                display_matrix(mat_b, "Matrix B")
                res = matrix_addition(mat_a, mat_b)
                display_matrix(res, "Result (A + B)")
            except (ValueError, TypeError) as err:
                print(f"Addition Error: {err}")

        elif choice == "2":
            try:
                print("\n[Matrix Multiplication: C = A x B]")
                mat_a = prompt_matrix("Matrix A")
                mat_b = prompt_matrix("Matrix B")
                display_matrix(mat_a, "Matrix A")
                display_matrix(mat_b, "Matrix B")
                res = matrix_multiplication(mat_a, mat_b)
                display_matrix(res, "Result (A x B)")
            except (ValueError, TypeError) as err:
                print(f"Multiplication Error: {err}")

        elif choice == "3":
            try:
                print("\n[Matrix Transpose: T = A^T]")
                mat_a = prompt_matrix("Matrix A")
                display_matrix(mat_a, "Original Matrix A")
                res = matrix_transpose(mat_a)
                display_matrix(res, "Transposed Matrix (A^T)")
            except (ValueError, TypeError) as err:
                print(f"Transpose Error: {err}")

        elif choice == "4":
            try:
                print("\n[Matrix Determinant: det(A)]")
                mat_a = prompt_matrix("Square Matrix A")
                display_matrix(mat_a, "Matrix A")
                det = matrix_determinant(mat_a)
                print(f"\nDeterminant det(A) = {det}")
                if det == 0:
                    print("Note: det(A) = 0 indicates that Matrix A is a SINGULAR matrix (non-invertible).")
                else:
                    print("Note: det(A) != 0 indicates that Matrix A is a NON-SINGULAR matrix (invertible).")
            except (ValueError, TypeError) as err:
                print(f"Determinant Error: {err}")

        elif choice == "5":
            run_self_tests()

        elif choice == "6":
            print("Exiting Matrix Calculator. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option between 1 and 6.")


if __name__ == "__main__":
    main()

