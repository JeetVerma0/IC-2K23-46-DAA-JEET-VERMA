# IC-307D: Data Structures and Algorithms Lab
## Unit 1: Introduction to Data Structures & Arrays (CO1)

---

## 1. Introduction

An **array** is one of the most fundamental data structures in computer science. It stores a collection of elements in contiguous memory locations, where each item can be accessed directly in constant time $O(1)$ using its index:

$$\text{Address}(A[i]) = \text{Base Address} + i \times \text{Size of Element}$$

Arrays form the backbone of memory management, buffer allocation, cache-friendly data structures, and mathematical modeling (vectors, matrices, tensors). While arrays provide rapid index-based lookups, modifying their structure (insertions and deletions) incurs shifting overhead because memory contiguity must be preserved. When modeling higher-dimensional grids, such as 2D matrices, spatial arrangement and transformations (rotations, transpositions) demand systematic index mapping. Furthermore, in scientific computing and graph theory, matrices are often **sparse**—consisting predominantly of zero elements. Storing full arrays for sparse structures wastes significant memory, motivating alternative representations such as the **3-tuple (Coordinate List) format**.

---

## 2. Aim

To study, implement, and analyze core 1D and 2D array operations, evaluate the memory efficiency of sparse matrix triple representation, and construct a robust, menu-driven matrix calculator in Python without external numerical libraries.

---

## 3. Learning Objectives

By completing this laboratory unit, students are able to:
1. Understand the memory layout and contiguity constraints of 1D and 2D arrays.
2. Implement insertion and deletion with manual element shifting.
3. Design and analyze in-place array rotation algorithms using reversal techniques.
4. Perform matrix transformations, including 90-degree clockwise rotation for square and rectangular dimensions.
5. Model sparse matrices using canonical 3-tuple format ($[rows, cols, values]$) and perform sparse arithmetic.
6. Evaluate storage trade-offs and calculate the mathematical break-even threshold for sparse storage optimization.
7. Build a matrix calculator supporting addition, multiplication, transpose, and determinant computation (Laplace cofactor expansion) with dimension validation.

---

## 4. Software Requirements

- **Programming Language**: Python 3.8+ (Pure Standard Library)
- **Operating System**: Linux (Ubuntu/Debian-based x86_64)
- **Execution Shell**: Bash Shell
- **Development Tooling**: Antigravity IDE / Terminal CLI
- **External Dependencies**: None (Standard Library only; NumPy and third-party libraries avoided intentionally to demonstrate foundational algorithm design).

---

## 5. Experiment 1: 1D Array Operations

### Problem Statement
Develop a modular, menu-driven Python program to perform standard 1D array operations:
1. Create and display an array.
2. Insert an element at an arbitrary valid index ($0 \le pos \le n$).
3. Delete an element from an arbitrary valid index ($0 \le pos < n$).
4. Search for a target value using linear search.
5. Rotate elements left and right by $k$ positions.
6. Validate all boundary conditions and handle empty arrays gracefully.

### Approach
In languages with static arrays, arrays are fixed blocks of memory. In Python, `list` is a dynamic array. To simulate low-level array behavior, insertion and deletion are implemented using manual element-by-element shifting rather than relying solely on built-in `.insert()` or `.pop(index)`. Rotation is implemented via the **Reversal Algorithm**, which operates in-place in $O(n)$ time and $O(1)$ auxiliary space.

### Algorithm

#### Insertion Algorithm (`insert_element`):
1. Receive array $A$, target $element$, and $position$.
2. Verify $0 \le position \le \text{length}(A)$. If invalid, raise `IndexError`.
3. Append a placeholder (`None`) to the end of $A$ to expand physical size by 1.
4. Starting from index $\text{length}(A) - 1$ down to $position + 1$, shift elements one slot right:
   $$A[i] \leftarrow A[i - 1]$$
5. Place $element$ at $A[position]$.

#### Deletion Algorithm (`delete_element`):
1. Check if array is empty ($\text{length}(A) == 0$). If so, raise `IndexError`.
2. Verify $0 \le position < \text{length}(A)$. If invalid, raise `IndexError`.
3. Store $deleted\_val \leftarrow A[position]$.
4. Shift elements leftward from $position$ up to $\text{length}(A) - 2$:
   $$A[i] \leftarrow A[i + 1]$$
5. Remove the trailing redundant slot using `pop()`.
6. Return $deleted\_val$.

