# IC-307D: Data Structures and Algorithms Lab
## Unit 6: Trees (CO3)

---

## 1. Introduction to Tree Data Structures

A **Tree** is a non-linear, hierarchical abstract data type (ADT) composed of entities called **nodes** linked together by directed edges without forming any cycles. Unlike linear data structures (arrays, linked lists, stacks, and queues) where elements exhibit a strict sequential predecessor-successor relationship, trees organize data hierarchically into parent-child relationships.

```
                     [Root: Level 0]
                         /      \
             [Node: Level 1]    [Node: Level 1]
                 /     \            /      \
            [Leaf]    [Leaf]     [Leaf]    [Leaf]  (Level 2)
```

### Essential Tree Terminology
1. **Root**: The unique topmost node in the hierarchy that has no parent ($0$ incoming edges).
2. **Edge**: The directed link connecting a parent node to its child.
3. **Parent & Child**: If an edge connects node $U$ to node $V$, $U$ is the parent of $V$, and $V$ is the child of $U$.
4. **Siblings**: Nodes that share the exact same parent node.
5. **Leaf Node (External Node)**: A node with zero children.
6. **Internal Node**: A non-leaf node possessing one or more children.
7. **Subtree**: Any tree node along with all of its descendants forms an independent subtree.
8. **Depth of a Node**: The number of edges along the path from the root node to that specific node. Depth of root is $0$.
9. **Height of a Node**: The length of the longest simple downward path from that node to a leaf. Height of a leaf is $1$ (or $0$ under 0-based convention).
10. **Height of a Tree**: The height of its root node.
11. **Degree of a Node**: The total number of children associated with that node.
12. **Binary Tree**: A constrained hierarchical tree where every node has **at most two children**, formally designated as the **left child** and the **right child**.

Trees form the core organizational substrate of file systems (hierarchical directory namespaces), compiler abstract syntax trees (ASTs), parsing engines, database indexing structures ($B$-Trees and $B+$-Trees), priority heaps, and network routing hierarchies.

---

## 2. Aim

To design, implement from first principles, test, analyze, and document fundamental and self-balancing tree data structures in Python 3; to master recursive and iterative tree traversals; to construct Binary Search Trees (BST) and self-balancing AVL Trees with all four rotation cases; to build and evaluate arithmetic Expression Trees; and to engineer practical tree-based applications including an in-memory File System Simulator and a Compiler Symbol Table.

---

## 3. Learning Objectives

- Master the hierarchical architecture and invariant relationships of binary trees and $N$-ary trees.
- Compare and contrast **recursive** (call-stack based) versus **iterative** (explicit LIFO stack based) tree traversals across Preorder, Inorder, and Postorder schemes.
- Implement the **Binary Search Tree (BST)** ordering invariant ($k_{\text{left}} < k_{\text{root}} < k_{\text{right}}$) and master the three structural deletion cases: leaf, single child, and two children (inorder successor replacement).
- Understand why unbalanced BSTs degenerate to $O(n)$ linear chains on sorted inputs, and solve this limitation using **AVL Trees**.
- Master height tracking, balance factor calculations ($\text{BF} = h_L - h_R$), and all four rotation primitives: **Left-Left (LL)**, **Right-Right (RR)**, **Left-Right (LR)**, and **Right-Left (RL)**.
- Build arithmetic **Expression Trees** from postfix tokens using an explicit node stack, evaluate them recursively without `eval()`, and reconstruct prefix, infix, and postfix notations.
- Model operating system namespaces as general $N$-ary trees in a **File System Simulator**.
- Construct a compiler **Symbol Table** using a BST to store identifiers, type signatures, scopes, and source lines, detecting duplicate declarations and undeclared identifiers.

---

## 4. Software Requirements

- **Operating System**: Linux (Ubuntu 22.04 LTS / Debian 12 / POSIX-compliant) or Windows 10/11 / macOS.
- **Language**: Python 3.8+ (Tested on Python 3.10 / 3.11).
- **External Dependencies**: None. Standard library built-ins only (no external tree libraries, no `heapq`, and no Python dictionaries replacing tree structures).
- **Terminal Shell**: Bash / Zsh / PowerShell.

---

## 5. Experiment 1: Recursive Binary Tree Traversals

### Problem Statement
Implement a binary tree with a `TreeNode` class containing `data`, `left`, and `right` references. Implement recursive Preorder, Inorder, and Postorder traversals, construct a representative reference tree, and display the visitation orders.

