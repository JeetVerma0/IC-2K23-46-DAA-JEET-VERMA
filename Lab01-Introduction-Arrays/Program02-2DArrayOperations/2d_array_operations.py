"""
Program 02: 2D Array Operations
Course: IC-307D Data Structures and Algorithms Lab
Unit 1: Introduction to Data Structures & Arrays (CO1)

This program demonstrates fundamental 2D array (matrix) operations using nested Python lists:
1. Matrix creation and formatted grid display.
2. Element insertion (update) at specified (row, col) coordinates.
3. Element deletion (resetting to 0/empty) at specified (row, col) coordinates.
4. Linear search across 2D grid coordinates.
5. 90-degree clockwise matrix rotation (supporting both square and rectangular matrices).
6. Rigorous validation of dimensions, bounds, and detection of irregular/jagged matrices.
7. Interactive menu-driven interface and automated self-tests.
"""

import sys
from typing import Any, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Validation & Helper Functions
# ---------------------------------------------------------------------------

def validate_matrix(matrix: List[List[Any]]) -> Tuple[int, int]:
    """
    Validates that the given object is a valid, non-empty, rectangular 2D matrix.

    Checks performed:
        1. Must be a list.
        2. Must have at least one row (rows > 0).
        3. Every row must be a list.
        4. Must have at least one column (cols > 0).
        5. Every row must have identical column length (rejects jagged/irregular matrices).

    Args:
        matrix: The 2D list to validate.

    Returns:
        A tuple of (num_rows, num_cols).

    Raises:
        ValueError: If matrix is empty, irregular, or malformed.
        TypeError: If matrix or its rows are not list instances.
    """
    if not isinstance(matrix, list):
        raise TypeError("Matrix must be represented as a Python list.")

    if len(matrix) == 0:
        raise ValueError("Matrix is empty (contains 0 rows).")

    if not isinstance(matrix[0], list):
        raise TypeError("Each row of the matrix must be a Python list.")

    num_cols = len(matrix[0])
    if num_cols == 0:
        raise ValueError("Matrix has 0 columns.")

    num_rows = len(matrix)
    for r_idx, row in enumerate(matrix):
        if not isinstance(row, list):
            raise TypeError(f"Row {r_idx} is not a list.")
        if len(row) != num_cols:
            raise ValueError(
                f"Irregular/jagged matrix detected: Row 0 has {num_cols} columns, "
                f"but row {r_idx} has {len(row)} columns."
            )

    return num_rows, num_cols


def create_matrix(rows: int, cols: int, fill_value: Any = 0) -> List[List[Any]]:
    """
    Creates a 2D matrix of dimensions rows x cols, initialized to fill_value.

    Note on Python memory model:
        Uses independent list instances for each row (`[[fill] for _ in range(rows)]`)
        to avoid shallow reference duplication (`[[fill] * cols] * rows`).

    Time Complexity: O(rows * cols)
    Space Complexity: O(rows * cols)

    Args:
        rows: Number of rows (must be > 0).
        cols: Number of columns (must be > 0).
        fill_value: Initial value for matrix elements.

    Returns:
        A 2D list of size rows x cols.

    Raises:
        ValueError: If rows <= 0 or cols <= 0.
    """
    if rows <= 0 or cols <= 0:
        raise ValueError(
            f"Matrix dimensions must be positive integers. Got rows={rows}, cols={cols}."
        )

    return [[fill_value for _ in range(cols)] for _ in range(rows)]


def display_matrix(matrix: List[List[Any]], name: str = "Matrix") -> None:
    """
    Prints a 2D matrix in a formatted tabular grid with row and column headers.

    Time Complexity: O(rows * cols)
    Space Complexity: O(1) auxiliary space.

    Args:
        matrix: The 2D list to display.
        name: A descriptive label.
    """
    try:
        rows, cols = validate_matrix(matrix)
    except (ValueError, TypeError) as err:
        print(f"\n{name} cannot be displayed: {err}")
        return

    print(f"\n{name} ({rows} x {cols}):")
    # Column headers
    col_header = "       " + "".join(f"Col {c:<6}" for c in range(cols))
    divider = "-" * len(col_header)

    print(col_header)
    print(divider)

    for r in range(rows):
        row_str = f"Row {r:<2}| " + "".join(f"{str(matrix[r][c]):<10}" for c in range(cols))
        print(row_str)

    print(divider)


# ---------------------------------------------------------------------------
# Core 2D Array Operations
# ---------------------------------------------------------------------------