#### Reversal Algorithm for Rotation:
- **Left Rotation by $k$**:
  1. $k \leftarrow k \pmod n$. If $k = 0$, return.
  2. Reverse subarray $A[0 \dots k-1]$.
  3. Reverse subarray $A[k \dots n-1]$.
  4. Reverse entire array $A[0 \dots n-1]$.
- **Right Rotation by $k$**:
  1. $k \leftarrow k \pmod n$. If $k = 0$, return.
  2. Reverse entire array $A[0 \dots n-1]$.
  3. Reverse subarray $A[0 \dots k-1]$.
  4. Reverse subarray $A[k \dots n-1]$.

### Pseudocode

```text
FUNCTION insert_element(A, element, pos):
    IF pos < 0 OR pos > len(A) THEN
        THROW IndexError
    APPEND None TO A
    FOR i FROM len(A) - 1 DOWNTO pos + 1 DO:
        A[i] = A[i - 1]
    A[pos] = element
END FUNCTION

FUNCTION delete_element(A, pos):
    IF len(A) == 0 OR pos < 0 OR pos >= len(A) THEN
        THROW IndexError
    val = A[pos]
    FOR i FROM pos TO len(A) - 2 DO:
        A[i] = A[i + 1]
    POP_LAST(A)
    RETURN val
END FUNCTION

FUNCTION rotate_left(A, k):
    n = len(A)
    IF n <= 1 THEN RETURN
    k = k MOD n
    REVERSE(A, 0, k - 1)
    REVERSE(A, k, n - 1)
    REVERSE(A, 0, n - 1)
END FUNCTION
```

### Sample Input / Output
```text
Array created: [10, 20, 30]

Insert '15' at position 1:
Index:   [0]    [1]    [2]    [3]
Value:   10     15     20     30

Delete at position 2:
Removed element: 20
Remaining array: [10, 15, 30]

Linear Search for 15:
Element '15' found at index/indices: [1]

Rotate Left by 1 position:
Array state: [15, 30, 10]

Rotate Right by 1 position:
Array state: [10, 15, 30]
```

### Dry Run
**Trace: Insert 15 at index 1 in `[10, 20, 30]` ($n=3$):**
1. Check bounds: $0 \le 1 \le 3$ (Valid).
2. Append placeholder: `[10, 20, 30, None]` (length = 4).
3. Loop $i = 3$: `A[3] = A[2] = 30` $\to$ `[10, 20, 30, 30]`.
4. Loop $i = 2$: `A[2] = A[1] = 20` $\to$ `[10, 20, 20, 30]`.
5. Place element: `A[1] = 15` $\to$ `[10, 15, 20, 30]`. Done.

**Trace: Rotate Left `[1, 2, 3, 4, 5]` by $k=2$ ($n=5$):**
1. $k = 2 \pmod 5 = 2$.
2. Reverse $A[0 \dots 1]$ (`[1, 2]`): `[2, 1, 3, 4, 5]`.
3. Reverse $A[2 \dots 4]$ (`[3, 4, 5]`): `[2, 1, 5, 4, 3]`.
4. Reverse entire array $A[0 \dots 4]$: `[3, 4, 5, 1, 2]`. Correct.

### Time and Space Complexity

| Operation | Best Case | Average Case | Worst Case | Auxiliary Space |
| :--- | :---: | :---: | :---: | :---: |
| **Insertion (at end)** | $O(1)$ | $O(n)$ | $O(n)$ (shift $n$ items) | $O(1)$ |
| **Insertion (at pos 0)** | $O(n)$ | $O(n)$ | $O(n)$ | $O(1)$ |
| **Deletion (from end)** | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ |
| **Deletion (from pos 0)** | $O(n)$ | $O(n)$ | $O(n)$ | $O(1)$ |
| **Linear Search** | $O(1)$ (target at index 0) | $O(n)$ | $O(n)$ (not found) | $O(k)$ matches |
| **Rotation (Reversal)** | $O(n)$ | $O(n)$ | $O(n)$ | $O(1)$ |

### Real-Life Applications
- **CPU Scheduling**: Ready queues and round-robin dispatching use cyclic array rotation.
- **Buffer Management**: Audio playback and video streaming frame ring buffers.
- **Undo Buffers**: Fixed-capacity history stacks with shifting deletion of oldest records.

---

## 6. Experiment 2: 2D Array Operations