### Approach
A binary tree node is encapsulated in `TreeNode(data)`. Traversals are implemented using classical structural recursion:
- **Preorder (Root $\to$ Left $\to$ Right)**: Processes the current node first, then recursively descends into the left subtree, followed by the right subtree. Used for deep copying and prefix serialization.
- **Inorder (Left $\to$ Root $\to$ Right)**: Traverses the left subtree, processes the root, and traverses the right subtree. In a BST, this yields keys in strictly ascending order.
- **Postorder (Left $\to$ Right $\to$ Root)**: Recursively processes both subtrees before processing the root node. Used for bottom-up node deallocation and postfix expression evaluation.

### Sample Reference Tree
```text
             1
           /   \
          2     3
         / \   / \
        4   5 6   7
```

### Dry Run
1. **Preorder**: Visit 1 $\to$ Left subtree at 2: Visit 2 $\to$ Visit 4 $\to$ Visit 5 $\to$ Right subtree at 3: Visit 3 $\to$ Visit 6 $\to$ Visit 7.
   $$\text{Result: } [1, 2, 4, 5, 3, 6, 7]$$
2. **Inorder**: Leftmost leaf 4 $\to$ Root 2 $\to$ 5 $\to$ Overall Root 1 $\to$ 6 $\to$ 3 $\to$ 7.
   $$\text{Result: } [4, 2, 5, 1, 6, 3, 7]$$
3. **Postorder**: Left leaves (4, 5) $\to$ Root 2 $\to$ Right leaves (6, 7) $\to$ Root 3 $\to$ Overall Root 1.
   $$\text{Result: } [4, 5, 2, 6, 7, 3, 1]$$

### Complexity
- **Time Complexity**: $O(n)$ for all three traversals, as each node is visited exactly once.
- **Auxiliary Space Complexity**: $O(h)$ where $h$ is tree height, representing call stack frames ($O(\log n)$ for balanced trees, $O(n)$ for skewed trees).

### Real-Life Applications
- Serialization and deserialization of tree data over network streams (Preorder).
- Generating sorted reports from hierarchical databases (Inorder).
- Clean bottom-up directory size summation and memory deallocation (Postorder).

---

## 6. Experiment 2: Iterative Binary Tree Traversals

### Problem Statement
Implement Preorder, Inorder, and Postorder traversals for a binary tree using an explicit LIFO stack without using recursion. Verify that results match recursive traversal outputs.

### Approach
In recursive traversals, the operating system manages a hidden runtime call stack. In iterative traversals, we simulate this mechanism explicitly using a Python list as a stack:
1. **Iterative Preorder**: Push `root` to stack. Loop: pop node, record data, push `node.right` (if exists), then push `node.left` (so left is popped and visited first).
2. **Iterative Inorder**: Track `curr = root`. While `curr is not None` or stack non-empty: descend along the left spine pushing ancestors onto stack. When reaching `None`, pop node, record data, and advance `curr = node.right`.
3. **Iterative Postorder (Two-Stack Algorithm)**: Push `root` to `stack1`. Loop: pop node from `stack1`, push to `stack2`, then push `node.left` followed by `node.right` to `stack1`. When `stack1` is exhausted, popping all elements from `stack2` inverts the sequence to exact $\text{Left} \to \text{Right} \to \text{Root}$ postorder.

### Complexity
- **Time Complexity**: $O(n)$ for Preorder, Inorder, and Postorder.
- **Auxiliary Space Complexity**: $O(h)$ for Preorder and Inorder stack depth; $O(n)$ for Postorder (two stacks).

