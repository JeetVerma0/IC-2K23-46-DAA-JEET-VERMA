"""
Program 03: Sparse Matrix (Triple Representation & Operations)
Course: IC-307D Data Structures and Algorithms Lab
Unit 1: Introduction to Data Structures & Arrays (CO1)

This program implements:
1. Conversion of a standard 2D matrix to canonical Triple Representation (Coordinate List format).
   - Header Row: [Total Rows, Total Columns, Total Non-zero Elements]
   - Subsequent Rows: [Row Index, Column Index, Non-zero Value]
2. Formatted display of both 2D dense and 3-column sparse formats.
3. Reconstruction of the original 2D matrix from triple representation.
4. Basic sparse matrix operations:
   - Transpose in triple format (row-col swap and canonical reordering).
   - Sparse matrix addition using linear two-pointer merge algorithm.
5. In-depth space optimization and sparsity analysis.
6. Validation of matrix dimensions and incompatible operations.
7. Interactive menu-driven interface and automated self-tests.
"""

import sys
from typing import Any, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Validation Helpers
# ---------------------------------------------------------------------------

def validate_dense_matrix(matrix: List[List[Any]]) -> Tuple[int, int]:
    """
    Validates that matrix is non-empty and rectangular.

    Returns:
        (rows, cols)

    Raises:
        ValueError: If empty or irregular.
        TypeError: If not a list of lists.
    """
    if not isinstance(matrix, list) or len(matrix) == 0:
        raise ValueError("Matrix is empty or invalid.")
    if not isinstance(matrix[0], list) or len(matrix[0]) == 0:
        raise ValueError("Matrix has invalid or empty rows.")

    cols = len(matrix[0])
    for r_idx, row in enumerate(matrix):
        if not isinstance(row, list) or len(row) != cols:
            raise ValueError(
                f"Irregular matrix: row {r_idx} has {len(row)} columns, expected {cols}."
            )

    return len(matrix), cols


def validate_triple(triples: List[List[Any]]) -> Tuple[int, int, int]:
    """
    Validates that triples list is a valid triple representation.

    Header format: [num_rows, num_cols, num_non_zero]
    Element rows: [row, col, value]

    Returns:
        (num_rows, num_cols, num_non_zero)

    Raises:
        ValueError: If structure, count, or indices are invalid.
    """
    if not isinstance(triples, list) or len(triples) < 1:
        raise ValueError("Sparse triple list must contain at least a header row.")

    header = triples[0]
    if len(header) != 3:
        raise ValueError(f"Header must contain exactly 3 elements [rows, cols, count], got {header}.")

    num_rows, num_cols, count = header[0], header[1], header[2]

    if num_rows < 0 or num_cols < 0 or count < 0:
        raise ValueError("Header dimensions and element count must be non-negative.")

    if len(triples) - 1 != count:
        raise ValueError(
            f"Triple header claims {count} non-zero entries, but found {len(triples) - 1} entries."
        )

    for i in range(1, len(triples)):
        entry = triples[i]
        if len(entry) != 3:
            raise ValueError(f"Triple at index {i} must have 3 items [row, col, value], got {entry}.")
        r, c, val = entry[0], entry[1], entry[2]
        if not (0 <= r < num_rows):
            raise ValueError(f"Triple at index {i} has invalid row {r} (matrix has {num_rows} rows).")
        if not (0 <= c < num_cols):
            raise ValueError(f"Triple at index {i} has invalid col {c} (matrix has {num_cols} cols).")
        if val == 0:
            raise ValueError(f"Triple at index {i} contains zero value, which is not permitted in sparse list.")

    return num_rows, num_cols, count


# ---------------------------------------------------------------------------
# Core Conversion Functions
# ---------------------------------------------------------------------------