### Problem Statement
Implement a 2D array (matrix) manipulation suite supporting:
1. Matrix initialization and structured grid rendering.
2. Element insertion (update) at coordinate $(r, c)$.
3. Element deletion (clearing to 0) at coordinate $(r, c)$.
4. 2D linear search returning all matching coordinates.
5. In-place / algorithmic 90-degree clockwise matrix rotation.
6. Validation against irregular (jagged) rows and out-of-bounds indices.

### Approach
A 2D array is modeled as a nested list of lists. Matrix regularity is strictly enforced: every row must be an independent list instance with identical length.
For rotation, every cell $(r, c)$ in an $M \times N$ matrix rotates clockwise to $(c, M - 1 - r)$ in an $N \times M$ matrix:
$$\text{Rotated}[c][M - 1 - r] = \text{Original}[r][c]$$
For a square $N \times N$ matrix, this transformation is equivalent to matrix transposition followed by horizontal row reversal.

### Algorithm

#### Validation (`validate_matrix`):
1. Ensure matrix is a non-empty list.
2. Ensure row count $M > 0$ and column count $N > 0$.
3. Check that every row $r$ satisfies $\text{length}(r) == N$. If unequal, raise `ValueError`.

#### 90-Degree Clockwise Rotation (`rotate_matrix_90_clockwise`):
1. Obtain dimensions $M, N$ via `validate_matrix`.
2. Allocate a new matrix of dimensions $N \times M$ filled with placeholders.
3. For each row $r$ from $0$ to $M - 1$:
   For each column $c$ from $0$ to $N - 1$:
   $$\text{Rotated}[c][M - 1 - r] = \text{Original}[r][c]$$
4. Return the rotated matrix.

### Pseudocode

```text
FUNCTION rotate_matrix_90_clockwise(M):
    rows, cols = validate_matrix(M)
    ALLOCATE R OF SIZE cols x rows
    FOR r FROM 0 TO rows - 1 DO:
        FOR c FROM 0 TO cols - 1 DO:
            R[c][rows - 1 - r] = M[r][c]
    RETURN R
END FUNCTION

FUNCTION search_2d(M, target):
    rows, cols = validate_matrix(M)
    matches = EMPTY_LIST
    FOR r FROM 0 TO rows - 1 DO:
        FOR c FROM 0 TO cols - 1 DO:
            IF M[r][c] == target THEN
                APPEND (r, c) TO matches
    RETURN matches
END FUNCTION
```

### Sample Input / Output
```text
Original Matrix (2 x 3):
       Col 0     Col 1     Col 2     
-------------------------------------
Row 0 | 1         2         3         
Row 1 | 4         5         6         
-------------------------------------

Rotated 90 Degrees Clockwise (3 x 2):
       Col 0     Col 1     
---------------------------
Row 0 | 4         1         
Row 1 | 5         2         
Row 2 | 6         3         
---------------------------

Four 90-degree rotations (360 deg) restore original matrix:
Verification Status: PASSED (Identity confirmed)
```

### Dry Run
**Trace: Rotate $2 \times 3$ matrix clockwise to $3 \times 2$:**
Original Matrix:
- Row 0: `[1, 2, 3]`
- Row 1: `[4, 5, 6]` ($M = 2, N = 3$).

1. New dimensions: $3 \times 2$.
2. Cell $(0, 0) = 1 \to \text{Rotated}[0][2 - 1 - 0] = \text{Rotated}[0][1] = 1$.
3. Cell $(0, 1) = 2 \to \text{Rotated}[1][2 - 1 - 0] = \text{Rotated}[1][1] = 2$.
4. Cell $(0, 2) = 3 \to \text{Rotated}[2][2 - 1 - 0] = \text{Rotated}[2][1] = 3$.
5. Cell $(1, 0) = 4 \to \text{Rotated}[0][2 - 1 - 1] = \text{Rotated}[0][0] = 4$.
6. Cell $(1, 1) = 5 \to \text{Rotated}[1][2 - 1 - 1] = \text{Rotated}[1][0] = 5$.
7. Cell $(1, 2) = 6 \to \text{Rotated}[2][2 - 1 - 1] = \text{Rotated}[2][0] = 6$.
Result: `[[4, 1], [5, 2], [6, 3]]`.

### Time and Space Complexity