def insert_element(matrix: List[List[Any]], row: int, col: int, value: Any) -> None:
    """
    Inserts (assigns) a value at the specified row and column coordinate.

    Concept:
        In a 2D matrix with fixed dimensions, inserting an element at coordinate
        (row, col) updates the cell value while verifying that coordinates remain
        within the valid grid boundaries [0 <= row < rows] and [0 <= col < cols].

    Time Complexity: O(1) direct index assignment.
    Space Complexity: O(1) auxiliary space.

    Args:
        matrix: The 2D list.
        row: Row index.
        col: Column index.
        value: The value to insert.

    Raises:
        ValueError: If matrix is irregular or empty.
        IndexError: If row or col is out of valid bounds.
    """
    rows, cols = validate_matrix(matrix)

    if row < 0 or row >= rows:
        raise IndexError(f"Row index {row} out of bounds. Valid range: [0, {rows - 1}].")
    if col < 0 or col >= cols:
        raise IndexError(f"Column index {col} out of bounds. Valid range: [0, {cols - 1}].")

    matrix[row][col] = value


def delete_element(matrix: List[List[Any]], row: int, col: int, reset_value: Any = 0) -> Any:
    """
    Deletes an element at (row, col) by resetting its cell to reset_value (default 0).

    Concept:
        In array-based matrix representations, cell deletion corresponds to clearing
        the cell back to a neutral default value (0), preserving matrix dimensions.

    Time Complexity: O(1).
    Space Complexity: O(1).

    Args:
        matrix: The 2D list.
        row: Row index.
        col: Column index.
        reset_value: Value to set after deletion (default is 0).

    Returns:
        The previous value stored at (row, col).

    Raises:
        ValueError: If matrix is irregular or empty.
        IndexError: If row or col is out of valid bounds.
    """
    rows, cols = validate_matrix(matrix)

    if row < 0 or row >= rows:
        raise IndexError(f"Row index {row} out of bounds. Valid range: [0, {rows - 1}].")
    if col < 0 or col >= cols:
        raise IndexError(f"Column index {col} out of bounds. Valid range: [0, {cols - 1}].")

    old_val = matrix[row][col]
    matrix[row][col] = reset_value
    return old_val


def search_element(matrix: List[List[Any]], target: Any) -> List[Tuple[int, int]]:
    """
    Performs a 2D linear search for target across all rows and columns.

    Algorithm:
        Traverses row-by-row (r from 0 to rows-1) and col-by-col (c from 0 to cols-1).
        Records all (r, c) tuples where matrix[r][c] == target.

    Time Complexity: O(rows * cols) full grid scan.
    Space Complexity: O(k) where k is the number of occurrences found.

    Args:
        matrix: The 2D list.
        target: The value to search for.

    Returns:
        A list of (row, col) coordinate tuples where target was found.
    """
    rows, cols = validate_matrix(matrix)
    found_positions: List[Tuple[int, int]] = []

    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == target:
                found_positions.append((r, c))

    return found_positions


def rotate_matrix_90_clockwise(matrix: List[List[Any]]) -> List[List[Any]]:
    """
    Rotates a matrix by 90 degrees clockwise.

    Supports both:
    1. Rectangular matrices (M x N -> N x M)
    2. Square matrices (N x N -> N x N)

    Mathematical Transformation:
        For an original matrix of size M x N:
        - The rotated matrix will have dimension N x M (N rows, M cols).
        - An element originally at matrix[r][c] is mapped to rotated[c][M - 1 - r].
        - Column 'c' of the original matrix becomes Row 'c' of the rotated matrix,
          with elements read from the bottom row up to the top row.

        For Square Matrices (N x N), this is also equivalent to:
            1. Transpose: Swap matrix[i][j] with matrix[j][i].
            2. Reverse: Reverse each individual row.

    Time Complexity: O(M * N) - each element is visited and placed once.
    Space Complexity: O(M * N) - allocates a new N x M matrix.

    Args:
        matrix: The 2D list to rotate.

    Returns:
        A newly created 2D list rotated 90 degrees clockwise.

    Raises:
        ValueError: If matrix is empty or irregular.
    """
    rows, cols = validate_matrix(matrix)

    # Initialize empty rotated matrix of dimensions (cols x rows)
    rotated = [[None for _ in range(rows)] for _ in range(cols)]

    for r in range(rows):
        for c in range(cols):
            # Element at (r, c) maps to (c, rows - 1 - r)
            rotated[c][rows - 1 - r] = matrix[r][c]

    return rotated


# ---------------------------------------------------------------------------
# Built-in Self-Tests
# ---------------------------------------------------------------------------

