# Data Structures and Algorithms Laboratory

**Course Code:** IC-307D  
**Course Title:** Data Structures and Algorithms Laboratory  
**Student:** Jeet Verma  
**Roll Number:** IC-2K23-46  
**Department:** Department of Computer Science & Engineering  
**Institution:** International Institute of Professional Studies (IIPS), Devi Ahilya Vishwavidyalaya (DAVV), Indore, Madhya Pradesh, India  
**Academic Term:** 2026–2027  
**Implementation Language:** Python 3.8+  
**Dependencies:** Python Standard Library  

---

## Table of Contents

1. [Introduction](#introduction)
2. [Educational Objectives](#educational-objectives)
3. [Technology Stack & Implementation Principles](#technology-stack-implementation-principles)
4. [Repository Architecture & Directory Tree](#repository-architecture-directory-tree)
5. [Unit-by-Unit Technical Breakdown](#unit-by-unit-technical-breakdown)
   - [Unit 1: Arrays & Matrices](#unit-1-arrays-matrices)
   - [Unit 2: Sorting & Searching](#unit-2-sorting-searching)
   - [Unit 3: Linked Lists](#unit-3-linked-lists)
   - [Unit 4: Stacks](#unit-4-stacks)
   - [Unit 5: Queues](#unit-5-queues)
   - [Unit 6: Trees](#unit-6-trees)
   - [Unit 7: Graphs](#unit-7-graphs)
6. [Capstone Project: Pathfinding Visualizer](#capstone-project-pathfinding-visualizer)
7. [Documentation & Visual Assets](#documentation-visual-assets)
8. [Algorithmic Complexity & Performance Analysis](#algorithmic-complexity-performance-analysis)
9. [Execution Guide & Verification](#execution-guide-verification)
10. [Curricular Learning Outcomes](#curricular-learning-outcomes)
11. [Academic Navigation Directory](#academic-navigation-directory)
12. [Conclusion](#conclusion)

---

## Introduction

This repository contains the complete laboratory curriculum, algorithmic implementations, formal performance analyses, and system applications for **IC-307D: Data Structures and Algorithms Laboratory**. 

The laboratory comprises **53 distinct programs** spanning **seven core units**—from contiguous arrays and empirical sorting comparisons to pointer-linked structures, hierarchical trees, and graph traversal networks. Every algorithmic routine and data structure in this repository is built strictly **from first principles using Python's standard library**, deliberately eschewing high-level container abstractions (such as `collections.deque`, `queue.Queue`, `heapq`, or `bisect`). 

By implementing pointer dereferencing, manual buffer shifting, linked node management, balance-factor rotations, and relaxation routines manually, this repository bridges abstract computer science theory with transparent, verifiable software engineering.

---

## Educational Objectives

The academic objectives of this laboratory course are:

- **Master Core Data Structures**: Understand the fundamental memory representations, structural properties, and access constraints of linear (arrays, linked lists, stacks, queues) and non-linear (trees, graphs, heaps) data structures.
- **Implement from First Principles**: Construct data structures and operations manually to observe low-level mechanics such as element shifting, dynamic pointer reassignment, balance factor tracking, and recursive call frames.
- **Analyze Time and Space Complexity**: Establish rigorous asymptotic bounds ($\mathcal{O}$, $\Omega$, $\Theta$) for best, average, and worst-case execution time, alongside auxiliary space footprints.
- **Evaluate Algorithmic Trade-offs**: Contrast competing paradigms—such as contiguous cache locality vs. dynamic pointer flexibility, recursive vs. iterative traversals, and adjacency matrices vs. adjacency lists.
- **Cultivate Engineering Rigor**: Implement defensive programming principles, comprehensive input validation, dimensional error handling, and self-testing assertion harnesses across all modules.
- **Deliver Applied Software Systems**: Integrate pure algorithmic primitives into functional applications, including matrix calculators, dictionary search engines, text editor buffers, expression evaluators, CPU schedulers, and maze solvers.

---

## Technology Stack & Implementation Principles

### Core Stack
- **Language**: Python 3.8+ (Pure Standard Library)
- **Mathematical & System Utilities**: `sys`, `time`, `math`, `os`
- **Plotting & Benchmarking Utilities**: `matplotlib` (used solely for empirical sorting visualization plots in Lab 2)
- **Documentation & Modeling**: PlantUML (`.puml`) and ReportLab 5.1.0 (for publication-grade PDF reports and flowcharts)

### Implementation Principles
1. **Zero External Data Structure Dependencies**: No third-party data structures or pre-built algorithms are utilized. All queues, priority heaps, linked nodes, trees, and graphs are constructed from basic classes and primitive lists.
2. **Defensive Invariant Validation**: Operations enforce structural integrity checks (e.g., stack underflow/overflow, division-by-zero, negative edge rejection in Dijkstra, cycle detection, and matrix dimension mismatch).
3. **Dual Execution Mode**: Each program functions both as a standalone interactive console utility and as an automated test suite executed via the `--test` command-line flag.
4. **Clean Code & Modularity**: Methods adhere to standard algorithmic naming conventions (`push`, `pop`, `enqueue`, `dequeue`, `sift_down`, `rotate_left`, `insert`, `search`, `delete`).

---

## Repository Architecture & Directory Tree

```
Data_structures/
├── Lab01-Introduction-Arrays/
│   ├── Program01-ArrayOperations/
│   │   └── array_operations.py
│   ├── Program02-2DArrayOperations/
│   │   └── 2d_array_operations.py
│   ├── Program03-SparseMatrix/
│   │   └── sparse_matrix.py
│   ├── Program04-MatrixCalculator/
│   │   └── matrix_calculator.py
│   ├── README.md
│   └── reflection.md
├── Lab02-Sorting-Searching/
│   ├── Program01-BubbleSort/
│   │   └── bubble_sort.py
│   ├── Program02-SelectionSort/
│   │   └── selection_sort.py
│   ├── Program03-InsertionSort/
│   │   └── insertion_sort.py
│   ├── Program04-MergeSort/
│   │   └── merge_sort.py
│   ├── Program05-QuickSort/
│   │   └── quick_sort.py
│   ├── Program06-HeapSort/
│   │   └── heap_sort.py
│   ├── Program07-RadixSort/
│   │   └── radix_sort.py
│   ├── Program08-BinarySearch/
│   │   └── binary_search.py
│   ├── Program09-PerformanceAnalysis/
│   │   └── sorting_comparison.py
│   ├── Program10-StudentRecordManager/
│   │   └── student_record_manager.py
│   ├── Program11-SearchEngineSimulator/
│   │   └── search_engine.py
│   ├── outputs/
│   │   ├── sorting_comparison_all.png
│   │   ├── sorting_comparison_random.png
│   │   ├── sorting_comparison_reverse.png
│   │   └── sorting_comparison_sorted.png
│   ├── README.md
│   └── reflection.md
├── Lab03-Linked-Lists/
│   ├── Program01-SinglyLinkedList/
│   │   └── singly_linked_list.py
│   ├── Program02-DoublyLinkedList/
│   │   └── doubly_linked_list.py
│   ├── Program03-CircularLinkedList/
│   │   └── circular_linked_list.py
│   ├── Program04-PolynomialOperations/
│   │   └── polynomial_operations.py
│   ├── Program05-TextEditorBuffer/
│   │   └── text_editor_buffer.py
│   ├── Program06-PlaylistManager/
│   │   └── playlist_manager.py
│   ├── README.md
│   └── reflection.md
├── Lab04-Stacks/
│   ├── Program01-StaticStack/
│   │   └── static_stack.py
│   ├── Program02-DynamicStack/
│   │   └── dynamic_stack.py
│   ├── Program03-InfixToPostfix/
│   │   └── infix_to_postfix.py
│   ├── Program04-InfixToPrefix/
│   │   └── infix_to_prefix.py
│   ├── Program05-PostfixEvaluation/
│   │   └── postfix_evaluation.py
│   ├── Program06-PrefixEvaluation/
│   │   └── prefix_evaluation.py
│   ├── Program07-ExpressionEvaluator/
│   │   └── expression_evaluator.py
│   ├── Program08-UndoRedo/
│   │   └── undo_redo.py
│   ├── README.md
│   └── reflection.md
├── Lab05-Queues/
│   ├── Program01-StaticQueue/
│   │   └── static_queue.py
│   ├── Program02-DynamicQueue/
│   │   └── dynamic_queue.py
│   ├── Program03-CircularQueue/
│   │   └── circular_queue.py
│   ├── Program04-Deque/
│   │   └── deque.py
│   ├── Program05-ArrayPriorityQueue/
│   │   └── array_priority_queue.py
│   ├── Program06-HeapPriorityQueue/
│   │   └── heap_priority_queue.py
│   ├── Program07-CustomerServiceSimulation/
│   │   └── customer_service.py
│   ├── Program08-ProcessScheduling/
│   │   └── process_scheduling.py
│   ├── README.md
│   └── reflection.md
├── Lab06-Trees/
│   ├── Program01-RecursiveTraversals/
│   │   └── recursive_traversals.py
│   ├── Program02-IterativeTraversals/
│   │   └── iterative_traversals.py
│   ├── Program03-BinarySearchTree/
│   │   └── binary_search_tree.py
│   ├── Program04-AVLTree/
│   │   └── avl_tree.py
│   ├── Program05-ExpressionTree/
│   │   └── expression_tree.py
│   ├── Program06-FileSystemSimulator/
│   │   └── file_system.py
│   ├── Program07-SymbolTable/
│   │   └── symbol_table.py
│   ├── README.md
│   └── reflection.md
├── Lab07-Graphs/
│   ├── Program01-AdjacencyMatrix/
│   │   └── adjacency_matrix.py
│   ├── Program02-AdjacencyList/
│   │   └── adjacency_list.py
│   ├── Program03-BFS/
│   │   └── bfs.py
│   ├── Program04-RecursiveDFS/
│   │   └── recursive_dfs.py
│   ├── Program05-IterativeDFS/
│   │   └── iterative_dfs.py
│   ├── Program06-Dijkstra/
│   │   └── dijkstra.py
│   ├── Program07-SocialNetwork/
│   │   └── social_network.py
│   ├── Program08-MazeSolver/
│   │   └── maze_solver.py
│   ├── Program09-CoursePrerequisites/
│   │   └── course_prerequisites.py
│   ├── README.md
│   └── reflection.md
├── Capstone-Projects/
│   └── Pathfinding-Visualizer/
│       ├── pathfinding_visualizer.py
│       ├── gui.py
│       ├── README.md
│       ├── reflection.md
│       └── tests/
│           ├── test_pathfinding.py
│           └── test_gui.py
└── docs/
    ├── algorithm-flowcharts/
    │   ├── 01_array_operations.png
    │   ├── 01_array_operations.puml
    │   ├── 02_sorting_and_searching.png
    │   ├── 02_sorting_and_searching.puml
    │   ├── 03_linked_list_operations.png
    │   ├── 03_linked_list_operations.puml
    │   ├── 04_infix_to_postfix_and_eval.png
    │   ├── 04_infix_to_postfix_and_eval.puml
    │   ├── 05_circular_queue_and_round_robin.png
    │   ├── 05_circular_queue_and_round_robin.puml
    │   ├── 06_bst_operations.png
    │   ├── 06_bst_operations.puml
    │   ├── 07_avl_insertion_and_rotations.png
    │   ├── 07_avl_insertion_and_rotations.puml
    │   ├── 08_bfs_dfs_and_dijkstra.png
    │   └── 08_bfs_dfs_and_dijkstra.puml
    ├── diagrams/
    │   ├── 01_arrays_and_2d_arrays.png
    │   ├── 01_arrays_and_2d_arrays.puml
    │   ├── 02_sparse_matrix.png
    │   ├── 02_sparse_matrix.puml
    │   ├── 03_singly_linked_list.png
    │   ├── 03_singly_linked_list.puml
    │   ├── 04_doubly_linked_list.png
    │   ├── 04_doubly_linked_list.puml
    │   ├── 05_circular_linked_list.png
    │   ├── 05_circular_linked_list.puml
    │   ├── 06_stack.png
    │   ├── 06_stack.puml
    │   ├── 07_queue_and_circular_queue.png
    │   ├── 07_queue_and_circular_queue.puml
    │   ├── 08_priority_queue_and_heap.png
    │   ├── 08_priority_queue_and_heap.puml
    │   ├── 09_binary_search_tree.png
    │   ├── 09_binary_search_tree.puml
    │   ├── 10_avl_tree.png
    │   ├── 10_avl_tree.puml
    │   ├── 11_graph_representations.png
    │   └── 11_graph_representations.puml
    ├── complexity-analysis.pdf
    ├── final-report.pdf
    └── presentation.pdf
```

---

## Unit-by-Unit Technical Breakdown

### Unit 1: Arrays & Matrices
- **Documentation**: [Lab01 README](Lab01-Introduction-Arrays/README.md) | [Lab01 Reflection](Lab01-Introduction-Arrays/reflection.md)
- **Theoretical Basis**: Contiguous memory allocation, index-based offset arithmetic $\text{Address}(A[i]) = \text{Base} + i \times \text{Size}$, row-major storage for multi-dimensional spaces, and coordinate list compression for sparse matrices.
- **Concepts Covered**: Contiguous buffer allocation, index shifting on insertion/deletion, in-place triple-reversal block rotation, row/column transformations, 90° clockwise matrix rotation, coordinate tuple representation ($[r, c, v]$), and Laplace cofactor expansion for determinants.

| Program | File Path | Description | Key Algorithms & Principles |
| :--- | :--- | :--- | :--- |
| **Program 1** | `Lab01-Introduction-Arrays/Program01-ArrayOperations/array_operations.py` | 1D array manipulation engine | Manual element shifting for index insertion/deletion, linear search with multiple occurrence tracking, and $\mathcal{O}(n)$ in-place triple reversal rotation. |
| **Program 2** | `Lab01-Introduction-Arrays/Program02-2DArrayOperations/2d_array_operations.py` | 2D matrix transformation suite | Row-wise/column-wise summation, principal/secondary diagonal extraction, in-place matrix transposition, and 90° clockwise matrix rotation. |
| **Program 3** | `Lab01-Introduction-Arrays/Program03-SparseMatrix/sparse_matrix.py` | Sparse matrix compression engine | Canonical 3-tuple coordinate list representation, sparse addition, sparse matrix transpose, and mathematical break-even memory threshold analysis ($K < \frac{M \cdot N - 3}{3}$). |
| **Program 4** | `Lab01-Introduction-Arrays/Program04-MatrixCalculator/matrix_calculator.py` | Command-line matrix calculator | Validated dimension addition, matrix multiplication ($\mathcal{O}(M \cdot K \cdot N)$), transpose, and recursive Laplace cofactor expansion for determinants ($\mathcal{O}(N!)$). |

---

### Unit 2: Sorting & Searching
- **Documentation**: [Lab02 README](Lab02-Sorting-Searching/README.md) | [Lab02 Reflection](Lab02-Sorting-Searching/reflection.md)
- **Theoretical Basis**: Comparison lower bounds ($\Omega(n \log n)$ via decision tree leaves $n!$), stable vs. unstable permutations, divide-and-conquer recurrences, binary heap properties, non-comparison linear-time sorting (LSD Radix Sort), and collision resolution in open vs. closed hashing.
- **Concepts Covered**: Quadratic sorting, log-linear divide-and-conquer, in-place binary max heap, non-comparison bucket distribution, bisection searching, polynomial rolling hash functions, separate chaining, and linear probing.

| Program | File Path | Description | Key Algorithms & Principles |
| :--- | :--- | :--- | :--- |
| **Program 1** | `Lab02-Sorting-Searching/Program01-BubbleSort/bubble_sort.py` | Adjacent exchange sorting | Adaptive $\mathcal{O}(n)$ early-exit termination flag on pre-sorted arrays, step-by-step pass logging. |
| **Program 2** | `Lab02-Sorting-Searching/Program02-SelectionSort/selection_sort.py` | Minimum selection sorting | Unconditional $\Theta(n^2)$ comparison loop, minimal element write/swap count ($\le n-1$). |
| **Program 3** | `Lab02-Sorting-Searching/Program03-InsertionSort/insertion_sort.py` | Online incremental insertion | Adaptive shifting sort; optimal $\mathcal{O}(n)$ runtime on nearly-sorted data, stable ordering. |
| **Program 4** | `Lab02-Sorting-Searching/Program04-MergeSort/merge_sort.py` | Divide-and-conquer bisection sort | Out-of-place stable merge subroutine; deterministic $\Theta(n \log n)$ time and $\mathcal{O}(n)$ auxiliary space. |
| **Program 5** | `Lab02-Sorting-Searching/Program05-QuickSort/quick_sort.py` | Partitioning sort with Hoare scheme | Median-of-three pivot selection to defend against sorted input degradation, in-place partitioning. |
| **Program 6** | `Lab02-Sorting-Searching/Program06-HeapSort/heap_sort.py` | Priority tree selection sort | In-place $\mathcal{O}(n)$ Floyd heapify construction followed by repeated max-extraction and sift-down. |
| **Program 7** | `Lab02-Sorting-Searching/Program07-RadixSort/radix_sort.py` | Non-comparison digit sort | Least Significant Digit (LSD) sorting using stable base-10 counting sort subroutines in $\mathcal{O}(d(n+b))$ time. |
| **Program 8** | `Lab02-Sorting-Searching/Program08-BinarySearch/binary_search.py` | Logarithmic search algorithm | Both iterative and recursive implementations, search space bisection, overflow-safe midpoint calculation. |
| **Program 9** | `Lab02-Sorting-Searching/Program09-PerformanceAnalysis/sorting_comparison.py` | Empirical benchmarking harness | Automated execution timing across input distributions (random, sorted, reverse) with generated visual charts. |
| **Program 10** | `Lab02-Sorting-Searching/Program10-StudentRecordManager/student_record_manager.py` | In-memory student records system | Multi-attribute sorting (roll number, GPA, name) using Merge Sort and Binary Search on sorted keys. |
| **Program 11** | `Lab02-Sorting-Searching/Program11-SearchEngineSimulator/search_engine.py` | Document indexer & lookup engine | Custom hash tables featuring polynomial rolling hash ($s[i] \cdot p^i \pmod m$), Separate Chaining, and Linear Probing. |

---

### Unit 3: Linked Lists
- **Documentation**: [Lab03 README](Lab03-Linked-Lists/README.md) | [Lab03 Reflection](Lab03-Linked-Lists/reflection.md)
- **Theoretical Basis**: Dynamic heap node allocation, explicit reference maintenance (`next`, `prev`), non-contiguous memory addressing, pointer-based insertion/deletion without element shifting, and cyclic reference topologies.
- **Concepts Covered**: Singly linked lists, doubly linked lists with bi-directional navigation, circular linked lists, pointer reversal, Floyd's cycle finding algorithm, polynomial arithmetic, gap/node text buffer manipulation, and circular playlist looping.

| Program | File Path | Description | Key Algorithms & Principles |
| :--- | :--- | :--- | :--- |
| **Program 1** | `Lab03-Linked-Lists/Program01-SinglyLinkedList/singly_linked_list.py` | Unidirectional linked list | Head/tail/index insertion, deletion by value/position, in-place iterative reversal ($\mathcal{O}(n)$ time, $\mathcal{O}(1)$ space), and search. |
| **Program 2** | `Lab03-Linked-Lists/Program02-DoublyLinkedList/doubly_linked_list.py` | Bidirectional linked list | Two-way node pointers (`next`, `prev`), forward and backward traversals, and $\mathcal{O}(1)$ boundary insertions and removals. |
| **Program 3** | `Lab03-Linked-Lists/Program03-CircularLinkedList/circular_linked_list.py` | Closed-loop circular list | Tail-pointer tracking where `tail.next == head`, cyclic traversals, and circular insertions/deletions. |
| **Program 4** | `Lab03-Linked-Lists/Program04-PolynomialOperations/polynomial_operations.py` | Symbolic polynomial engine | Exponent-descending linked node storage, linear polynomial addition, subtraction, and term-by-term multiplication. |
| **Program 5** | `Lab03-Linked-Lists/Program05-TextEditorBuffer/text_editor_buffer.py` | Interactive text line buffer | Doubly linked line representation supporting cursor navigation, line insertion, deletion, and file saving/loading. |
| **Program 6** | `Lab03-Linked-Lists/Program06-PlaylistManager/playlist_manager.py` | Circular audio playlist manager | Circular doubly linked list supporting next/previous song skips, infinite playback cycling, and playlist rearrangement. |

---

### Unit 4: Stacks
- **Documentation**: [Lab04 README](Lab04-Stacks/README.md) | [Lab04 Reflection](Lab04-Stacks/reflection.md)
- **Theoretical Basis**: Last-In, First-Out (LIFO) operational discipline, stack overflow and underflow boundaries, activation record frames, operator precedence hierarchies, and Dijkstra's Shunting-Yard algorithm.
- **Concepts Covered**: Fixed-capacity array stacks, unbound dynamic linked stacks, balanced delimiter parsing, infix-to-postfix and infix-to-prefix conversions, postfix and prefix operand evaluations, full arithmetic expression parsing, and command pattern undo/redo state histories.

| Program | File Path | Description | Key Algorithms & Principles |
| :--- | :--- | :--- | :--- |
| **Program 1** | `Lab04-Stacks/Program01-StaticStack/static_stack.py` | Fixed-capacity stack | Array-backed buffer enforcing maximum capacity, top index pointer, and strict overflow/underflow exception guards. |
| **Program 2** | `Lab04-Stacks/Program02-DynamicStack/dynamic_stack.py` | Heap-linked dynamic stack | Node-based pointer chain offering unbounded capacity, $\mathcal{O}(1)$ push and pop without reallocation penalties. |
| **Program 3** | `Lab04-Stacks/Program03-InfixToPostfix/infix_to_postfix.py` | Shunting-Yard conversion | Operator precedence ranking, left-to-right scanning, operand queuing, and parenthesis scoping. |
| **Program 4** | `Lab04-Stacks/Program04-InfixToPrefix/infix_to_prefix.py` | Polish notation converter | Reversal of infix tokens, inverted parenthesis matching, Shunting-Yard translation, and post-conversion reversal. |
| **Program 5** | `Lab04-Stacks/Program05-PostfixEvaluation/postfix_evaluation.py` | Postfix expression evaluator | Single-pass operand stacking, operator popping, execution of basic operations (`+`, `-`, `*`, `/`, `^`), and division-by-zero checks. |
| **Program 6** | `Lab04-Stacks/Program06-PrefixEvaluation/prefix_evaluation.py` | Prefix expression evaluator | Right-to-left token scanning, operand stack caching, and deterministic evaluation. |
| **Program 7** | `Lab04-Stacks/Program07-ExpressionEvaluator/expression_evaluator.py` | End-to-end arithmetic calculator | Multi-digit tokenizer, bracket syntax validation, infix-to-postfix transformation, and computational evaluation. |
| **Program 8** | `Lab04-Stacks/Program08-UndoRedo/undo_redo.py` | Dual-stack history manager | Dual-stack operational tracking (`undo_stack`, `redo_stack`) supporting reversible text state transitions. |

---

### Unit 5: Queues
- **Documentation**: [Lab05 README](Lab05-Queues/README.md) | [Lab05 Reflection](Lab05-Queues/reflection.md)
- **Theoretical Basis**: First-In, First-Out (FIFO) operational discipline, false overflow in linear arrays, modulo index arithmetic for circular queues, double-ended queues (deque), priority heaps, and discrete-event simulation modeling.
- **Concepts Covered**: Linear static and dynamic queues, circular modulo wrap-around buffers, double-ended queues (deques), unordered array priority queues, complete binary min-heaps, Round-Robin CPU scheduling, and bank customer service queuing.

| Program | File Path | Description | Key Algorithms & Principles |
| :--- | :--- | :--- | :--- |
| **Program 1** | `Lab05-Queues/Program01-StaticQueue/static_queue.py` | Fixed linear array queue | Front and rear index tracking, boundary checking, and demonstration of false overflow under repeated dequeues. |
| **Program 2** | `Lab05-Queues/Program02-DynamicQueue/dynamic_queue.py` | Dynamic linked queue | Singly linked node list maintaining explicit `front` and `rear` pointers for guaranteed $\mathcal{O}(1)$ enqueue and dequeue. |
| **Program 3** | `Lab05-Queues/Program03-CircularQueue/circular_queue.py` | Modulo wrap-around queue | Circular index math (`rear = (rear + 1) % capacity`), eliminating false overflow and recycling deallocated buffer slots. |
| **Program 4** | `Lab05-Queues/Program04-Deque/deque.py` | Double-ended queue | Doubly linked queue supporting constant-time $\mathcal{O}(1)$ insertions and removals at both `front` and `rear`. |
| **Program 5** | `Lab05-Queues/Program05-ArrayPriorityQueue/array_priority_queue.py` | Unordered array priority queue | $\mathcal{O}(1)$ enqueue with linear scan $\mathcal{O}(n)$ minimum extraction; baseline priority queue model. |
| **Program 6** | `Lab05-Queues/Program06-HeapPriorityQueue/heap_priority_queue.py` | Binary min-heap priority queue | Complete binary tree in contiguous list; logarithmic $\mathcal{O}(\log n)$ insertion (`sift_up`) and extraction (`sift_down`). |
| **Program 7** | `Lab05-Queues/Program07-CustomerServiceSimulation/customer_service.py` | Multi-teller bank simulator | Discrete-event queuing simulation computing arrival rates, customer waiting times, and teller utilization. |
| **Program 8** | `Lab05-Queues/Program08-ProcessScheduling/process_scheduling.py` | Round-Robin CPU scheduler | Circular queue process dispatching under fixed time quantum, calculating turnaround and response metrics. |

---

### Unit 6: Trees
- **Documentation**: [Lab06 README](Lab06-Trees/README.md) | [Lab06 Reflection](Lab06-Trees/reflection.md)
- **Theoretical Basis**: Hierarchical non-linear topologies, recursive structural definitions, binary search invariants ($L < P < R$), tree balance factor tracking ($\text{BF} \in \{-1, 0, +1\}$), AVL self-balancing rotations, expression syntax trees, and multi-way directory trees.
- **Concepts Covered**: Preorder, Inorder, Postorder, and Level-Order traversals (recursive and iterative with explicit stacks/queues), BST insertion/search/deletion, AVL Tree rotations (LL, RR, LR, RL), expression tree construction from postfix tokens, hierarchical file systems, and compiler symbol tables.

| Program | File Path | Description | Key Algorithms & Principles |
| :--- | :--- | :--- | :--- |
| **Program 1** | `Lab06-Trees/Program01-RecursiveTraversals/recursive_traversals.py` | Recursive tree traversals | Depth-first traversals (Inorder, Preorder, Postorder) and Level-order traversal using queue BFS. |
| **Program 2** | `Lab06-Trees/Program02-IterativeTraversals/iterative_traversals.py` | Explicit-stack iterative traversals | Iterative Inorder, Preorder, and Postorder traversals utilizing explicit Python lists as call-stacks. |
| **Program 3** | `Lab06-Trees/Program03-BinarySearchTree/binary_search_tree.py` | Binary Search Tree (BST) | Search, insert, and 3-case node deletion (leaf, single-child, two-children via in-order successor). |
| **Program 4** | `Lab06-Trees/Program04-AVLTree/avl_tree.py` | Self-balancing AVL tree | Dynamic height and balance factor tracking; Left and Right single and double rotations maintaining $\mathcal{O}(\log n)$ height. |
| **Program 5** | `Lab06-Trees/Program05-ExpressionTree/expression_tree.py` | Syntax expression tree | Builds binary syntax tree from postfix tokens; recursive expression evaluation and prefix/infix/postfix reconstruction. |
| **Program 6** | `Lab06-Trees/Program06-FileSystemSimulator/file_system.py` | Hierarchical directory tree | N-ary tree modeling file system paths, directory creation (`mkdir`), path traversal (`cd`), listing (`ls`), and file storage. |
| **Program 7** | `Lab06-Trees/Program07-SymbolTable/symbol_table.py` | Compiler symbol table | Scoped symbol table implemented via Binary Search Tree supporting variable scoping, lookup, and lexical binding. |

---

### Unit 7: Graphs
- **Documentation**: [Lab07 README](Lab07-Graphs/README.md) | [Lab07 Reflection](Lab07-Graphs/reflection.md)
- **Theoretical Basis**: Relational networks $G=(V, E)$, directed and undirected graphs, dense matrix representations ($\mathcal{O}(V^2)$) vs. sparse adjacency lists ($\mathcal{O}(V + E)$), vertex color states (white/gray/black), queue-based level-order search, stack/backtracking search, greedy shortest path relaxation, and topological sorting on Directed Acyclic Graphs (DAGs).
- **Concepts Covered**: Adjacency matrices, adjacency lists, Breadth-First Search (BFS), recursive and iterative Depth-First Search (DFS), Dijkstra's single-source shortest path, social network connection degree analysis, 2D grid maze pathfinding, and Kahn's / DFS topological prerequisite scheduling.

| Program | File Path | Description | Key Algorithms & Principles |
| :--- | :--- | :--- | :--- |
| **Program 1** | `Lab07-Graphs/Program01-AdjacencyMatrix/adjacency_matrix.py` | Dense 2D grid graph model | 2D array representation supporting edge addition/removal, vertex degree computation, and density calculation. |
| **Program 2** | `Lab07-Graphs/Program02-AdjacencyList/adjacency_list.py` | Sparse dictionary-linked graph model | Space-efficient representation storing neighbors in dynamic lists; neighbor inspection in $\mathcal{O}(\text{deg}(v))$ time. |
| **Program 3** | `Lab07-Graphs/Program03-BFS/bfs.py` | Breadth-First Search engine | Queue-driven level-order traversal, visited state tracking, and shortest-path hop calculation on unweighted graphs. |
| **Program 4** | `Lab07-Graphs/Program04-RecursiveDFS/recursive_dfs.py` | Recursive Depth-First Search | Recursive call-stack exploration, connected components discovery, and cycle detection in undirected graphs. |
| **Program 5** | `Lab07-Graphs/Program05-IterativeDFS/iterative_dfs.py` | Explicit-stack Depth-First Search | Non-recursive DFS preventing recursion limit overflows, graph path discovery. |
| **Program 6** | `Lab07-Graphs/Program06-Dijkstra/dijkstra.py` | Shortest path on weighted graphs | Greedy relaxation ($d[v] = \min(d[v], d[u] + w)$) powered by a custom Min-Heap Priority Queue in $\mathcal{O}((V + E) \log V)$ time. |
| **Program 7** | `Lab07-Graphs/Program07-SocialNetwork/social_network.py` | Social network analytics engine | Degree of separation analysis, mutual friend discovery, and network centrality scoring. |
| **Program 8** | `Lab07-Graphs/Program08-MazeSolver/maze_solver.py` | 2D grid pathfinder | BFS and DFS pathfinding through obstacled mazes, reconstructing optimal exit coordinates. |
| **Program 9** | `Lab07-Graphs/Program09-CoursePrerequisites/course_prerequisites.py` | Academic course DAG scheduler | Directed Acyclic Graph dependency validation, cycle detection, and Topological Sorting (Kahn's in-degree algorithm). |

---

## Capstone Project: Pathfinding Visualizer
### A Graph-Based Pathfinding and Shortest Path Analysis System

- **Location**: [`Capstone-Projects/Pathfinding-Visualizer/`](Capstone-Projects/Pathfinding-Visualizer/)
- **Documentation**: [Project README](Capstone-Projects/Pathfinding-Visualizer/README.md) | [Engineering Reflection](Capstone-Projects/Pathfinding-Visualizer/reflection.md)
- **Theoretical Basis**: Complete synthesis of Units 1–7. Discrete 2D planar grid modeled as an implicit graph $G=(V, E)$ with 4-connectivity (Up, Down, Left, Right). Demonstrates how foundational data structures govern exploration frontiers, space-time complexities, and optimality guarantees across unweighted and weighted topologies.
- **Manual Core Data Structures**:
  - **FIFO Queue (`Queue`)**: Singly-linked list with head/tail pointers delivering strict $\mathcal{O}(1)$ operations for BFS level-order frontier expansion.
  - **LIFO Stack (`Stack`)**: Singly-linked list with top pointer delivering strict $\mathcal{O}(1)$ operations for DFS backtracking and deep branch exploration.
  - **Binary Min-Heap (`MinHeap`)**: 0-indexed dynamic array priority queue with $\mathcal{O}(\log V)$ sift-up/down operations and a monotonic tie-breaker counter for Dijkstra's distance extraction.
- **Algorithms Implemented**:
  - **Breadth-First Search (BFS)**: Finds the guaranteed shortest path on unweighted grids ($\mathcal{O}(V + E)$ time, $\mathcal{O}(V)$ space).
  - **Depth-First Search (DFS)**: Deeply dives along branches; finds a valid path if reachable ($\mathcal{O}(V + E)$ time, $\mathcal{O}(V)$ space).
  - **Dijkstra's Algorithm**: Provably optimal shortest path for non-negative cell/edge weights ($\mathcal{O}((V + E) \log V)$ time, $\mathcal{O}(V)$ space).
- **Dual-Mode System Interface**:
  - **Graphical Desktop Application (`gui.py`)**: Modern dark-themed Tkinter GUI (Tokyo Dark / Catppuccin palette). Features non-blocking step-by-step animation via `widget.after()`, click-and-drag wall creation, right-click wall erasing, drag-and-drop Start (**S**) and Destination (**E**) relocation, procedural braided maze generation, speed slider ($1$–$100\text{ ms}$), pause/resume playback, and live statistics reporting pure computational runtime via `time.perf_counter()`.
  - **Interactive Terminal CLI (`pathfinding_visualizer.py --cli`)**: ANSI-colored console interface with menu-driven grid editing, live terminal step rendering, preset scenarios, and a multi-algorithm benchmark comparison suite.
- **Verification**: 38 automated unit tests covering core data structures, algorithms, edge cases, controller state transitions, and GUI lifecycle (`tests/test_pathfinding.py`, `tests/test_gui.py`).

---

## Documentation & Visual Assets

All high-level architectural documentation, mathematical analyses, PlantUML source specifications, and publication-ready graphics reside in the [`docs/`](docs/) directory:

- **[`docs/diagrams/`](docs/diagrams/)**: Contains 11 PlantUML source files (`.puml`) along with high-resolution rendered PNG diagrams illustrating the memory layout and pointer references of every implemented data structure:
  - `01_arrays_and_2d_arrays.png` & `01_arrays_and_2d_arrays.puml`
  - `02_sparse_matrix.png` & `02_sparse_matrix.puml`
  - `03_singly_linked_list.png` & `03_singly_linked_list.puml`
  - `04_doubly_linked_list.png` & `04_doubly_linked_list.puml`
  - `05_circular_linked_list.png` & `05_circular_linked_list.puml`
  - `06_stack.png` & `06_stack.puml`
  - `07_queue_and_circular_queue.png` & `07_queue_and_circular_queue.puml`
  - `08_priority_queue_and_heap.png` & `08_priority_queue_and_heap.puml`
  - `09_binary_search_tree.png` & `09_binary_search_tree.puml`
  - `10_avl_tree.png` & `10_avl_tree.puml`
  - `11_graph_representations.png` & `11_graph_representations.puml`

- **[`docs/algorithm-flowcharts/`](docs/algorithm-flowcharts/)**: Contains 8 PlantUML source files and publication-grade flowcharts detailing algorithmic execution logic:
  - `01_array_operations.png` & `01_array_operations.puml`: Array insertion, deletion, and rotation.
  - `02_sorting_and_searching.png` & `02_sorting_and_searching.puml`: Comparison sorting pipelines and binary search.
  - `03_linked_list_operations.png` & `03_linked_list_operations.puml`: Pointer reversal and node splicing.
  - `04_infix_to_postfix_and_eval.png` & `04_infix_to_postfix_and_eval.puml`: Shunting-Yard conversion and postfix execution.
  - `05_circular_queue_and_round_robin.png` & `05_circular_queue_and_round_robin.puml`: Modulo queue arithmetic and CPU timeslicing.
  - `06_bst_operations.png` & `06_bst_operations.puml`: Binary search tree insertion and 3-case node deletion.
  - `07_avl_insertion_and_rotations.png` & `07_avl_insertion_and_rotations.puml`: AVL recursive insertion and LL/RR/LR/RL rebalancing.
  - `08_bfs_dfs_and_dijkstra.png` & `08_bfs_dfs_and_dijkstra.puml`: Graph queue exploration, stack recursion, and greedy edge relaxation.

- **[`docs/complexity-analysis.pdf`](docs/complexity-analysis.pdf)**: Comprehensive mathematical treatise covering asymptotic time bounds, space complexities, memory topologies, and structural comparison tables across all 7 units.
- **[`docs/final-report.pdf`](docs/final-report.pdf)**: Consolidated academic laboratory manual integrating all program specifications, code listings, execution outputs, and theoretical reflections.
- **[`docs/presentation.pdf`](docs/presentation.pdf)**: 12-slide landscape presentation summarizing system architectures, laboratory achievements, and performance metrics.

---

## Algorithmic Complexity & Performance Analysis

Algorithmic efficiency across the repository is formally analyzed based on asymptotic execution time (Best, Average, Worst) and auxiliary memory footprint.

### Asymptotic Comparison Summary

| Algorithm / Data Structure | Best Time | Average Time | Worst Time | Aux Space | Invariant / Structural Constraint |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Bubble Sort (Optimized)** | $\mathcal{O}(n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Stable. Early-exit flag halts after 1 pass on pre-sorted data. |
| **Selection Sort** | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Unstable. Fixed comparisons; maximum $n-1$ memory writes. |
| **Insertion Sort** | $\mathcal{O}(n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Stable. Adaptive shifting; optimal for nearly-sorted arrays. |
| **Merge Sort** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | Stable. Divide-and-conquer; deterministic upper bound. |
| **Quick Sort (Median-of-3)**| $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(\log n)$ | Unstable. In-place partitioning; median pivot mitigates worst case. |
| **Heap Sort** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(1)$ | Unstable. In-place binary heap; guaranteed log-linear runtime. |
| **Radix Sort (LSD)** | $\mathcal{O}(d(n+b))$ | $\mathcal{O}(d(n+b))$ | $\mathcal{O}(d(n+b))$ | $\mathcal{O}(n+b)$ | Stable. Non-comparison sorting via base-$b$ positional digits. |
| **Binary Search** | $\mathcal{O}(1)$ | $\mathcal{O}(\log n)$ | $\mathcal{O}(\log n)$ | $\mathcal{O}(1)$ | Requires sorted contiguous array; bisects search range. |
| **Separate Chaining Hash** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(n)$ | $\mathcal{O}(m+n)$ | Polynomial rolling hash; dynamic linked collision lists. |
| **Linear Probing Hash** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(n)$ | $\mathcal{O}(m)$ | Open addressing; susceptible to primary clustering at high load. |
| **Singly / Doubly Linked List**| $\mathcal{O}(1)$ | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ head insertion/deletion; $\mathcal{O}(n)$ arbitrary index access. |
| **Stack (Array / Linked)** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Strict LIFO boundary enforcement. |
| **Queue (Circular / Linked)**| $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Strict FIFO boundary enforcement; modulo index wrapping. |
| **Binary Min-Heap Queue** | $\mathcal{O}(1)$ | $\mathcal{O}(\log n)$ | $\mathcal{O}(\log n)$ | $\mathcal{O}(1)$ | Complete binary tree satisfying heap ordering property. |
| **Binary Search Tree (BST)**| $\mathcal{O}(1)$ | $\mathcal{O}(\log n)$ | $\mathcal{O}(n)$ | $\mathcal{O}(h)$ | Degenerates to linear chain $\mathcal{O}(n)$ on pre-sorted input. |
| **AVL Tree (Self-Balancing)**| $\mathcal{O}(1)$ | $\mathcal{O}(\log n)$ | $\mathcal{O}(\log n)$ | $\mathcal{O}(\log n)$ | Strict balance constraint $\|\text{BF}\| \le 1$; height bounded by $1.44 \log_2 n$. |
| **Graph BFS / DFS** | $\mathcal{O}(V + E)$ | $\mathcal{O}(V + E)$ | $\mathcal{O}(V + E)$ | $\mathcal{O}(V)$ | Linear exploration; BFS yields unweighted shortest paths. |
| **Dijkstra's Algorithm** | $\mathcal{O}((V+E)\log V)$| $\mathcal{O}((V+E)\log V)$| $\mathcal{O}((V+E)\log V)$| $\mathcal{O}(V)$ | Greedy relaxation on non-negative weighted graphs with min-heap. |

For detailed mathematical derivations and break-even formulations, refer to [`docs/complexity-analysis.pdf`](docs/complexity-analysis.pdf).

---

## Execution Guide & Verification

### System Requirements
- **Python**: Version 3.8 or later installed.
- **Operating Systems**: Linux (Ubuntu, Debian, Fedora, Arch), macOS, or Windows (Command Prompt / PowerShell / WSL).
- **External Dependencies**: None required for running programs. (Python standard library only).

### Verification of Python Environment

Verify that Python 3.8+ is installed on your system:

```bash
python3 --version
```
*(On Windows systems, use `python --version`)*

### Running Programs

All 53 programs in the repository are completely independent and directly executable. Each program provides an interactive command-line interface when executed without arguments.

#### 1. Interactive Execution Mode
To execute any program interactively, run:

```bash
# Example 1: Run 1D Array Operations (Lab 1)
python3 Lab01-Introduction-Arrays/Program01-ArrayOperations/array_operations.py

# Example 2: Run Matrix Calculator (Lab 1)
python3 Lab01-Introduction-Arrays/Program04-MatrixCalculator/matrix_calculator.py

# Example 3: Run Quick Sort (Lab 2)
python3 Lab02-Sorting-Searching/Program05-QuickSort/quick_sort.py

# Example 4: Run Shunting-Yard Expression Evaluator (Lab 4)
python3 Lab04-Stacks/Program07-ExpressionEvaluator/expression_evaluator.py

# Example 5: Run AVL Tree Visualizer (Lab 6)
python3 Lab06-Trees/Program04-AVLTree/avl_tree.py

# Example 6: Run Dijkstra's Shortest Path Algorithm (Lab 7)
python3 Lab07-Graphs/Program06-Dijkstra/dijkstra.py

# Example 7: Launch Capstone Desktop GUI Visualizer
python3 Capstone-Projects/Pathfinding-Visualizer/gui.py

# Example 8: Run Capstone Terminal CLI
python3 Capstone-Projects/Pathfinding-Visualizer/pathfinding_visualizer.py --cli
```

#### 2. Automated Self-Testing Mode (`--test` & `unittest`)
Every program in the repository is equipped with a comprehensive self-testing assertion harness. To verify correct algorithmic invariants, boundary cases, and error handling without interactive inputs, pass the `--test` flag:

```bash
# Run automated tests on Singly Linked List
python3 Lab03-Linked-Lists/Program01-SinglyLinkedList/singly_linked_list.py --test

# Run automated tests on Binary Min-Heap Priority Queue
python3 Lab05-Queues/Program06-HeapPriorityQueue/heap_priority_queue.py --test

# Run automated tests on AVL Balanced Tree
python3 Lab06-Trees/Program04-AVLTree/avl_tree.py --test

# Run automated tests on Dijkstra Shortest Path
python3 Lab07-Graphs/Program06-Dijkstra/dijkstra.py --test

# Run automated tests on Maze Solver
python3 Lab07-Graphs/Program08-MazeSolver/maze_solver.py --test

# Run automated test suite on Capstone Project (38 tests)
python3 -m unittest discover -s Capstone-Projects/Pathfinding-Visualizer/tests -p "test_*.py" -v
```

#### 3. Empirical Benchmarking (Lab 2)
To run the automated empirical sorting benchmark and generate the performance curves:

```bash
python3 Lab02-Sorting-Searching/Program09-PerformanceAnalysis/sorting_comparison.py
```
*(Generated plots are saved directly to `Lab02-Sorting-Searching/outputs/`)*

---

## Curricular Learning Outcomes

Upon completing this seven-unit curriculum, the following technical competencies were established:

1. **Memory Contiguity & Offset Math (CO1)**: Understanding row-major array indexing, element shifting penalties, and memory-saving techniques like 3-tuple sparse matrix compression.
2. **Asymptotic Sorting & Searching Discipline (CO2)**: Distinguishing between quadratic comparisons ($\mathcal{O}(n^2)$), optimal divide-and-conquer comparisons ($\mathcal{O}(n \log n)$), and non-comparison distribution sorts ($\mathcal{O}(d(n+b))$).
3. **Dynamic Pointer Topology Management (CO1)**: Manipulating pointer links across singly, doubly, and circular lists without memory leaks, handling head/tail pointer updates and in-place sequence reversals.
4. **LIFO & Infix Parsing Architecture (CO1)**: Managing call-stack activation records, operator precedence, syntax parsing, bracket validation, and undo/redo dual-stack command patterns.
5. **FIFO & Scheduling Mechanics (CO1)**: Resolving false overflow via circular queue modulo arithmetic, priority-ordered heap queues, and simulating realistic Round-Robin CPU timeslicing and bank queuing.
6. **Hierarchical Structures & Self-Balancing Invariants (CO3)**: Balancing binary search trees via single and double AVL rotations to guarantee strict logarithmic execution ($\mathcal{O}(\log n)$).
7. **Graph Theory & Pathfinding (CO3)**: Formulating problem spaces as relational graphs, analyzing topological prerequisites via DAGs, and executing greedy shortest path relaxations via Dijkstra's algorithm.

---

## Academic Navigation Directory

The following directory provides direct links to the README documentation and reflective analyses for all units, alongside consolidated project reports:

| Unit / Topic | Documentation README | Student Reflection | Key Implementation Files |
| :--- | :--- | :--- | :--- |
| **Unit 1: Arrays & Matrices** | [Lab01 README](Lab01-Introduction-Arrays/README.md) | [Lab01 Reflection](Lab01-Introduction-Arrays/reflection.md) | [1D Arrays](Lab01-Introduction-Arrays/Program01-ArrayOperations/array_operations.py), [2D Arrays](Lab01-Introduction-Arrays/Program02-2DArrayOperations/2d_array_operations.py), [Sparse Matrix](Lab01-Introduction-Arrays/Program03-SparseMatrix/sparse_matrix.py), [Matrix Calc](Lab01-Introduction-Arrays/Program04-MatrixCalculator/matrix_calculator.py) |
| **Unit 2: Sorting & Searching** | [Lab02 README](Lab02-Sorting-Searching/README.md) | [Lab02 Reflection](Lab02-Sorting-Searching/reflection.md) | [Bubble](Lab02-Sorting-Searching/Program01-BubbleSort/bubble_sort.py), [Selection](Lab02-Sorting-Searching/Program02-SelectionSort/selection_sort.py), [Insertion](Lab02-Sorting-Searching/Program03-InsertionSort/insertion_sort.py), [Merge](Lab02-Sorting-Searching/Program04-MergeSort/merge_sort.py), [Quick](Lab02-Sorting-Searching/Program05-QuickSort/quick_sort.py), [Heap](Lab02-Sorting-Searching/Program06-HeapSort/heap_sort.py), [Radix](Lab02-Sorting-Searching/Program07-RadixSort/radix_sort.py), [Binary Search](Lab02-Sorting-Searching/Program08-BinarySearch/binary_search.py), [Benchmark](Lab02-Sorting-Searching/Program09-PerformanceAnalysis/sorting_comparison.py), [Student Records](Lab02-Sorting-Searching/Program10-StudentRecordManager/student_record_manager.py), [Search Engine](Lab02-Sorting-Searching/Program11-SearchEngineSimulator/search_engine.py) |
| **Unit 3: Linked Lists** | [Lab03 README](Lab03-Linked-Lists/README.md) | [Lab03 Reflection](Lab03-Linked-Lists/reflection.md) | [Singly List](Lab03-Linked-Lists/Program01-SinglyLinkedList/singly_linked_list.py), [Doubly List](Lab03-Linked-Lists/Program02-DoublyLinkedList/doubly_linked_list.py), [Circular List](Lab03-Linked-Lists/Program03-CircularLinkedList/circular_linked_list.py), [Polynomial](Lab03-Linked-Lists/Program04-PolynomialOperations/polynomial_operations.py), [Text Buffer](Lab03-Linked-Lists/Program05-TextEditorBuffer/text_editor_buffer.py), [Playlist](Lab03-Linked-Lists/Program06-PlaylistManager/playlist_manager.py) |
| **Unit 4: Stacks** | [Lab04 README](Lab04-Stacks/README.md) | [Lab04 Reflection](Lab04-Stacks/reflection.md) | [Static Stack](Lab04-Stacks/Program01-StaticStack/static_stack.py), [Dynamic Stack](Lab04-Stacks/Program02-DynamicStack/dynamic_stack.py), [Infix-Postfix](Lab04-Stacks/Program03-InfixToPostfix/infix_to_postfix.py), [Infix-Prefix](Lab04-Stacks/Program04-InfixToPrefix/infix_to_prefix.py), [Postfix Eval](Lab04-Stacks/Program05-PostfixEvaluation/postfix_evaluation.py), [Prefix Eval](Lab04-Stacks/Program06-PrefixEvaluation/prefix_evaluation.py), [Expression Eval](Lab04-Stacks/Program07-ExpressionEvaluator/expression_evaluator.py), [Undo-Redo](Lab04-Stacks/Program08-UndoRedo/undo_redo.py) |
| **Unit 5: Queues** | [Lab05 README](Lab05-Queues/README.md) | [Lab05 Reflection](Lab05-Queues/reflection.md) | [Static Queue](Lab05-Queues/Program01-StaticQueue/static_queue.py), [Dynamic Queue](Lab05-Queues/Program02-DynamicQueue/dynamic_queue.py), [Circular Queue](Lab05-Queues/Program03-CircularQueue/circular_queue.py), [Deque](Lab05-Queues/Program04-Deque/deque.py), [Array PQ](Lab05-Queues/Program05-ArrayPriorityQueue/array_priority_queue.py), [Heap PQ](Lab05-Queues/Program06-HeapPriorityQueue/heap_priority_queue.py), [Customer Service](Lab05-Queues/Program07-CustomerServiceSimulation/customer_service.py), [CPU Scheduling](Lab05-Queues/Program08-ProcessScheduling/process_scheduling.py) |
| **Unit 6: Trees** | [Lab06 README](Lab06-Trees/README.md) | [Lab06 Reflection](Lab06-Trees/reflection.md) | [Recursive Traversal](Lab06-Trees/Program01-RecursiveTraversals/recursive_traversals.py), [Iterative Traversal](Lab06-Trees/Program02-IterativeTraversals/iterative_traversals.py), [BST](Lab06-Trees/Program03-BinarySearchTree/binary_search_tree.py), [AVL Tree](Lab06-Trees/Program04-AVLTree/avl_tree.py), [Expression Tree](Lab06-Trees/Program05-ExpressionTree/expression_tree.py), [File System](Lab06-Trees/Program06-FileSystemSimulator/file_system.py), [Symbol Table](Lab06-Trees/Program07-SymbolTable/symbol_table.py) |
| **Unit 7: Graphs** | [Lab07 README](Lab07-Graphs/README.md) | [Lab07 Reflection](Lab07-Graphs/reflection.md) | [Adjacency Matrix](Lab07-Graphs/Program01-AdjacencyMatrix/adjacency_matrix.py), [Adjacency List](Lab07-Graphs/Program02-AdjacencyList/adjacency_list.py), [BFS](Lab07-Graphs/Program03-BFS/bfs.py), [Recursive DFS](Lab07-Graphs/Program04-RecursiveDFS/recursive_dfs.py), [Iterative DFS](Lab07-Graphs/Program05-IterativeDFS/iterative_dfs.py), [Dijkstra](Lab07-Graphs/Program06-Dijkstra/dijkstra.py), [Social Network](Lab07-Graphs/Program07-SocialNetwork/social_network.py), [Maze Solver](Lab07-Graphs/Program08-MazeSolver/maze_solver.py), [Prerequisites](Lab07-Graphs/Program09-CoursePrerequisites/course_prerequisites.py) |
| **Capstone Project: Pathfinding Visualizer** | [Capstone README](Capstone-Projects/Pathfinding-Visualizer/README.md) | [Capstone Reflection](Capstone-Projects/Pathfinding-Visualizer/reflection.md) | [Desktop GUI](Capstone-Projects/Pathfinding-Visualizer/gui.py), [Core & CLI](Capstone-Projects/Pathfinding-Visualizer/pathfinding_visualizer.py), [Unit Tests](Capstone-Projects/Pathfinding-Visualizer/tests/test_pathfinding.py) |

### Consolidated Academic Publications
- **Consolidated Laboratory Manual**: [`docs/final-report.pdf`](docs/final-report.pdf)
- **Mathematical Complexity Analysis**: [`docs/complexity-analysis.pdf`](docs/complexity-analysis.pdf)
- **System Architecture Slide Deck**: [`docs/presentation.pdf`](docs/presentation.pdf)
- **Data Structure UML Diagrams**: [`docs/diagrams/`](docs/diagrams/)
- **Algorithm Flowcharts**: [`docs/algorithm-flowcharts/`](docs/algorithm-flowcharts/)

---

## Conclusion

This laboratory repository provides an extensive, academically rigorous exploration of data structures and algorithms implemented purely from first principles. Across 53 standalone programs, 11 architectural diagrams, and 8 algorithmic flowcharts, the codebase demonstrates how fundamental invariants govern computational efficiency and software architecture.

By deliberately avoiding black-box library shortcuts, the implementations illuminate the trade-offs between memory contiguity and dynamic flexibility, quadratic vs. log-linear complexity, and recursive vs. iterative mechanics—equipping students with practical system design skills and deep theoretical comprehension.