| Operation | Complexity (Time) | Complexity (Auxiliary Space) | Remarks |
| :--- | :---: | :---: | :--- |
| **Matrix Creation** | $O(M \times N)$ | $O(M \times N)$ | Allocates independent list rows |
| **Element Access/Update** | $O(1)$ | $O(1)$ | Direct coordinate indexing |
| **Element Deletion (Zeroing)** | $O(1)$ | $O(1)$ | Resets cell to default |
| **2D Linear Search** | $O(M \times N)$ | $O(k)$ | Scans all grid coordinates |
| **90° Rotation** | $O(M \times N)$ | $O(M \times N)$ | $O(1)$ auxiliary possible for square in-place |

### Real-Life Applications
- **Digital Image Processing**: 90° image rotation, kernel convolution filters, and pixel manipulation.
- **Game Development**: Tilemaps, chessboard layouts, and 2D physics collision grids.
- **Geographic Information Systems (GIS)**: Elevation models and satellite raster grid analysis.

---

## 7. Experiment 3: Sparse Matrix (Triple Representation)

### 1. Sparse Matrix Concept
A matrix is considered **sparse** when the overwhelming majority of its elements have a value of zero. Storing a sparse matrix as a full 2D array wastes significant physical memory and causes redundant computation (e.g., adding or multiplying zeros).

### 2. Triple Representation (Coordinate List Format)
In canonical **3-tuple (triple) representation**:
- **Row 0 (Header Row)**: Stores metadata:
  $$\text{Header} = [\text{Total Rows } (M), \text{Total Columns } (N), \text{Non-Zero Elements } (K)]$$
- **Subsequent Rows (Rows $1 \dots K$)**: Store individual non-zero entries in row-major order:
  $$\text{Entry}_i = [\text{Row Index } (r), \text{Column Index } (c), \text{Non-Zero Value } (v)]$$

```text
Dense Matrix (4 x 4):           Triple Representation:
[ 0  0  3  0 ]                  Header : [4, 4, 3]
[ 0  5  0  0 ]                  Triple 1: [0, 2, 3]
[ 0  0  0  7 ]                  Triple 2: [1, 1, 5]
[ 0  0  0  0 ]                  Triple 3: [2, 3, 7]
```

### 3. Conversion and Reconstruction
- **Dense to Triple (`matrix_to_triple`)**: Scans the dense matrix row-by-row. When `matrix[r][c] != 0`, appends `[r, c, val]`. Header is prepended as `[rows, cols, K]`.
- **Triple to Dense (`triple_to_matrix`)**: Reads $M$ and $N$ from Header. Allocates an $M \times N$ matrix of zeros. Iterates through triples $1 \dots K$ and populates `matrix[r][c] = val`.

### 4. Basic Operations
- **Sparse Transpose (`transpose_sparse`)**:
  - Swap header dimensions: $[N, M, K]$.
  - For each triple $[r, c, v]$, swap row and col $\to [c, r, v]$.
  - Sort triples canonically by new row index, then new column index: $O(K \log K)$ time.
- **Sparse Addition (`add_sparse`)**:
  - Validates dimension equality ($M_A == M_B$ and $N_A == N_B$).
  - Utilizes a **Two-Pointer Linear Merge Algorithm** over sorted triples of $A$ and $B$:
    - If $\text{pos}_A < \text{pos}_B$: Append entry from $A$, advance pointer $A$.
    - If $\text{pos}_A > \text{pos}_B$: Append entry from $B$, advance pointer $B$.
    - If $\text{pos}_A == \text{pos}_B$: Compute $sum = v_A + v_B$. If $sum \neq 0$, append $[r, c, sum]$. If $sum == 0$ (cancellation), do **not** add to triples. Advance both pointers.
  - Linear execution time: $O(K_A + K_B)$.

### 5. Storage Comparison & Space Optimization

Let:
- $M$: Number of matrix rows.
- $N$: Number of matrix columns.
- $K$: Number of non-zero elements.
- $S$: Byte size per element (e.g., 4 bytes for standard integer).

$$\text{Dense Storage} = (M \times N) \times S \text{ bytes}$$

$$\text{Sparse Triple Storage} = 3 \times (K + 1) \times S \text{ bytes}$$

#### Break-Even / Crossover Threshold:
Sparse representation uses strictly less storage when:
$$3(K + 1) < M \times N \implies K < \frac{M \times N - 3}{3}$$

When non-zero elements constitute fewer than approximately **33.3%** of the matrix entries, sparse triple representation delivers substantial memory savings.

#### Mathematical Sparsity Percentage:
$$\text{Sparsity} = \left(\frac{M \times N - K}{M \times N}\right) \times 100\%$$