def run_self_tests() -> None:
    """
    Automated test suite verifying 2D array operations, boundaries, and errors.
    """
    print("\n==========================================")
    print("Running Self-Tests for Program 2 (2D Arrays)")
    print("==========================================")

    # 1. Creation and Validation Tests
    print("\n[Test 1] Create 2x3 matrix:")
    m = create_matrix(2, 3, 0)
    assert len(m) == 2 and len(m[0]) == 3, "Matrix dimensions incorrect"
    assert m == [[0, 0, 0], [0, 0, 0]], "Initial values incorrect"
    print("  Passed: 2x3 zero matrix created")

    print("[Test 2] Dimension validation on irregular matrix:")
    irregular = [[1, 2, 3], [4, 5]]  # Row 1 is missing an element
    try:
        validate_matrix(irregular)
        assert False, "Should have caught irregular matrix"
    except ValueError as e:
        print(f"  Passed: Caught irregular matrix ({e})")

    print("[Test 3] Dimension validation on empty matrix:")
    try:
        validate_matrix([])
        assert False, "Should have caught empty matrix"
    except ValueError:
        print("  Passed: Caught empty matrix")

    # 2. Insertion Tests
    print("\n[Test 4] Insertion at (0, 0), middle (0, 1), and boundary (1, 2):")
    insert_element(m, 0, 0, 10)
    insert_element(m, 0, 1, 20)
    insert_element(m, 1, 2, 99)
    assert m[0][0] == 10 and m[0][1] == 20 and m[1][2] == 99
    print(f"  Passed: Matrix state is {m}")

    print("[Test 5] Insertion with out-of-bounds indices:")
    try:
        insert_element(m, 2, 0, 100)  # Row 2 does not exist (valid rows: 0, 1)
        assert False, "Should raise IndexError"
    except IndexError:
        print("  Passed: Row out-of-bounds caught")

    try:
        insert_element(m, 0, 3, 100)  # Col 3 does not exist (valid cols: 0, 1, 2)
        assert False, "Should raise IndexError"
    except IndexError:
        print("  Passed: Column out-of-bounds caught")

    # 3. Deletion Tests
    print("\n[Test 6] Deletion (reset to 0) at (0, 1):")
    deleted_val = delete_element(m, 0, 1, reset_value=0)
    assert deleted_val == 20 and m[0][1] == 0
    print(f"  Passed: Deleted {deleted_val}, cell reset to {m[0][1]}")

    print("[Test 7] Deletion out-of-bounds:")
    try:
        delete_element(m, -1, 0)
        assert False, "Should raise IndexError"
    except IndexError:
        print("  Passed: Negative index caught")

    # 4. Search Tests
    print("\n[Test 8] Search for existing element:")
    m[1][0] = 99  # Now 99 exists at (1, 0) and (1, 2)
    matches = search_element(m, 99)
    assert matches == [(1, 0), (1, 2)], f"Expected [(1, 0), (1, 2)], got {matches}"
    print(f"  Passed: Found target 99 at coordinates {matches}")

    print("[Test 9] Search for non-existent element:")
    missing = search_element(m, 12345)
    assert missing == [], f"Expected [], got {missing}"
    print(f"  Passed: Missing element returned {missing}")

    # 5. Rotation Tests
    print("\n[Test 10] Rotate 3x3 square matrix 90 degrees clockwise:")
    sq = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    rot_sq = rotate_matrix_90_clockwise(sq)
    expected_sq = [
        [7, 4, 1],
        [8, 5, 2],
        [9, 6, 3]
    ]
    assert rot_sq == expected_sq, f"Expected {expected_sq}, got {rot_sq}"
    print(f"  Passed: Square matrix rotated 90 deg clockwise -> {rot_sq}")

    print("[Test 11] Four 90-degree rotations equal original matrix (360 deg identity):")
    r1 = rotate_matrix_90_clockwise(sq)
    r2 = rotate_matrix_90_clockwise(r1)
    r3 = rotate_matrix_90_clockwise(r2)
    r4 = rotate_matrix_90_clockwise(r3)
    assert r4 == sq, "Four 90-deg rotations must equal original"
    print("  Passed: 4 rotations restore original state")

    print("[Test 12] Rotate 2x3 rectangular matrix 90 degrees clockwise:")
    rect = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    rot_rect = rotate_matrix_90_clockwise(rect)
    expected_rect = [
        [4, 1],
        [5, 2],
        [6, 3]
    ]
    assert rot_rect == expected_rect, f"Expected {expected_rect}, got {rot_rect}"
    print(f"  Passed: 2x3 rotated into 3x2 matrix -> {rot_rect}")

    print("\nAll Program 2 self-tests PASSED successfully!")