### Real-Life Applications
- Production compiler and graphics rendering pipelines that must avoid stack overflow on deeply unbalanced trees (bypassing Python's default recursion limit of 1000 frames).

---

## 7. Experiment 3: Binary Search Tree (BST)

### Problem Statement
Implement a Binary Search Tree supporting `insert`, `search`, `delete`, `find_min`, `find_max`, `inorder_traversal`, and recursive BST validation. Define and enforce a duplicate policy, and handle all three deletion cases.

### Approach
- **BST Invariant**: For every node $N$, all keys in $N.\text{left} < N.\text{key} < \text{all keys in } N.\text{right}$.
- **Duplicate Policy**: Duplicate keys are strictly rejected with a `ValueError` to preserve set semantics and unique key constraints.
- **Deletion Cases**:
  - *Case 1 (Leaf node)*: No children. Simply unlink the node by returning `None` to its parent.
  - *Case 2 (Single child)*: Node has only left or only right child. Bypass the node by returning its non-null child to the parent.
  - *Case 3 (Two children)*: Locate the **inorder successor** (the minimum node in the right subtree: $\min(\text{node.right})$). Copy the successor's key to the current node, then recursively delete the successor key from the right subtree.
- **BST Validation**: Recursively verify that every node satisfies:
  $$\text{min\_val} < \text{node.key} < \text{max\_val}$$
  For left child, bounds become $(\text{min\_val}, \text{node.key})$; for right child, bounds become $(\text{node.key}, \text{max\_val})$.

### Complexity
- **Time Complexity**:
  - `search` / `insert` / `delete`:
    - Best Case: $O(1)$ (root match).
    - Average Case: $O(\log n)$ (balanced tree).
    - Worst Case: $O(n)$ (degenerate skewed tree).
  - `find_min` / `find_max`: $O(h)$ where $h$ is height.
  - `inorder_traversal`: $O(n)$.
- **Auxiliary Space Complexity**: $O(h)$ recursion stack frames.

### Real-Life Applications
- In-memory key-value indexes and symbol lookup tables in software tools.
- Auto-complete and range query engines.

---

## 8. Experiment 4: Self-Balancing AVL Tree

### Problem Statement
Implement an Adelson-Velsky and Landis (AVL) self-balancing Binary Search Tree. Maintain node heights, compute balance factors, implement all four rotation cases (LL, RR, LR, RL), and support self-balancing `insert` and `delete` with validation.

### Approach
- **Height Definition**: 1-based height where $\text{height}(\text{leaf}) = 1$ and $\text{height}(\text{None}) = 0$:
  $$\text{height}(\text{node}) = 1 + \max(\text{height}(\text{node.left}), \text{height}(\text{node.right}))$$
- **Balance Factor ($\text{BF}$)**:
  $$\text{BF}(\text{node}) = \text{height}(\text{node.left}) - \text{height}(\text{node.right})$$
  **AVL Invariant**: For every node, $\text{BF} \in \{-1, 0, +1\}$. If $|\text{BF}| > 1$, rebalance immediately.
- **The Four Rotation Cases**:
  1. **Left-Left (LL)**: Unbalanced node has $\text{BF} > 1$ and key inserted into left child's left subtree ($\text{BF}(\text{left}) \ge 0$). Solution: **Single Right Rotation**.
  2. **Right-Right (RR)**: Unbalanced node has $\text{BF} < -1$ and key inserted into right child's right subtree ($\text{BF}(\text{right}) \le 0$). Solution: **Single Left Rotation**.
  3. **Left-Right (LR)**: Unbalanced node has $\text{BF} > 1$ and key inserted into left child's right subtree ($\text{BF}(\text{left}) < 0$). Solution: **Left Rotate left child, then Right Rotate node**.
  4. **Right-Left (RL)**: Unbalanced node has $\text{BF} < -1$ and key inserted into right child's left subtree ($\text{BF}(\text{right}) > 0$). Solution: **Right Rotate right child, then Left Rotate node**.

### Why AVL Trees Guarantee Logarithmic Height
Let $N(h)$ be the minimum number of nodes in an AVL tree of height $h$. Then:
$$N(h) = 1 + N(h - 1) + N(h - 2)$$
This recurrence behaves like the Fibonacci sequence. Solving it yields:
$$h < 1.44 \log_2(n + 2) - 0.328 \implies h = O(\log n)$$
Thus, the height of an AVL tree with $n$ nodes is strictly bounded by $1.44 \log_2 n$, guaranteeing that search, insertion, and deletion **never degrade to $O(n)$**.

### Complexity
- **Time Complexity**:
  - `search`: Worst case $O(\log n)$.
  - `insert`: $O(\log n)$ (traversal + at most 2 rotations).
  - `delete`: $O(\log n)$ (traversal + at most $O(\log n)$ rotations up to the root).
- **Auxiliary Space Complexity**: $O(\log n)$ recursion stack frames.

### Real-Life Applications
- Database indexing systems where lookups vastly outnumber writes.
- Real-time routing tables where worst-case $O(\log n)$ query bounds are mission-critical.

---

## 9. Experiment 5: Expression Tree

### Problem Statement
Construct an arithmetic Expression Tree from a postfix expression using an explicit node stack. Display Infix (with minimal/correct parentheses), Prefix, and Postfix notations. Recursively evaluate the tree without using Python's `eval()`, handling division by zero and invalid postfix expressions.

### Approach
- **Node Structure**: `ExprNode(value)` with `left` and `right` pointers. Leaf nodes represent numeric operands; internal nodes represent operators (`+`, `-`, `*`, `/`, `^`).
- **Postfix Construction Algorithm**:
  1. Tokenize whitespace-separated postfix string.
  2. For each token:
     - If numeric operand: create `ExprNode(token)` and push to stack.
     - If operator: pop `right_child`, pop `left_child` (raise error if $<2$ items on stack). Create `ExprNode(operator)`, attach children, and push operator node to stack.
  3. When tokens finish, verify that exactly $1$ node remains on stack (the tree root).
- **Evaluation**: Recursively evaluate left and right subtrees and apply arithmetic operation. If operator is `/` and right operand evaluates to $0.0$, raise `ZeroDivisionError`.

### Complexity
- **Time Complexity**:
  - Construction: $O(n)$ where $n$ is token count.
  - Evaluation: $O(n)$ visiting each node once.
- **Auxiliary Space Complexity**: $O(n)$ for tree nodes and evaluation call stack.

### Real-Life Applications
- Compiler optimization passes (Constant Folding, Subexpression Elimination).
- Database SQL query plan trees and spreadsheet formula evaluation engines.

---

## 10. Experiment 6: File System Simulator

### Problem Statement
Build an in-memory hierarchical File System Simulator using an $N$-ary general tree structure. Support directory creation (`mkdir`), file creation (`touch`), directory traversal (`cd`, `cd ..`), current path display (`pwd`), recursive file search, deletion with non-empty protection (`rm`), and hierarchical tree visualization (`tree`). Do not interact with the host OS filesystem.

### Approach
- **Node Architecture**: `FSNode(name, is_directory, size)` containing:
  - `parent`: Reference to parent `FSNode` (`None` for root `/`).
  - `children`: List of child `FSNode` objects for directory nodes.
- **Path Resolution**: Absolute path is reconstructed dynamically by following `parent` links up to root and reversing the collected names.
- **Safety Invariants**:
  - Duplicate file or directory names within the same directory are rejected.
  - The root directory (`/`) cannot be deleted.
  - Deleting a non-empty directory requires explicit recursive confirmation (`recursive=True`).
  - Memory operates entirely in RAM without OS file creation.

### Complexity
- **Time Complexity**:
  - Create file/directory: $O(k)$ where $k$ is number of children in current directory.
  - `cd` to child: $O(k)$; `cd ..`: $O(1)$.
  - `pwd` (path display): $O(d)$ where $d$ is directory depth.
  - `tree` display & search: $O(N)$ where $N$ is total nodes in the subtree.
- **Auxiliary Space Complexity**: $O(N)$ for $N$ nodes in memory.

### Real-Life Applications
- Virtual file systems (VFS in Linux kernels).
- In-memory ZIP/TAR archive inspection tools and cloud bucket folder simulators (Amazon S3 virtual prefixes).

---

## 11. Experiment 7: Symbol Table using BST

### Problem Statement
Implement a compiler Symbol Table using a custom Binary Search Tree without using Python dictionaries. Store identifier names, data types, values, scopes, and source lines. Support insertion, lookup, updating, deletion, and alphabetical display, detecting duplicate declarations and missing identifiers.

### Approach
- **Data Entities**:
  - `SymbolRecord(name, data_type, value, scope, line)`
  - `BSTSymbolNode(record)` where `record.name` acts as the BST search key.
- **Operations**:
  - `insert`: Inserts symbol alphabetically. If identifier already exists, raises `ValueError` ("Redundant declaration on Line X").
  - `lookup`: Performs $O(\log n)$ search. Returns `SymbolRecord` if found, `None` if undeclared.
  - `update`: Locates identifier and mutates value/type. Raises `KeyError` if undeclared.
  - `delete`: Deletes identifier from BST (e.g., when exiting a lexical scope block). Raises `KeyError` if undeclared.
  - `display`: Inorder traversal produces an alphabetical table of all symbols.

### Complexity
- **Time Complexity**:
  - `insert` / `lookup` / `update` / `delete`: Average $O(\log n)$, Worst $O(n)$.
  - `display` (inorder table print): $O(n)$.
- **Auxiliary Space Complexity**: $O(n)$ for tree nodes.

### Real-Life Applications
- Compiler lexical and semantic analysis phases (C, C++, Rust, Java compilers).
- Linkers and loaders managing symbol relocation tables.

---

## 12. Comparison of Binary Tree, BST and AVL Tree

| Feature / Property | General Binary Tree | Binary Search Tree (BST) | Self-Balancing AVL Tree |
|:---|:---:|:---:|:---:|
| **Ordering Property** | None (arbitrary placement) | $k_{\text{left}} < k_{\text{root}} < k_{\text{right}}$ | $k_{\text{left}} < k_{\text{root}} < k_{\text{right}}$ |
| **Balance Invariant** | None | None (can skew completely) | Strict: $\|\text{BF}\| \le 1$ at every node |
| **Height on $n$ Nodes (Best)** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ |
| **Height on $n$ Nodes (Worst)**| $O(n)$ (linear chain) | $O(n)$ (sorted input) | **$O(\log n)$ strictly guaranteed** |
| **Search Time (Average)** | $O(n)$ | $O(\log n)$ | $O(\log n)$ |
| **Search Time (Worst Case)** | $O(n)$ | $O(n)$ | **$O(\log n)$** |
| **Insertion Time (Worst Case)**| $O(n)$ | $O(n)$ | **$O(\log n)$** |
| **Deletion Time (Worst Case)** | $O(n)$ | $O(n)$ | **$O(\log n)$** |
| **Rebalancing Overhead** | None | None | Rotations during insert and delete |
| **Memory Overhead** | 2 pointers per node | 2 pointers per node | 2 pointers + height field per node |

---

## 13. Traversal Algorithms and Pseudocode

### 1. Recursive Traversals

```text
FUNCTION preorder_recursive(node):
    IF node IS NOT NULL THEN:
        VISIT(node.data)
        preorder_recursive(node.left)
        preorder_recursive(node.right)

FUNCTION inorder_recursive(node):
    IF node IS NOT NULL THEN:
        inorder_recursive(node.left)
        VISIT(node.data)
        inorder_recursive(node.right)

FUNCTION postorder_recursive(node):
    IF node IS NOT NULL THEN:
        postorder_recursive(node.left)
        postorder_recursive(node.right)
        VISIT(node.data)
```

### 2. Iterative Traversals (Using Explicit Stack)

```text
FUNCTION preorder_iterative(root):
    IF root IS NULL: RETURN []
    stack = [root]
    result = []
    WHILE stack IS NOT EMPTY:
        curr = stack.POP()
        result.APPEND(curr.data)
        IF curr.right IS NOT NULL: stack.PUSH(curr.right)
        IF curr.left IS NOT NULL:  stack.PUSH(curr.left)
    RETURN result

FUNCTION inorder_iterative(root):
    stack = []
    curr = root
    result = []
    WHILE curr IS NOT NULL OR stack IS NOT EMPTY:
        WHILE curr IS NOT NULL:
            stack.PUSH(curr)
            curr = curr.left
        curr = stack.POP()
        result.APPEND(curr.data)
        curr = curr.right
    RETURN result

FUNCTION postorder_iterative_two_stacks(root):
    IF root IS NULL: RETURN []
    stack1 = [root]
    stack2 = []
    result = []
    WHILE stack1 IS NOT EMPTY:
        curr = stack1.POP()
        stack2.PUSH(curr)
        IF curr.left IS NOT NULL:  stack1.PUSH(curr.left)
        IF curr.right IS NOT NULL: stack1.PUSH(curr.right)
    WHILE stack2 IS NOT EMPTY:
        result.APPEND(stack2.POP().data)
    RETURN result
```

---

## 14. AVL Rotations and Balancing

```
Case 1: Left-Left (LL) Heavy                 Case 2: Right-Right (RR) Heavy
           y                                            x
          / \                                          / \
         x   T3       -- Right Rotate(y) ->           T1  y
        / \                                              / \
       T1  T2                                           T2  T3

Case 3: Left-Right (LR) Heavy                Case 4: Right-Left (RL) Heavy
          z                     z                         z                     z
         / \                   / \                       / \                   / \
        x   T4  -- L-Rot(x) ->y   T4                    T1  x   -- R-Rot(x) ->T1  y
       / \                   / \                           / \                   / \
      T1  y                 x   T3                        y   T4                T2  x
         / \               / \                           / \                       / \
        T2  T3            T1  T2                        T2  T3                    T3  T4
        -- R-Rot(z) -> Balanced Tree                     -- L-Rot(z) -> Balanced Tree
```

### Rotation Pseudocode

```text
FUNCTION right_rotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = 1 + MAX(height(y.left), height(y.right))
    x.height = 1 + MAX(height(x.left), height(x.right))
    RETURN x

FUNCTION left_rotate(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    x.height = 1 + MAX(height(x.left), height(x.right))
    y.height = 1 + MAX(height(y.left), height(y.right))
    RETURN y

FUNCTION balance_node(node, key):
    node.height = 1 + MAX(height(node.left), height(node.right))
    bf = height(node.left) - height(node.right)

    # LL Case
    IF bf > 1 AND key < node.left.key:
        RETURN right_rotate(node)
    # RR Case
    IF bf < -1 AND key > node.right.key:
        RETURN left_rotate(node)
    # LR Case
    IF bf > 1 AND key > node.left.key:
        node.left = left_rotate(node.left)
        RETURN right_rotate(node)
    # RL Case
    IF bf < -1 AND key < node.right.key:
        node.right = right_rotate(node.right)
        RETURN left_rotate(node)

    RETURN node
```

---

## 15. Expression Tree Construction and Evaluation

### Pseudocode: Postfix to Expression Tree
```text
FUNCTION build_expression_tree(postfix_string):
    tokens = SPLIT(postfix_string)
    stack = []
    FOR token IN tokens:
        IF token IN ['+', '-', '*', '/', '^']:
            IF LENGTH(stack) < 2: RAISE ValueError("Malformed expression")
            right_child = stack.POP()
            left_child = stack.POP()
            node = NEW ExprNode(token)
            node.left = left_child
            node.right = right_child
            stack.PUSH(node)
        ELSE:
            val = PARSE_FLOAT(token)
            stack.PUSH(NEW ExprNode(token))
    IF LENGTH(stack) != 1: RAISE ValueError("Malformed expression")
    RETURN stack.POP()

FUNCTION evaluate_expression_tree(node):
    IF node.is_leaf():
        RETURN TO_FLOAT(node.value)
    left_val = evaluate_expression_tree(node.left)
    right_val = evaluate_expression_tree(node.right)
    SWITCH node.value:
        CASE '+': RETURN left_val + right_val
        CASE '-': RETURN left_val - right_val
        CASE '*': RETURN left_val * right_val
        CASE '/':
            IF right_val == 0.0: RAISE ZeroDivisionError()
            RETURN left_val / right_val
        CASE '^': RETURN left_val ^ right_val
```

---

## 16. Time and Space Complexity Analysis

| Program | Operation | Best Case | Average Case | Worst Case | Auxiliary Space |
|:---|:---|:---:|:---:|:---:|:---:|
| **Program 1: Recursive Traversals** | Preorder / Inorder / Postorder | $\Theta(n)$ | $\Theta(n)$ | $O(n)$ | $O(h)$ |
| **Program 2: Iterative Traversals** | Preorder / Inorder | $\Theta(n)$ | $\Theta(n)$ | $O(n)$ | $O(h)$ |
| | Postorder (2 Stacks) | $\Theta(n)$ | $\Theta(n)$ | $O(n)$ | $O(n)$ |
| **Program 3: Binary Search Tree** | Search | $\Theta(1)$ | $\Theta(\log n)$ | $O(n)$ | $O(h)$ |
| | Insert | $\Theta(\log n)$ | $\Theta(\log n)$ | $O(n)$ | $O(h)$ |
| | Delete | $\Theta(\log n)$ | $\Theta(\log n)$ | $O(n)$ | $O(h)$ |
| | Inorder Traversal | $\Theta(n)$ | $\Theta(n)$ | $O(n)$ | $O(h)$ |
| **Program 4: AVL Tree** | Search | $\Theta(1)$ | $\Theta(\log n)$ | **$O(\log n)$** | $O(\log n)$ |
| | Insert | $\Theta(\log n)$ | $\Theta(\log n)$ | **$O(\log n)$** | $O(\log n)$ |
| | Delete | $\Theta(\log n)$ | $\Theta(\log n)$ | **$O(\log n)$** | $O(\log n)$ |
| **Program 5: Expression Tree** | Construction | $\Theta(n)$ | $\Theta(n)$ | $O(n)$ | $O(n)$ |
| | Recursive Evaluation | $\Theta(n)$ | $\Theta(n)$ | $O(n)$ | $O(n)$ |
| **Program 6: File System Simulator** | Create File/Dir (`mkdir`/`touch`)| $\Theta(1)$ | $\Theta(k)$ | $O(k)$ | $O(1)$ |
| | Search Tree | $\Theta(N)$ | $\Theta(N)$ | $O(N)$ | $O(d)$ |
| **Program 7: Symbol Table (BST)** | Lookup / Update | $\Theta(1)$ | $\Theta(\log n)$ | $O(n)$ | $O(h)$ |
| | Insert Symbol | $\Theta(\log n)$ | $\Theta(\log n)$ | $O(n)$ | $O(h)$ |
| | Delete Symbol | $\Theta(\log n)$ | $\Theta(\log n)$ | $O(n)$ | $O(h)$ |

---

## 17. Testing and Sample I/O

All seven programs contain comprehensive automated unit test suites triggered via the `--test` CLI flag.

### Execution Command
```console
$ python3 Lab06-Trees/Program01-RecursiveTraversals/recursive_traversals.py --test && \
  python3 Lab06-Trees/Program02-IterativeTraversals/iterative_traversals.py --test && \
  python3 Lab06-Trees/Program03-BinarySearchTree/binary_search_tree.py --test && \
  python3 Lab06-Trees/Program04-AVLTree/avl_tree.py --test && \
  python3 Lab06-Trees/Program05-ExpressionTree/expression_tree.py --test && \
  python3 Lab06-Trees/Program06-FileSystemSimulator/file_system.py --test && \
  python3 Lab06-Trees/Program07-SymbolTable/symbol_table.py --test
```

### Actual Output Log
```text
======================================================================
RUNNING AUTOMATED TEST SUITE: Binary Tree Recursive Traversals
======================================================================
[PASS] Test 1: Empty tree traversals handled correctly.
[PASS] Test 2: Single-node tree traversals verified.
[PASS] Test 3: Preorder verified  -> [1, 2, 4, 5, 3, 6, 7]
[PASS] Test 4: Inorder verified   -> [4, 2, 5, 1, 6, 3, 7]
[PASS] Test 5: Postorder verified -> [4, 5, 2, 6, 7, 3, 1]

ALL 5 TEST CASES PASSED SUCCESSFULLY!
======================================================================
======================================================================
RUNNING AUTOMATED TEST SUITE: Binary Tree Iterative Traversals
======================================================================
[PASS] Test 1: Empty tree handled correctly.
[PASS] Test 2: Single-node tree handled correctly.
[PASS] Test 3: Iterative Preorder matches reference  -> [1, 2, 4, 5, 3, 6, 7]
[PASS] Test 4: Iterative Inorder matches reference   -> [4, 2, 5, 1, 6, 3, 7]
[PASS] Test 5: Iterative Postorder matches reference -> [4, 5, 2, 6, 7, 3, 1]

ALL 5 TEST CASES PASSED SUCCESSFULLY!
======================================================================
======================================================================
RUNNING AUTOMATED TEST SUITE: Binary Search Tree (BST)
======================================================================
[PASS] Test 1: Initial empty tree state and validation verified.
[PASS] Test 2: Insertions, min, max, and sorted inorder verified.
[PASS] Test 3: Search hits and misses verified.
[PASS] Test 4: Duplicate insertion rejection verified.
[PASS] Test 5: Deletion Case 1 (Leaf node deletion) verified.
[PASS] Test 6: Deletion Case 2 (One child node deletion) verified.
[PASS] Test 7: Deletion Case 3 (Two children node deletion) verified.
[PASS] Test 8: Non-existent key deletion error handling verified.

ALL 8 TEST CASES PASSED SUCCESSFULLY!
======================================================================
======================================================================
RUNNING AUTOMATED TEST SUITE: Self-Balancing AVL Tree
======================================================================
[PASS] Test 1: Case 1 (LL Rotation -> Single Right Rotate) verified.
[PASS] Test 2: Case 2 (RR Rotation -> Single Left Rotate) verified.
[PASS] Test 3: Case 3 (LR Rotation -> Double Rotation Left-Right) verified.
[PASS] Test 4: Case 4 (RL Rotation -> Double Rotation Right-Left) verified.
[PASS] Test 5: Multi-element insertion & continuous balance verified.
[PASS] Test 6: Deletion with automatic rebalancing verified.

ALL 6 TEST CASES PASSED SUCCESSFULLY!
======================================================================
======================================================================
RUNNING AUTOMATED TEST SUITE: Expression Tree
======================================================================
[PASS] Test 1: Standard arithmetic '(10 + 20) * 3' verified.
[PASS] Test 2: Exponentiation and division '((5 + 3) ^ 2) / 4' verified.
[PASS] Test 3: Floating point operands verified.
[PASS] Test 4: Division by zero caught cleanly.
[PASS] Test 5: Malformed expression (insufficient operands) caught.
[PASS] Test 6: Malformed expression (leftover operands) caught.
[PASS] Test 7: Invalid alphanumeric token rejected.

ALL 7 TEST CASES PASSED SUCCESSFULLY!
======================================================================
======================================================================
RUNNING AUTOMATED TEST SUITE: File System Simulator (N-ary Tree)
======================================================================
[PASS] Test 1: Root directory initialized.
[PASS] Test 2: Directory and file creation verified.
[PASS] Test 3: Duplicate name rejection verified.
[PASS] Test 4: Path navigation (cd and cd ..) verified.
[PASS] Test 5: Recursive file search verified.
[PASS] Test 6: Non-empty directory safety and recursive deletion verified.
[PASS] Test 7: Multi-level sample tree search and navigation verified.

ALL 7 TEST CASES PASSED SUCCESSFULLY!
======================================================================
======================================================================
RUNNING AUTOMATED TEST SUITE: Compiler Symbol Table (BST)
======================================================================
[PASS] Test 1: Empty symbol table initialized.
[PASS] Test 2: Symbol insertions verified.
[PASS] Test 3: Alphabetical ordering (alpha -> beta -> gamma) verified.
[PASS] Test 4: Duplicate identifier rejection verified.
[PASS] Test 5: Identifier lookup hit and miss verified.
[PASS] Test 6: Symbol update and missing validation verified.
[PASS] Test 7: Symbol deletion and missing identifier validation verified.

ALL 7 TEST CASES PASSED SUCCESSFULLY!
======================================================================
```

---

## 18. Real-Life Applications

1. **Operating System File Systems**: Unix/Linux VFS, ext4, and Windows NTFS represent directory hierarchies as general trees where internal nodes are directories and leaf nodes are files.
2. **Compiler & Interpreter Frontends**: Source code is parsed into Abstract Syntax Trees (ASTs) and Expression Trees, enabling syntactic validation, constant folding, and intermediate representation (IR) code generation.
3. **Database Indexing**: Relational database management systems (RDBMS) such as PostgreSQL and MySQL InnoDB utilize self-balancing tree variants ($B+$ Trees and AVL derivatives) to execute primary key index lookups in guaranteed logarithmic time.
4. **Domain Name System (DNS)**: The global Internet domain name resolution hierarchy (`.` root $\to$ `.com`, `.org` TLDs $\to$ domain names $\to$ subdomains) is organized as a distributed tree.
5. **DOM Trees in Web Browsers**: HTML web pages are rendered into the Document Object Model (DOM) tree, where CSS styling cascades downward and JavaScript traverses nodes to manipulate user interfaces.

---

## 19. Folder Structure

```text
Lab06-Trees/
├── Program01-RecursiveTraversals/
│   └── recursive_traversals.py
├── Program02-IterativeTraversals/
│   └── iterative_traversals.py
├── Program03-BinarySearchTree/
│   └── binary_search_tree.py
├── Program04-AVLTree/
│   └── avl_tree.py
├── Program05-ExpressionTree/
│   └── expression_tree.py
├── Program06-FileSystemSimulator/
│   └── file_system.py
├── Program07-SymbolTable/
│   └── symbol_table.py
├── README.md
└── reflection.md
```

---

## 20. Execution Instructions

Every program is completely self-contained and executable in two modes: an **interactive menu-driven CLI mode** and an **automated test mode** via `--test`.

### 1. Interactive Menu Mode
```bash
python3 Lab06-Trees/Program01-RecursiveTraversals/recursive_traversals.py
python3 Lab06-Trees/Program02-IterativeTraversals/iterative_traversals.py
python3 Lab06-Trees/Program03-BinarySearchTree/binary_search_tree.py
python3 Lab06-Trees/Program04-AVLTree/avl_tree.py
python3 Lab06-Trees/Program05-ExpressionTree/expression_tree.py
python3 Lab06-Trees/Program06-FileSystemSimulator/file_system.py
python3 Lab06-Trees/Program07-SymbolTable/symbol_table.py
```

### 2. Automated Test Verification Mode
```bash
python3 Lab06-Trees/Program01-RecursiveTraversals/recursive_traversals.py --test
python3 Lab06-Trees/Program02-IterativeTraversals/iterative_traversals.py --test
python3 Lab06-Trees/Program03-BinarySearchTree/binary_search_tree.py --test
python3 Lab06-Trees/Program04-AVLTree/avl_tree.py --test
python3 Lab06-Trees/Program05-ExpressionTree/expression_tree.py --test
python3 Lab06-Trees/Program06-FileSystemSimulator/file_system.py --test
python3 Lab06-Trees/Program07-SymbolTable/symbol_table.py --test
```

---

## 21. Learning Outcomes

By completing Unit 6, students have achieved:
1. **Tree Architecture Fluency**: Understanding non-linear hierarchical models, node depth, height invariants, and pointer link mechanics.
2. **Traversal Mastery**: Fluency in recursive and stack-based iterative traversals across Preorder, Inorder, and Postorder schemes.
3. **BST Algorithmics**: Implementation of BST search, insert, and the three structural deletion cases (leaf, single child, and inorder successor replacement).
4. **Self-Balancing Tree Engineering**: Complete mathematical and practical understanding of AVL trees, balance factors ($\text{BF} \in \{-1, 0, 1\}$), and the four rotation primitives (LL, RR, LR, RL) that guarantee $O(\log n)$ runtime.
5. **Expression Tree & Evaluation**: Parsing postfix expressions using an explicit node stack, converting across prefix/infix/postfix notations, and evaluating arithmetic expressions recursively without `eval()`.
6. **Systems Modeling**: Applying tree structures to model real-world operating system file hierarchies and compiler symbol tables.

---

## 22. References

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press. Chapter 10: Elementary Data Structures, Chapter 12: Binary Search Trees, Chapter 13: Red-Black & Balanced Trees.
2. Adelson-Velsky, G. M., & Landis, E. M. (1962). *An algorithm for the organization of information*. Proceedings of the USSR Academy of Sciences, 146: 263–266.
3. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Addison-Wesley. Chapter 2: A Simple Syntax-Directed Translator (Expression Trees, Symbol Tables).
4. Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2013). *Data Structures and Algorithms in Python*. John Wiley & Sons. Chapter 8: Trees, Chapter 11: Search Trees.