### 6. Algorithm, Pseudocode, and Dry Run

#### Pseudocode for Sparse Addition:
```text
FUNCTION add_sparse(T_A, T_B):
    IF T_A[0][0] != T_B[0][0] OR T_A[0][1] != T_B[0][1] THEN
        THROW ValueError("Dimension mismatch")
    
    i = 1, j = 1
    result_entries = EMPTY_LIST
    
    WHILE i < len(T_A) AND j < len(T_B) DO:
        posA = (T_A[i][0], T_A[i][1])
        posB = (T_B[j][0], T_B[j][1])
        
        IF posA < posB THEN
            APPEND T_A[i] TO result_entries; i = i + 1
        ELSE IF posA > posB THEN
            APPEND T_B[j] TO result_entries; j = j + 1
        ELSE
            sum_val = T_A[i][2] + T_B[j][2]
            IF sum_val != 0 THEN
                APPEND [posA[0], posA[1], sum_val] TO result_entries
            i = i + 1; j = j + 1
            
    WHILE i < len(T_A) DO: APPEND T_A[i++]; 
    WHILE j < len(T_B) DO: APPEND T_B[j++];
    
    RETURN [[T_A[0][0], T_A[0][1], len(result_entries)]] + result_entries
END FUNCTION
```

### Sample Input / Output
```text
Original Dense Matrix (3 x 3):
         [0]     [1]     [2]   
-------------------------------
[0]   |      0       0       5 
[1]   |      0       2       0 
[2]   |      0       0       0 
-------------------------------

Converted Triple Representation:
Header: Rows = 3, Columns = 3, Non-zero Elements = 2
--------------------------------------
Index   | Row     | Col     | Value   
--------------------------------------
0 (H)   | 3       | 3       | 2       
1       | 0       | 2       | 5       
2       | 1       | 1       | 2       
--------------------------------------

Sparse Transpose:
Header: Rows = 3, Columns = 3, Non-zero Elements = 2
Index 1: Row 1, Col 1, Value 2
Index 2: Row 2, Col 0, Value 5

Space Optimization Report (100 x 100 Matrix with 50 Non-zeros):
------------------------------------------------------------
Total Elements        : 10,000
Non-zero Elements (K) : 50
Matrix Sparsity       : 99.50%
Dense Storage (4B)    : 40,000 bytes
Sparse Storage (4B)   : 612 bytes
Savings               : 39,388 bytes (98.47% reduction)
Verdict               : SAVING: Sparse format saves 39388 bytes!
------------------------------------------------------------
```

### Time and Space Complexity

| Operation | Time Complexity | Auxiliary Space | Remarks |
| :--- | :---: | :---: | :--- |
| **Matrix to Triple** | $O(M \times N)$ | $O(K)$ | Full matrix scan |
| **Triple to Matrix** | $O(M \times N + K)$ | $O(M \times N)$ | Allocates full dense grid |
| **Sparse Transpose** | $O(K \log K)$ | $O(K)$ | Row/col swap followed by sort |
| **Sparse Addition** | $O(K_A + K_B)$ | $O(K_A + K_B)$ | Linear two-pointer merge |

---

## 8. Experiment 4: Matrix Calculator

### Problem Statement
Develop a self-contained, menu-driven Matrix Calculator implementing:
1. Matrix Addition ($A + B$)
2. Matrix Multiplication ($A \times B$)
3. Matrix Transpose ($A^T$)
4. Matrix Determinant ($\det(A)$) for square matrices ($N \times N$)
5. Strict dimension compatibility checking and non-square/singular matrix diagnostics without external libraries.

### Operations and Conditions

#### 1. Matrix Addition
- **Compatibility Condition**: $R_A = R_B$ and $C_A = C_B$.
- **Formula**: $C_{ij} = A_{ij} + B_{ij}$.
- **Complexity**: Time $O(R \times C)$, Space $O(R \times C)$.

#### 2. Matrix Multiplication
- **Compatibility Condition**: Number of columns in $A$ must equal number of rows in $B$ ($C_A = R_B$).
- **Formula**:
  $$C_{ij} = \sum_{k=0}^{C_A - 1} A_{ik} \times B_{kj}$$
- **Result Dimension**: $R_A \times C_B$.
- **Complexity**: Time $O(R_A \times C_A \times C_B)$, Space $O(R_A \times C_B)$.