# ---------------------------------------------------------------------------
# Menu-Driven User Interface
# ---------------------------------------------------------------------------

def parse_input_val(val_str: str) -> Any:
    """Helper to parse numeric or string values."""
    s = val_str.strip()
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


def main() -> None:
    """Main interactive driver for Program 2."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_self_tests()
        sys.exit(0)

    matrix: Optional[List[List[Any]]] = None

    menu = """
========================================
     2D ARRAY OPERATIONS MENU (CO1)
========================================
1. Create New Matrix (rows x cols)
2. Display Current Matrix
3. Insert / Update Element at (row, col)
4. Delete Element at (row, col) [reset to 0]
5. Search Element (2D Linear Search)
6. Rotate Matrix 90 Degrees Clockwise
7. Run Automated Self-Tests
8. Exit
========================================
"""

    while True:
        print(menu)
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            try:
                r_in = int(input("Enter number of rows: ").strip())
                c_in = int(input("Enter number of columns: ").strip())
                if r_in <= 0 or c_in <= 0:
                    print("Error: Dimensions must be positive.")
                    continue

                mode = input("Initialize with zeros (z) or manual row values (m)? [z/m]: ").strip().lower()
                if mode == "m":
                    new_m = []
                    print(f"Enter {c_in} space-separated values for each of the {r_in} rows:")
                    for r in range(r_in):
                        row_line = input(f"Row {r}: ").strip().split()
                        if len(row_line) != c_in:
                            raise ValueError(f"Expected {c_in} values, but got {len(row_line)}.")
                        new_m.append([parse_input_val(v) for v in row_line])
                    matrix = new_m
                else:
                    matrix = create_matrix(r_in, c_in, 0)

                print(f"Matrix of size {r_in} x {c_in} initialized successfully.")
                display_matrix(matrix)
            except ValueError as err:
                print(f"Input Error: {err}")

        elif choice == "2":
            if matrix is None:
                print("No matrix initialized yet. Please create one first (Option 1).")
            else:
                display_matrix(matrix)

        elif choice == "3":
            if matrix is None:
                print("No matrix initialized yet. Please create one first (Option 1).")
                continue
            display_matrix(matrix)
            try:
                r_idx = int(input("Enter row index: ").strip())
                c_idx = int(input("Enter column index: ").strip())
                val_raw = input("Enter value to insert: ")
                val = parse_input_val(val_raw)
                insert_element(matrix, r_idx, c_idx, val)
                print(f"Successfully inserted '{val}' at position ({r_idx}, {c_idx}).")
                display_matrix(matrix)
            except (ValueError, IndexError) as err:
                print(f"Error: {err}")

        elif choice == "4":
            if matrix is None:
                print("No matrix initialized yet. Please create one first (Option 1).")
                continue
            display_matrix(matrix)
            try:
                r_idx = int(input("Enter row index to delete: ").strip())
                c_idx = int(input("Enter column index to delete: ").strip())
                deleted = delete_element(matrix, r_idx, c_idx, reset_value=0)
                print(f"Successfully removed '{deleted}' at ({r_idx}, {c_idx}) (cell reset to 0).")
                display_matrix(matrix)
            except (ValueError, IndexError) as err:
                print(f"Error: {err}")

        elif choice == "5":
            if matrix is None:
                print("No matrix initialized yet. Please create one first (Option 1).")
                continue
            target_raw = input("Enter element to search for: ")
            target = parse_input_val(target_raw)
            try:
                results = search_element(matrix, target)
                if results:
                    print(f"Element '{target}' found at coordinate(s):")
                    for coord in results:
                        print(f"  -> Row {coord[0]}, Column {coord[1]}")
                else:
                    print(f"Element '{target}' not found in the matrix.")
            except (ValueError, TypeError) as err:
                print(f"Error: {err}")

        elif choice == "6":
            if matrix is None:
                print("No matrix initialized yet. Please create one first (Option 1).")
                continue
            try:
                print("\nOriginal Matrix:")
                display_matrix(matrix)
                matrix = rotate_matrix_90_clockwise(matrix)
                print("\nMatrix Rotated 90 Degrees Clockwise:")
                display_matrix(matrix)
            except ValueError as err:
                print(f"Rotation Error: {err}")

        elif choice == "7":
            run_self_tests()

        elif choice == "8":
            print("Exiting 2D Array Operations. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option between 1 and 8.")


if __name__ == "__main__":
    main()