def matrix_to_triple(matrix: List[List[Any]]) -> List[List[Any]]:
    """
    Converts a standard 2D matrix into canonical 3-tuple representation.

    Triple Format Structure:
        - Row 0 (Header): [rows, cols, num_non_zero]
        - Rows 1..k: [row_index, col_index, non_zero_value]
        Entries are ordered in row-major order (sorted by row, then col).

    Time Complexity: O(R * C) where R is rows and C is columns.
    Space Complexity: O(K) where K is the number of non-zero elements.

    Args:
        matrix: 2D list of numbers.

    Returns:
        List of 3-element lists representing the sparse matrix.
    """
    rows, cols = validate_dense_matrix(matrix)
    entries: List[List[Any]] = []

    for r in range(rows):
        for c in range(cols):
            val = matrix[r][c]
            if val != 0:
                entries.append([r, c, val])

    header = [rows, cols, len(entries)]
    return [header] + entries


def triple_to_matrix(triples: List[List[Any]]) -> List[List[Any]]:
    """
    Reconstructs the original 2D dense matrix from its triple representation.

    Algorithm:
        1. Read dimensions (rows, cols) from header.
        2. Initialize an empty dense matrix of size rows x cols with all zeros.
        3. Iterate through each triple [r, c, val] and assign matrix[r][c] = val.

    Time Complexity: O(R * C + K)
    Space Complexity: O(R * C) to construct the reconstructed dense matrix.

    Args:
        triples: The sparse triple list.

    Returns:
        A 2D list with all zero and non-zero values restored.
    """
    num_rows, num_cols, _ = validate_triple(triples)
    reconstructed = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    for entry in triples[1:]:
        r, c, val = entry[0], entry[1], entry[2]
        reconstructed[r][c] = val

    return reconstructed


# ---------------------------------------------------------------------------
# Sparse Matrix Operations
# ---------------------------------------------------------------------------

def transpose_sparse(triples: List[List[Any]]) -> List[List[Any]]:
    """
    Computes the transpose of a sparse matrix directly in triple representation.

    Concept & Mathematical Explanation:
        In matrix transpose, element at position (r, c) moves to position (c, r),
        and overall dimensions (rows, cols) become (cols, rows).
        In canonical triple representation, entries must remain sorted primarily
        by row, then by column. Therefore, after swapping row and column indices,
        we sort the resulting triples so that the transposed matrix is immediately
        usable by all standard sparse operations.

    Time Complexity: O(K log K) where K is the number of non-zero elements.
    Space Complexity: O(K) to store the transposed triples.

    Args:
        triples: The source sparse matrix in triple format.

    Returns:
        A new triple-format list representing the transposed matrix.
    """
    num_rows, num_cols, count = validate_triple(triples)

    if count == 0:
        # Empty sparse matrix: just swap dimensions in header
        return [[num_cols, num_rows, 0]]

    # Swap row and column for each non-zero entry
    transposed_entries = [[entry[1], entry[0], entry[2]] for entry in triples[1:]]

    # Sort canonically: primarily by new row index, secondarily by new col index
    transposed_entries.sort(key=lambda item: (item[0], item[1]))

    new_header = [num_cols, num_rows, count]
    return [new_header] + transposed_entries