#### 3. Matrix Transpose
- **Transformation**: Flips matrix over its diagonal ($T_{ji} = A_{ij}$).
- **Result Dimension**: If $A$ is $R \times C$, $A^T$ is $C \times R$.
- **Complexity**: Time $O(R \times C)$, Space $O(R \times C)$.

#### 4. Matrix Determinant
- **Compatibility Condition**: Must be a square matrix ($R = C = n$). Non-square matrices raise `ValueError`.
- **Algorithm (Laplace Cofactor Expansion)**:
  - Base Case $1 \times 1$: $\det([a]) = a$.
  - Base Case $2 \times 2$:
    $$\det\begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc$$
  - Base Case $3 \times 3$ (Direct Rule):
    $$\det(A) = a(ei - fh) - b(di - fg) + c(dh - eg)$$
  - General $n \times n$ recursive Laplace expansion along Row 0:
    $$\det(A) = \sum_{j=0}^{n-1} (-1)^j A_{0j} \det(M_{0j})$$
    where $M_{0j}$ is the $(n-1) \times (n-1)$ submatrix formed by dropping row 0 and column $j$.
- **Singular Matrix Diagnostic**: If $\det(A) = 0$, the matrix is classified as **singular** (non-invertible with linearly dependent rows/columns).
- **Complexity**: Time $O(n!)$, Space $O(n)$ recursion depth (well-suited for small educational matrices $n \le 4$).

### Sample Input / Output
```text
Matrix Addition Result:
 |       11      22 |
 |       33      44 |

Matrix Multiplication:
Matrix A (2 x 3) x Matrix B (3 x 2) -> Result (2 x 2):
 |       31      19 |
 |       85      55 |

Matrix Transpose:
Original A (2 x 3) -> Transpose A^T (3 x 2):
 |        1       4 |
 |        2       5 |
 |        3       6 |

Determinant (3 x 3 Non-Singular):
Matrix A:
 |        6       1       1 |
 |        4      -2       5 |
 |        2       8       7 |
Determinant det(A) = -306
Note: det(A) != 0 indicates that Matrix A is a NON-SINGULAR matrix (invertible).

Determinant (3 x 3 Singular):
Matrix:
 |        1       2       3 |
 |        4       5       6 |
 |        7       8       9 |
Determinant det(A) = 0
Note: det(A) = 0 indicates that Matrix A is a SINGULAR matrix (non-invertible).
```

---

## 9. Program Structure

```text
Lab01-Introduction-Arrays/
├── Program01-ArrayOperations/
│   └── array_operations.py
├── Program02-2DArrayOperations/
│   └── 2d_array_operations.py
├── Program03-SparseMatrix/
│   └── sparse_matrix.py
├── Program04-MatrixCalculator/
│   └── matrix_calculator.py
├── README.md
└── reflection.md
```

Each program is completely independent and executable both interactively and via automated testing with the `--test` flag:

```bash
python3 Lab01-Introduction-Arrays/Program01-ArrayOperations/array_operations.py --test
python3 Lab01-Introduction-Arrays/Program02-2DArrayOperations/2d_array_operations.py --test
python3 Lab01-Introduction-Arrays/Program03-SparseMatrix/sparse_matrix.py --test
python3 Lab01-Introduction-Arrays/Program04-MatrixCalculator/matrix_calculator.py --test
```

---

## 10. Testing and Sample Results

### Program 1: 1D Array Operations
```text
==========================================
Running Self-Tests for Program 1 (1D Arrays)
==========================================
[Test 1] Insert into empty array at index 0:
  Passed: [10]
[Test 2] Insert at beginning (index 0):
  Passed: [5, 10]
[Test 3] Insert at end (index len):
  Passed: [5, 10, 20]
[Test 4] Insert in the middle (index 1):
  Passed: [5, 8, 10, 20]
[Test 5] Invalid insert positions (boundary check):
  Passed: Negative index caught
  Passed: Out-of-bounds index caught
[Test 6] Delete from middle:
  Passed: Deleted 8, remaining: [5, 10, 20]
[Test 7] Delete from beginning (index 0):
  Passed: Deleted 5, remaining: [10, 20]
[Test 8] Delete from end:
  Passed: Deleted 20, remaining: [10]
[Test 9] Delete the last remaining element:
  Passed: Deleted 10, remaining is empty: []
[Test 10] Delete from empty array:
  Passed: Deletion from empty array rejected
[Test 11] Linear search for existing and missing elements:
  Passed: Search 25 -> positions [1, 3]
  Passed: Search 999 (missing) -> []
  Passed: Search in empty array -> []
[Test 12] Left rotation:
  Passed: [1,2,3,4,5] left rotated by 2 -> [3, 4, 5, 1, 2]
[Test 13] Right rotation:
  Passed: [1,2,3,4,5] right rotated by 2 -> [4, 5, 1, 2, 3]
[Test 14] Rotation boundary cases (k=0, k=len, k > len):
  Passed: Rotate by 0 leaves array unchanged
  Passed: Rotate by length leaves array unchanged
  Passed: Rotate by 7 (k > len) left rotated correctly -> [2, 3, 1]
  Passed: Rotation on empty array handled cleanly
All Program 1 self-tests PASSED successfully!
```

### Program 2: 2D Array Operations
```text
==========================================
Running Self-Tests for Program 2 (2D Arrays)
==========================================
[Test 1] Create 2x3 matrix:
  Passed: 2x3 zero matrix created
[Test 2] Dimension validation on irregular matrix:
  Passed: Caught irregular matrix (Irregular/jagged matrix detected)
[Test 3] Dimension validation on empty matrix:
  Passed: Caught empty matrix
[Test 4] Insertion at (0, 0), middle (0, 1), and boundary (1, 2):
  Passed: Matrix state is [[10, 20, 0], [0, 0, 99]]
[Test 5] Insertion with out-of-bounds indices:
  Passed: Row out-of-bounds caught
  Passed: Column out-of-bounds caught
[Test 6] Deletion (reset to 0) at (0, 1):
  Passed: Deleted 20, cell reset to 0
[Test 7] Deletion out-of-bounds:
  Passed: Negative index caught
[Test 8] Search for existing element:
  Passed: Found target 99 at coordinates [(1, 0), (1, 2)]
[Test 9] Search for non-existent element:
  Passed: Missing element returned []
[Test 10] Rotate 3x3 square matrix 90 degrees clockwise:
  Passed: Square matrix rotated 90 deg clockwise -> [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
[Test 11] Four 90-degree rotations equal original matrix (360 deg identity):
  Passed: 4 rotations restore original state
[Test 12] Rotate 2x3 rectangular matrix 90 degrees clockwise:
  Passed: 2x3 rotated into 3x2 matrix -> [[4, 1], [5, 2], [6, 3]]
All Program 2 self-tests PASSED successfully!
```

### Program 3: Sparse Matrix
```text
==========================================
Running Self-Tests for Program 3 (Sparse Matrix)
==========================================
[Test 1] Sparse matrix conversion and reconstruction:
  Passed: Triples generated: [[4, 4, 3], [0, 2, 3], [1, 1, 5], [2, 3, 7]]
  Passed: Matrix correctly reconstructed from triples
[Test 2] Completely zero matrix:
  Passed: Completely zero matrix handled correctly
[Test 3] 1x1 Matrix:
  Passed: 1x1 matrix converted and restored
[Test 4] Sparse transpose:
  Passed: Sparse transpose matches dense transpose correctly
[Test 5] Sparse matrix addition:
  Passed: Sparse addition matches dense sum: [[1, 0, 5], [0, 3, 4]]
[Test 6] Addition with cancellation to zero:
  Passed: Cancelling elements properly removed from non-zero triples
[Test 7] Incompatible dimension addition rejection:
  Passed: Caught dimension mismatch (Matrix A is 2x3, but Matrix B is 3x2)
[Test 8] Space optimization report generation:
  Passed: Space optimization calculation verified
All Program 3 self-tests PASSED successfully!
```

### Program 4: Matrix Calculator
```text
==========================================
Running Self-Tests for Program 4 (Matrix Calculator)
==========================================
[Test 1] Matrix Addition (Compatible 2x2):
  Passed: Addition correct -> [[6, 8], [10, 12]]
[Test 2] Matrix Addition (Incompatible dimensions):
  Passed: Dimension mismatch caught
[Test 3] Matrix Multiplication (Compatible 2x3 and 3x2 -> 2x2):
  Passed: Multiplication correct -> [[31, 19], [85, 55]]
[Test 4] Matrix Multiplication (Incompatible dimensions):
  Passed: Incompatible multiplication caught (cols(A) != rows(B))
[Test 5] Transpose (Rectangular 2x3 -> 3x2):
  Passed: Transpose of 2x3 -> 3x2 matches: [[1, 4], [2, 5], [3, 6]]
[Test 6] Determinant 1x1 Matrix:
  Passed: det([[42]]) = 42
[Test 7] Determinant 2x2 Matrix:
  Passed: det([[1, 2], [3, 4]]) = -2
[Test 8] Determinant 3x3 Matrix (Non-singular):
  Passed: det(3x3) = -306
[Test 9] Determinant of Singular Matrix (det = 0):
  Passed: Singular matrix correctly identified with determinant = 0
[Test 10] Determinant of Non-Square Matrix Rejection:
  Passed: Non-square determinant rejected (ValueError)
All Program 4 self-tests PASSED successfully!
```