def add_sparse(triples_a: List[List[Any]], triples_b: List[List[Any]]) -> List[List[Any]]:
    """
    Adds two sparse matrices directly using their triple representations.

    Two-Pointer Linear Merge Algorithm:
        Since both inputs are in canonical row-major order:
        - Let pointer i traverse entries of matrix A, and j traverse matrix B.
        - Compare coordinates (r_A, c_A) with (r_B, c_B):
            Case 1: (r_A, c_A) < (r_B, c_B)
                Entry from A appears earlier. Append it and increment i.
            Case 2: (r_A, c_A) > (r_B, c_B)
                Entry from B appears earlier. Append it and increment j.
            Case 3: (r_A, c_A) == (r_B, c_B)
                Same coordinate. Sum the values: sum_val = val_A + val_B.
                CRITICAL: If sum_val != 0, append [r_A, c_A, sum_val].
                If sum_val == 0 (values cancel each other out), do NOT append!
                Increment both i and j.
        - Append any remaining elements from either list.

    Time Complexity: O(K_A + K_B) linear merge where K_A, K_B are non-zero counts.
    Space Complexity: O(K_A + K_B) for the resulting sum triples.

    Args:
        triples_a: First sparse matrix in triple format.
        triples_b: Second sparse matrix in triple format.

    Returns:
        The resulting sum in triple format.

    Raises:
        ValueError: If matrix dimensions are incompatible for addition.
    """
    rows_a, cols_a, _ = validate_triple(triples_a)
    rows_b, cols_b, _ = validate_triple(triples_b)

    if rows_a != rows_b or cols_a != cols_b:
        raise ValueError(
            f"Cannot add matrices: Dimension mismatch! "
            f"Matrix A is {rows_a}x{cols_a}, but Matrix B is {rows_b}x{cols_b}."
        )

    result_entries: List[List[Any]] = []
    i = 1
    j = 1
    len_a = len(triples_a)
    len_b = len(triples_b)

    while i < len_a and j < len_b:
        ra, ca, va = triples_a[i]
        rb, cb, vb = triples_b[j]

        pos_a = (ra, ca)
        pos_b = (rb, cb)

        if pos_a < pos_b:
            result_entries.append([ra, ca, va])
            i += 1
        elif pos_a > pos_b:
            result_entries.append([rb, cb, vb])
            j += 1
        else:
            # Same coordinate: compute sum
            sum_val = va + vb
            if sum_val != 0:
                result_entries.append([ra, ca, sum_val])
            i += 1
            j += 1

    # Append remaining entries from A
    while i < len_a:
        result_entries.append(triples_a[i][:])
        i += 1

    # Append remaining entries from B
    while j < len_b:
        result_entries.append(triples_b[j][:])
        j += 1

    header = [rows_a, cols_a, len(result_entries)]
    return [header] + result_entries


# ---------------------------------------------------------------------------
# Space Optimization Analysis
# ---------------------------------------------------------------------------