---

## 11. Performance and Complexity Analysis

| Program | Operation | Time Complexity (Best) | Time Complexity (Average/Worst) | Auxiliary Space Complexity | Primary Constraint / Factor |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Prog 1 (1D)** | Insert Element | $O(1)$ (at end) | $O(n)$ | $O(1)$ | Contiguous element shifting |
| **Prog 1 (1D)** | Delete Element | $O(1)$ (from end) | $O(n)$ | $O(1)$ | Contiguous element shifting |
| **Prog 1 (1D)** | Linear Search | $O(1)$ (target at 0) | $O(n)$ | $O(k)$ | Sequential element comparison |
| **Prog 1 (1D)** | Left / Right Rotation | $O(n)$ | $O(n)$ | $O(1)$ | 3 array reversals |
| **Prog 2 (2D)** | Cell Access / Update | $O(1)$ | $O(1)$ | $O(1)$ | Direct coordinate indexing |
| **Prog 2 (2D)** | 2D Linear Search | $O(1)$ | $O(M \times N)$ | $O(k)$ | Full grid traversal |
| **Prog 2 (2D)** | 90° Clockwise Rotation| $O(M \times N)$ | $O(M \times N)$ | $O(M \times N)$ | Grid coordinate remap |
| **Prog 3 (Sparse)**| Convert / Reconstruct | $O(M \times N)$ | $O(M \times N)$ | $O(K)$ / $O(M \times N)$ | Grid scanning / allocation |
| **Prog 3 (Sparse)**| Sparse Transpose | $O(K)$ | $O(K \log K)$ | $O(K)$ | Coordinate swap & sort |
| **Prog 3 (Sparse)**| Sparse Addition | $O(1)$ | $O(K_A + K_B)$ | $O(K_A + K_B)$ | Two-pointer sorted merge |
| **Prog 4 (Calc)** | Matrix Addition | $O(R \times C)$ | $O(R \times C)$ | $O(R \times C)$ | Equal dimension matching |
| **Prog 4 (Calc)** | Matrix Multiplication | $O(M \times K \times N)$ | $O(M \times K \times N)$ | $O(M \times N)$ | Inner dimension condition |
| **Prog 4 (Calc)** | Matrix Transpose | $O(R \times C)$ | $O(R \times C)$ | $O(R \times C)$ | Coordinate inversion |
| **Prog 4 (Calc)** | Matrix Determinant | $O(1)$ ($1 \times 1, 2 \times 2$) | $O(n!)$ | $O(n)$ | Square matrix; Laplace expansion |

---

## 12. Learning Outcomes

1. **Memory Contiguity**: Experienced how contiguous arrays demand explicit element shifting during insertion and deletion.
2. **Algorithmic Efficiency**: Mastered in-place array rotation via the reversal technique, reducing auxiliary space from $O(n)$ to $O(1)$.
3. **Multidimensional Indexing**: Understood row-major memory mapping and coordinate transformations for 90-degree matrix rotations across square and rectangular shapes.
4. **Data Compression in DSA**: Proved analytically and empirically that sparse triple representation cuts memory consumption significantly when non-zero elements comprise $< 33.3\%$ of the matrix.
5. **Robust Engineering**: Implemented defensive programming through input validation, dimensional checks, singular matrix detection, and built-in self-tests.

---

## 13. References

1. Horowitz, E., Sahni, S., & Anderson-Freed, S. *Fundamentals of Data Structures in C* (2nd ed.). Silicon Press.
2. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. *Introduction to Algorithms* (3rd ed.). MIT Press.
3. Python Software Foundation. *Python 3.10+ Standard Library Documentation: Data Structures & Built-in Types*.
4. Strang, G. *Introduction to Linear Algebra* (5th ed.). Wellesley-Cambridge Press.