def analyze_space_optimization(rows: int, cols: int, num_non_zero: int, bytes_per_unit: int = 4) -> str:
    """
    Analyzes and compares memory usage between standard 2D array and sparse triple format.

    Mathematical Analysis:
        - Total Elements in Matrix: M * N
        - Dense Matrix Storage:
            Requires storing all M * N elements, including zeros.
            Total Units = M * N
            Total Bytes = M * N * bytes_per_unit
        - Sparse Triple Representation:
            Requires 1 header row (rows, cols, count) + K data rows (row, col, value).
            Each row holds 3 numbers.
            Total Units = 3 * (K + 1)
            Total Bytes = 3 * (K + 1) * bytes_per_unit
        - Break-even / Crossover Threshold:
            Sparse storage < Dense storage
            3 * (K + 1) < M * N  ==>  K < (M * N - 3) / 3
            In general, if non-zero count K is less than ~33.3% of total elements,
            sparse representation uses less storage than a dense 2D array.
        - Sparsity Percentage:
            Sparsity = ((M * N - K) / (M * N)) * 100%

    Args:
        rows: Number of rows.
        cols: Number of columns.
        num_non_zero: Number of non-zero entries (K).
        bytes_per_unit: Assumed bytes per integer/float (default 4 bytes).

    Returns:
        A comprehensive multi-line analysis string.
    """
    total_elements = rows * cols
    if total_elements == 0:
        return "Empty matrix: 0 elements."

    zeros = total_elements - num_non_zero
    sparsity_pct = (zeros / total_elements) * 100.0

    dense_units = total_elements
    dense_bytes = dense_units * bytes_per_unit

    sparse_units = 3 * (num_non_zero + 1)
    sparse_bytes = sparse_units * bytes_per_unit

    threshold_k = max(0, (total_elements - 3) // 3)
    threshold_pct = (threshold_k / total_elements) * 100.0 if total_elements > 0 else 0

    diff_bytes = dense_bytes - sparse_bytes
    if diff_bytes > 0:
        savings_pct = (diff_bytes / dense_bytes) * 100.0
        status_msg = f"SAVING: Sparse format saves {diff_bytes} bytes ({savings_pct:.2f}% memory reduction)!"
    elif diff_bytes < 0:
        overhead_pct = (abs(diff_bytes) / dense_bytes) * 100.0
        status_msg = f"OVERHEAD: Dense format is better by {abs(diff_bytes)} bytes ({overhead_pct:.2f}% extra in triple)."
    else:
        status_msg = "BREAK-EVEN: Both representations use identical memory."

    report = f"""
============================================================
              SPARSE STORAGE OPTIMIZATION REPORT
============================================================
Matrix Dimensions        : {rows} rows x {cols} columns
Total Matrix Elements    : {total_elements}
Non-zero Elements (K)    : {num_non_zero}
Zero Elements            : {zeros}
Matrix Sparsity          : {sparsity_pct:.2f}% (zeros / total)
------------------------------------------------------------
Dense 2D Storage Formula : M * N = {total_elements} units ({dense_bytes} bytes @ {bytes_per_unit}B/unit)
Sparse Triple Formula    : 3 * (K + 1) = {sparse_units} units ({sparse_bytes} bytes @ {bytes_per_unit}B/unit)
Crossover Threshold      : K < {threshold_k} elements (~{threshold_pct:.1f}% density)
Verdict                  : {status_msg}
============================================================
"""
    return report.strip()


# ---------------------------------------------------------------------------
# Display Functions
# ---------------------------------------------------------------------------

def display_dense_matrix(matrix: List[List[Any]], name: str = "Dense Matrix") -> None:
    """Prints a standard 2D matrix in tabular form."""
    try:
        rows, cols = validate_dense_matrix(matrix)
    except (ValueError, TypeError) as err:
        print(f"\n{name} cannot be displayed: {err}")
        return

    print(f"\n{name} ({rows} x {cols}):")
    col_hdr = "       " + "".join(f"[{c}]".center(8) for c in range(cols))
    print(col_hdr)
    print("-" * len(col_hdr))
    for r in range(rows):
        row_str = f"[{r}]   |" + "".join(f"{str(matrix[r][c]):>7} " for c in range(cols))
        print(row_str)
    print("-" * len(col_hdr))


def display_triple(triples: List[List[Any]], name: str = "Sparse Matrix (Triple Format)") -> None:
    """Prints the 3-column triple representation in a neat table."""
    try:
        num_rows, num_cols, count = validate_triple(triples)
    except (ValueError, TypeError) as err:
        print(f"\n{name} cannot be displayed: {err}")
        return

    print(f"\n{name}:")
    print(f"Header: Rows = {num_rows}, Columns = {num_cols}, Non-zero Elements = {count}")
    print("-" * 38)
    print(f"{'Index':<8}| {'Row':<8}| {'Col':<8}| {'Value':<8}")
    print("-" * 38)
    # Header row at index 0
    hdr = triples[0]
    print(f"{'0 (H)':<8}| {hdr[0]:<8}| {hdr[1]:<8}| {hdr[2]:<8}")
    # Elements
    for idx in range(1, len(triples)):
        r, c, v = triples[idx]
        print(f"{idx:<8}| {r:<8}| {c:<8}| {v:<8}")
    print("-" * 38)


# ---------------------------------------------------------------------------
# Built-in Self-Tests
# ---------------------------------------------------------------------------

def run_self_tests() -> None:
    """Automated test cases for sparse matrix conversions, operations, and analysis."""
    print("\n==========================================")
    print("Running Self-Tests for Program 3 (Sparse Matrix)")
    print("==========================================")

    # 1. Conversion and Round-Trip Reconstruction
    print("\n[Test 1] Sparse matrix conversion and reconstruction:")
    dense_sample = [
        [0, 0, 3, 0],
        [0, 5, 0, 0],
        [0, 0, 0, 7],
        [0, 0, 0, 0]
    ]
    triples = matrix_to_triple(dense_sample)
    expected_header = [4, 4, 3]
    assert triples[0] == expected_header, f"Expected header {expected_header}, got {triples[0]}"
    assert triples[1:] == [[0, 2, 3], [1, 1, 5], [2, 3, 7]], "Triples incorrect"
    print(f"  Passed: Triples generated: {triples}")

    reconstructed = triple_to_matrix(triples)
    assert reconstructed == dense_sample, "Reconstruction does not match original"
    print("  Passed: Matrix correctly reconstructed from triples")

    # 2. Boundary: Completely Zero Matrix
    print("\n[Test 2] Completely zero matrix:")
    zero_dense = [[0, 0], [0, 0]]
    zero_triple = matrix_to_triple(zero_dense)
    assert zero_triple == [[2, 2, 0]], f"Expected [[2, 2, 0]], got {zero_triple}"
    assert triple_to_matrix(zero_triple) == zero_dense
    print("  Passed: Completely zero matrix handled correctly")

    # 3. Boundary: 1x1 Non-zero Matrix
    print("\n[Test 3] 1x1 Matrix:")
    one_by_one = [[42]]
    one_triple = matrix_to_triple(one_by_one)
    assert one_triple == [[1, 1, 1], [0, 0, 42]]
    assert triple_to_matrix(one_triple) == one_by_one
    print("  Passed: 1x1 matrix converted and restored")

    # 4. Transpose in Triple Representation
    print("\n[Test 4] Sparse transpose:")
    # Original: 3x4 matrix with non-zeros at (0, 3)=10 and (2, 1)=20
    m_rect = [
        [0, 0, 0, 10],
        [0, 0, 0, 0],
        [0, 20, 0, 0]
    ]
    t_rect = matrix_to_triple(m_rect)
    transposed_t = transpose_sparse(t_rect)
    # Expected transpose: 4x3 matrix, non-zeros at (1, 2)=20 and (3, 0)=10
    reconstructed_trans = triple_to_matrix(transposed_t)
    expected_dense_trans = [
        [0, 0, 0],
        [0, 0, 20],
        [0, 0, 0],
        [10, 0, 0]
    ]
    assert reconstructed_trans == expected_dense_trans, f"Transpose failed: {reconstructed_trans}"
    print(f"  Passed: Sparse transpose matches dense transpose correctly")

    # 5. Sparse Addition of Compatible Matrices
    print("\n[Test 5] Sparse matrix addition:")
    dense_a = [
        [1, 0, 0],
        [0, 0, 2]
    ]
    dense_b = [
        [0, 0, 5],
        [0, 3, 2]
    ]
    t_a = matrix_to_triple(dense_a)
    t_b = matrix_to_triple(dense_b)
    sum_t = add_sparse(t_a, t_b)
    sum_dense = triple_to_matrix(sum_t)
    expected_sum = [
        [1, 0, 5],
        [0, 3, 4]
    ]
    assert sum_dense == expected_sum, f"Expected {expected_sum}, got {sum_dense}"
    print(f"  Passed: Sparse addition matches dense sum: {sum_dense}")

    # 6. Cancellation to Zero in Addition
    print("\n[Test 6] Addition with cancellation to zero:")
    dense_c = [
        [-1, 0, 0],
        [0, 0, -2]
    ]
    t_c = matrix_to_triple(dense_c)
    sum_zero_t = add_sparse(t_a, t_c)
    assert sum_zero_t == [[2, 3, 0]], f"Expected [[2, 3, 0]], got {sum_zero_t}"
    print("  Passed: Cancelling elements properly removed from non-zero triples")

    # 7. Addition of Incompatible Matrices
    print("\n[Test 7] Incompatible dimension addition rejection:")
    t_diff_dim = [[3, 2, 0]]  # 3x2 vs 2x3
    try:
        add_sparse(t_a, t_diff_dim)
        assert False, "Should raise ValueError for mismatched dimensions"
    except ValueError as e:
        print(f"  Passed: Caught dimension mismatch ({e})")

    # 8. Space Optimization Analysis Check
    print("\n[Test 8] Space optimization report generation:")
    rep = analyze_space_optimization(100, 100, 50)
    assert "SAVING" in rep, "100x100 with 50 elements should show memory savings"
    print("  Passed: Space optimization calculation verified")

    print("\nAll Program 3 self-tests PASSED successfully!")


# ---------------------------------------------------------------------------
# Menu-Driven User Interface
# ---------------------------------------------------------------------------

def parse_num(s: str) -> Any:
    """Helper to parse numeric input as int or float."""
    v = s.strip()
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v


def main() -> None:
    """Main interactive driver for Program 3."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_self_tests()
        sys.exit(0)

    current_matrix: Optional[List[List[Any]]] = None
    current_triple: Optional[List[List[Any]]] = None

    menu = """
========================================
     SPARSE MATRIX OPERATIONS MENU (CO1)
========================================
1. Input Dense Matrix & Convert to Triple Representation
2. Display Current Dense Matrix
3. Display Current Sparse Triple Representation
4. Reconstruct Dense Matrix from Triple Representation
5. Transpose Sparse Matrix
6. Add Another Sparse Matrix
7. View Space Optimization & Sparsity Analysis
8. Run Automated Self-Tests
9. Exit
========================================
"""

    while True:
        print(menu)
        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            try:
                r_in = int(input("Enter number of rows: ").strip())
                c_in = int(input("Enter number of columns: ").strip())
                if r_in <= 0 or c_in <= 0:
                    print("Error: Dimensions must be positive.")
                    continue

                print(f"Enter {c_in} space-separated values for each of the {r_in} rows (use 0 for zero elements):")
                mat = []
                for r in range(r_in):
                    row_tokens = input(f"Row {r}: ").strip().split()
                    if len(row_tokens) != c_in:
                        raise ValueError(f"Expected {c_in} numbers, but got {len(row_tokens)}.")
                    mat.append([parse_num(tok) for tok in row_tokens])

                current_matrix = mat
                current_triple = matrix_to_triple(mat)
                print("\nMatrix converted to Triple Representation successfully!")
                display_dense_matrix(current_matrix, "Original Dense Matrix")
                display_triple(current_triple, "Converted Triple Representation")
            except ValueError as err:
                print(f"Input Error: {err}")

        elif choice == "2":
            if current_matrix is None:
                print("No matrix loaded. Please enter one using Option 1.")
            else:
                display_dense_matrix(current_matrix, "Current Dense Matrix")

        elif choice == "3":
            if current_triple is None:
                print("No sparse triple loaded. Please enter a matrix using Option 1.")
            else:
                display_triple(current_triple, "Current Sparse Matrix (Triple Format)")

        elif choice == "4":
            if current_triple is None:
                print("No sparse triple loaded. Please enter a matrix using Option 1.")
                continue
            reconstructed = triple_to_matrix(current_triple)
            display_dense_matrix(reconstructed, "Reconstructed Dense Matrix from Triples")

        elif choice == "5":
            if current_triple is None:
                print("No sparse triple loaded. Please enter a matrix using Option 1.")
                continue
            trans_triple = transpose_sparse(current_triple)
            print("\nTranspose performed successfully on Triple Representation!")
            display_triple(trans_triple, "Transposed Sparse Matrix")
            display_dense_matrix(triple_to_matrix(trans_triple), "Reconstructed Transposed Matrix")

        elif choice == "6":
            if current_triple is None:
                print("Please create Matrix A first using Option 1.")
                continue
            rows_a, cols_a, _ = current_triple[0]
            print(f"\nEntering Matrix B for addition (must have dimension {rows_a} x {cols_a}):")
            try:
                mat_b = []
                for r in range(rows_a):
                    row_tokens = input(f"Row {r}: ").strip().split()
                    if len(row_tokens) != cols_a:
                        raise ValueError(f"Expected {cols_a} numbers, got {len(row_tokens)}.")
                    mat_b.append([parse_num(tok) for tok in row_tokens])

                triple_b = matrix_to_triple(mat_b)
                sum_triple = add_sparse(current_triple, triple_b)
                print("\nMatrices added successfully using sparse two-pointer merge!")
                display_triple(sum_triple, "Sum Sparse Matrix (Triple Format)")
                display_dense_matrix(triple_to_matrix(sum_triple), "Reconstructed Sum Matrix")
            except ValueError as err:
                print(f"Addition Error: {err}")

        elif choice == "7":
            if current_triple is None:
                print("Please enter a matrix first using Option 1.")
                continue
            rows, cols, count = current_triple[0]
            report = analyze_space_optimization(rows, cols, count)
            print(report)

        elif choice == "8":
            run_self_tests()

        elif choice == "9":
            print("Exiting Sparse Matrix Operations. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option between 1 and 9.")


if __name__ == "__main__":
    main()

