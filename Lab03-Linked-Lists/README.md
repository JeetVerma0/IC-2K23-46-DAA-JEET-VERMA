# IC-307D: Data Structures and Algorithms Lab
## Unit 3: Linked Lists (CO1)

---

## 1. Introduction

A **linked list** is a fundamental dynamic linear data structure wherein elements—termed **nodes**—are not stored in contiguous physical memory locations. Instead, each node consists of two essential parts:
1. **Data payload**: The actual value, object, or record stored within the node.
2. **Pointer / Reference field(s)**: One or more memory references directing to the neighboring node(s) in the sequence.

Unlike contiguous data structures like arrays where element memory is allocated in one homogeneous chunk and sequential indexing relies on arithmetic offsets ($\text{Address}(A[i]) = \text{Base} + i \times \text{Size}$), linked lists allocate memory dynamically on the heap for each node as needed. This structural property provides two distinct algorithmic advantages:
- **Dynamic Resizing**: A linked list can expand or shrink arbitrarily at runtime without requiring upfront capacity declaration or costly geometric array reallocations.
- **Constant-Time Insertions and Deletions**: Inserting or removing an element at a known location (such as the beginning or adjacent to an active pointer) requires only local pointer updates ($O(1)$ time) without shifting subsequent elements rightward or leftward.

However, non-contiguity also introduces trade-offs:
- **Sequential Access**: Direct random indexing in $O(1)$ time is impossible; accessing the $k$-th element requires traversing $k$ pointer references from the head in $O(n)$ time.
- **Reference Overhead**: Storing explicit pointer fields (`next`, `prev`) consumes auxiliary memory per node ($8$ to $16$ bytes on 64-bit systems).
- **Cache Locality**: Dynamically allocated nodes may reside in fragmented heap memory pages, diminishing CPU L1/L2 cache prefetching efficiency compared to contiguous arrays.

Linked lists branch into three principal topological variants:
1. **Singly Linked List (SLL)**: Unidirectional traversal where each node references exclusively its succeeding node (`next`), culminating in a terminal `None` / `NULL`.
2. **Doubly Linked List (DLL)**: Bidirectional traversal where each node maintains references to both its successor (`next`) and predecessor (`prev`), facilitating $O(1)$ operations at both boundaries (`head` and `tail`) and reverse traversal.
3. **Circular Linked List (CLL)**: A closed loop where the terminal node links directly back to the head node, supporting continuous round-robin scheduling and repetitive cycling.

This laboratory unit explores the design, theoretical analysis, manual implementation from first principles, and practical application of linked lists—culminating in algebraic polynomial manipulation, an interactive text editor line buffer, and a circular media playlist engine.

---

## 2. Aim

To study, design, implement from first principles, test, and analyze Singly Linked Lists, Doubly Linked Lists, and Circular Linked Lists in Python 3 without utilizing built-in lists as data stores; to implement core operations (insertion at arbitrary positions, deletion, searching, in-place reversal, and concatenation); and to engineer real-world systems including an algebraic Polynomial Arithmetic Engine, a Text Editor Line Buffer, and a Music Playlist Manager.

---

## 3. Learning Objectives

By completing this laboratory unit, students will be able to:

1. **Understand Heap Memory and Node References**:
   - Master explicit pointer reference assignment, dereferencing, and garbage collection mechanisms in node-based structures.
   - Contrast contiguous memory layouts (arrays) with scattered heap memory layouts (linked structures).
2. **Implement Core Singly Linked List Operations**:
   - Construct a `Node` class and implement zero-based positional insertion, boundary deletion, linear search, in-place pointer reversal, and list concatenation.
3. **Master Bidirectional Pointer Linking in Doubly Linked Lists**:
   - Maintain dual `head` and `tail` pointers to achieve $O(1)$ operations at both ends.
   - Accurately manage invariant symmetry: $\text{node.next.prev} == \text{node}$ and $\text{node.prev.next} == \text{node}$.
   - Implement in-place reversal by swapping predecessor and successor pointers for every node.
4. **Construct Cycle-Safe Circular Linked Lists**:
   - Form self-referential cycles ($\text{node.next} == \text{node}$) and ring topologies ($\text{last.next} == \text{head}$).
   - Develop cycle-termination criteria to display, search, reverse, and concatenate circular lists without causing infinite loops.
5. **Apply Linked Lists to Domain-Specific Problems**:
   - **Polynomial Arithmetic**: Model multivariable or single-variable polynomials using node records `(coeff, exp, next)`, maintaining descending exponent order and executing two-pointer merge addition in $O(n + m)$ time.
   - **Text Editor Buffer**: Utilize a doubly linked list to model an in-memory document, achieving $O(1)$ cursor movement and localized line edits without shifting array blocks.
   - **Music Playlist Manager**: Implement a Circular Doubly Linked List (CDLL) providing $O(1)$ bidirectional song navigation, track insertion/removal, and infinite loop playback.
6. **Evaluate Time and Space Complexity**:
   - Mathematically analyze pointer traversal overheads, best/worst-case execution scenarios, and auxiliary memory footprints.

---

## 4. Software Requirements

- **Programming Language**: Python 3.8+ (Standard Library)
- **Execution Shell**: GNU Bash 5.0+ / Linux CLI
- **Operating System**: Linux (Ubuntu/Debian-based x86_64)
- **Development Tooling**: Antigravity IDE / Terminal CLI
- **Dependencies**: Pure Python standard library (`typing`, `sys`). No external data structure packages, arrays, or built-in list proxies are used for primary data storage.

---

## 5. Experiment 1: Singly Linked List

### Problem Statement
Implement a complete Singly Linked List from first principles in [singly_linked_list.py](file:///home/jeet/Desktop/Data_structures/Lab03-Linked-Lists/Program01-SinglyLinkedList/singly_linked_list.py). The system must support zero-based positional insertions (beginning, middle, end), deletions (beginning, middle, end), linear searching, in-place pointer reversal, and concatenation of another singly linked list, with defensive handling of empty lists and invalid index boundaries.

### Approach & Memory Organization
A Singly Linked List is composed of isolated `Node` objects allocated on the system heap. The [`SinglyLinkedList`](file:///home/jeet/Desktop/Data_structures/Lab03-Linked-Lists/Program01-SinglyLinkedList/singly_linked_list.py#L36) class maintains a single external reference, `head`, pointing to the first node (or `None` if empty), alongside an integer `_size`.
- **Zero-based Indexing**:
  - Index $0$ references the `head` node directly.
  - Index $k$ represents the node reached after traversing $k$ `next` links from `head`.
  - Valid insertion positions are $0 \le \text{pos} \le n$ (where $\text{pos} == n$ appends to the tail).
  - Valid deletion positions are $0 \le \text{pos} < n$.

```
+------------+      +------------+      +------------+
| data: 10   | ---> | data: 20   | ---> | data: 30   | ---> None
| next: ref  |      | next: ref  |      | next: None |
+------------+      +------------+      +------------+
  ^
  head
```

### Algorithm

#### 1. Insertion at Position $k$ (`insert_at_position`):
1. If $k < 0$ or $k > n$, raise `IndexError`.
2. Allocate `new_node = Node(data)`.
3. If $k == 0$:
   - Set `new_node.next = head`.
   - Update `head = new_node`.
4. Else:
   - Traverse pointer `curr` from `head` for $k - 1$ steps.
   - Set `new_node.next = curr.next`.
   - Set `curr.next = new_node`.
5. Increment `_size` by 1.

#### 2. Deletion at Position $k$ (`delete_at_position`):
1. If `head is None`, raise `IndexError`.
2. If $k < 0$ or $k \ge n$, raise `IndexError`.
3. If $k == 0$:
   - Store `deleted_data = head.data`.
   - Update `head = head.next`.
4. Else:
   - Traverse pointer `curr` to index $k - 1$.
   - Let `target = curr.next`.
   - Store `deleted_data = target.data`.
   - Update `curr.next = target.next`.
   - Disconnect `target.next = None`.
5. Decrement `_size` by 1. Return `deleted_data`.

#### 3. In-Place Reversal (`reverse`):
1. Initialize three pointers: `prev = None`, `curr = head`.
2. While `curr is not None`:
   - Store successor: `next_node = curr.next`.
   - Reverse link: `curr.next = prev`.
   - Step forward: `prev = curr`, `curr = next_node`.
3. Update `head = prev`.

### Pseudocode
```text
FUNCTION insert_at_position(data, pos):
    IF pos < 0 OR pos > size THEN THROW IndexError
    new_node = ALLOCATE Node(data)
    IF pos == 0 THEN:
        new_node.next = head
        head = new_node
    ELSE:
        curr = head
        FOR i FROM 0 TO pos - 2 DO:
            curr = curr.next
        new_node.next = curr.next
        curr.next = new_node
    size = size + 1
END FUNCTION

FUNCTION reverse():
    prev = None
    curr = head
    WHILE curr != None DO:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    head = prev
END FUNCTION
```

### Dry Run
Reversing list `10 -> 20 -> 30 -> None`:
- **Initial**: `head = 10`, `prev = None`, `curr = 10`.
- **Step 1**: `next_node = 20`. `10.next = None`. `prev = 10`, `curr = 20`.
- **Step 2**: `next_node = 30`. `20.next = 10`. `prev = 20`, `curr = 30`.
- **Step 3**: `next_node = None`. `30.next = 20`. `prev = 30`, `curr = None`.
- **Final**: `head = prev = 30`. Resulting list: `30 -> 20 -> 10 -> None`.

### Complexity Analysis
- **Insert at Beginning**: $O(1)$ time, $O(1)$ space.
- **Insert at End / Position $k$**: $O(n)$ traversal time, $O(1)$ space.
- **Delete from Beginning**: $O(1)$ time, $O(1)$ space.
- **Delete from End / Position $k$**: $O(n)$ traversal time, $O(1)$ space.
- **Search**: Best case $O(1)$ (target at head), Average/Worst case $O(n)$, $O(1)$ space.
- **Reversal**: $O(n)$ time, $O(1)$ auxiliary space.
- **Concatenation**: $O(n + m)$ time, $O(m)$ space for copied nodes.

### Real-Life Applications
- Operating system memory allocation free lists (e.g., Buddy allocator free blocks).
- Blockchain block chains where each block headers point to the preceding block hash.
- Undo stacks and transaction log queues with frequent front operations.

---

## 6. Experiment 2: Doubly Linked List

### Problem Statement
Implement a Doubly Linked List in [doubly_linked_list.py](file:///home/jeet/Desktop/Data_structures/Lab03-Linked-Lists/Program02-DoublyLinkedList/doubly_linked_list.py) supporting bidirectional traversal, dual boundary references (`head` and `tail`), positional insertions and deletions, linear search, in-place reversal by swapping pointer references, and concatenation, with complete preservation of the invariant $\text{node.next.prev} == \text{node}$.

### Approach & Memory Organization
Each [`DoublyNode`](file:///home/jeet/Desktop/Data_structures/Lab03-Linked-Lists/Program02-DoublyLinkedList/doubly_linked_list.py#L22) encapsulates three fields: `data`, `prev` (pointing to the preceding node), and `next` (pointing to the succeeding node). Maintaining both `head` and `tail` enables constant-time operations at both ends of the collection.

```
None <- +-------------+ <=> +-------------+ <=> +-------------+ -> None
        | prev: None  |     | prev: ref   |     | prev: ref   |
        | data: 10    |     | data: 20    |     | data: 30    |
        | next: ref   |     | next: ref   |     | next: None  |
        +-------------+     +-------------+     +-------------+
          ^                                       ^
          head                                    tail
```

### Algorithm

#### 1. Insertion at End (`insert_end`):
1. Allocate `new_node = DoublyNode(data)`.
2. If `tail is None`: set `head = tail = new_node`.
3. Else:
   - `tail.next = new_node`.
   - `new_node.prev = tail`.
   - `tail = new_node`.
4. Increment `_size` by 1.

#### 2. Bidirectional Deletion at Position $k$ (`delete_at_position`):
1. If list is empty, raise `IndexError`. If $k < 0$ or $k \ge n$, raise `IndexError`.
2. If $k == 0$: call `delete_beginning()`. If $k == n - 1$: call `delete_end()`.
3. Traverse to node at index $k$ (optimizing direction: traverse from `head` if $k \le n/2$, else from `tail`).
4. Update references:
   - `curr.prev.next = curr.next`.
   - `curr.next.prev = curr.prev`.
5. Decrement `_size` by 1. Return `curr.data`.

#### 3. In-Place Reversal (`reverse`):
1. If list is empty or has 1 node, return.
2. Initialize `curr = head`, store `new_tail = head`.
3. While `curr is not None`:
   - Swap pointers: `temp = curr.prev; curr.prev = curr.next; curr.next = temp`.
   - Advance: `curr = curr.prev` (since `prev` now holds the original `next`).
4. Update `head = tail`, `tail = new_tail`.

### Pseudocode
```text
FUNCTION reverse():
    IF head == None OR head == tail THEN RETURN
    curr = head
    new_tail = head
    WHILE curr != None DO:
        temp = curr.prev
        curr.prev = curr.next
        curr.next = temp
        curr = curr.prev
    head = tail
    tail = new_tail
END FUNCTION
```

### Dry Run
Reversing `None <- 10 <=> 20 <=> 30 -> None`:
- **Node 10**: Swap: `prev` becomes ref to 20, `next` becomes `None`. Advance to 20.
- **Node 20**: Swap: `prev` becomes ref to 30, `next` becomes ref to 10. Advance to 30.
- **Node 30**: Swap: `prev` becomes `None`, `next` becomes ref to 20. Advance to `None`.
- **Termination**: `head = 30`, `tail = 10`. Result: `None <- 30 <=> 20 <=> 10 -> None`.

### Complexity Analysis
- **Insert at Beginning / End**: Strictly $O(1)$ time, $O(1)$ space.
- **Insert / Delete at Position $k$**: $O(n/2) = O(n)$ traversal, $O(1)$ space.
- **Forward / Backward Traversal**: $O(n)$ time, $O(n)$ space.
- **In-Place Reversal**: $O(n)$ time, $O(1)$ auxiliary space.

### Real-Life Applications
- Web browser forward and backward navigation history.
- LRU (Least Recently Used) cache architectures (coupled with hash maps).
- Undo and redo buffers in graphics software.

---

## 7. Experiment 3: Circular Linked List

### Problem Statement
Implement a Circular Singly Linked List in [circular_linked_list.py](file:///home/jeet/Desktop/Data_structures/Lab03-Linked-Lists/Program03-CircularLinkedList/circular_linked_list.py) where the terminal node wraps around to point back to the `head`. Provide complete insertion, deletion, searching, in-place reversal, and concatenation operations while guaranteeing that traversals terminate strictly without infinite loops.

### Approach & Memory Organization
In a Circular Singly Linked List, there is no `None` sentinel. 
- For an empty list: `head = None`.
- For a single-node list: `head.next = head` (self-referential loop).
- For an $n$-node list: `last.next = head`.

```
         +-------------------------------------------------+
         |                                                 |
         v                                                 |
  +------------+      +------------+      +------------+   |
  | data: 10   | ---> | data: 20   | ---> | data: 30   | --+
  | next: ref  |      | next: ref  |      | next: head |
  +------------+      +------------+      +------------+
    ^
    head
```

### Algorithm

#### 1. Insertion at Beginning (`insert_beginning`):
1. Allocate `new_node = CircularNode(data)`.
2. If `head is None`:
   - `new_node.next = new_node`.
   - `head = new_node`.
3. Else:
   - Traverse to last node (where `curr.next == head`).
   - `new_node.next = head`.
   - `last.next = new_node`.
   - `head = new_node`.
4. Increment `_size` by 1.

#### 2. Deletion at Beginning (`delete_beginning`):
1. If `head is None`, raise `IndexError`.
2. If `head.next == head` (single-node):
   - Store `val = head.data`. `head = None`.
3. Else:
   - Traverse to last node (`last.next == head`).
   - Store `val = head.data`.
   - `last.next = head.next`.
   - `head = head.next`.
4. Decrement `_size` by 1. Return `val`.

#### 3. In-Place Circular Reversal (`reverse`):
1. If list has $\le 1$ node, return.
2. Store `original_head = head`.
3. Initialize `prev = None`, `curr = head`.
4. Traverse loop once:
   - `next_node = curr.next`.
   - `curr.next = prev`.
   - `prev = curr`, `curr = next_node`.
   - If `curr == original_head`, break.
5. Link new tail (`original_head.next = prev`).
6. Set `head = prev`.

### Pseudocode
```text
FUNCTION reverse():
    IF head == None OR head.next == head THEN RETURN
    orig_head = head
    prev = None
    curr = head
    REPEAT:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    UNTIL curr == orig_head
    orig_head.next = prev
    head = prev
END FUNCTION
```

### Dry Run
Given `10 -> 20 -> 30 -> (back to 10)`:
- `orig_head = 10`.
- Iteration 1: `10.next = None`, `prev = 10`, `curr = 20`.
- Iteration 2: `20.next = 10`, `prev = 20`, `curr = 30`.
- Iteration 3: `30.next = 20`, `prev = 30`, `curr = 10` (cycle completes, loop terminates).
- Relink tail: `orig_head.next = prev` $\implies 10.\text{next} = 30$.
- Update `head = 30`.
- Output: `30 -> 20 -> 10 -> (back to 30)`.

### Complexity Analysis
- **Insert / Delete at Beginning or End**: $O(n)$ without tail pointer; $O(1)$ auxiliary space.
- **Search & Traversal**: $O(n)$ time bounded by one full cycle.
- **In-Place Reversal**: $O(n)$ time, $O(1)$ space.
- **Concatenation**: $O(m)$ time, $O(m)$ space for copied nodes.

### Real-Life Applications
- Round-Robin process scheduling in operating system CPU dispatchers.
- Multiplayer turn-based gaming systems where player turns cycle continuously.
- Billboard and electronic carousel displays.

---

## 8. Experiment 4: Polynomial Representation and Addition

### Problem Statement
Design an algebraic polynomial engine in [polynomial_operations.py](file:///home/jeet/Desktop/Data_structures/Lab03-Linked-Lists/Program04-PolynomialOperations/polynomial_operations.py) using linked lists. Each term must be represented as an individual node storing coefficient, exponent, and a next reference. The program must combine like terms, keep terms strictly ordered by descending exponent, handle zero coefficients and complete polynomial cancellation, and add two polynomials using a two-pointer merge algorithm in $O(n + m)$ time.

### Approach & Memory Organization
Each term of polynomial $P(x) = \sum c_i x^{e_i}$ is stored in a [`PolyNode`](file:///home/jeet/Desktop/Data_structures/Lab03-Linked-Lists/Program04-PolynomialOperations/polynomial_operations.py#L22):
- `coeff`: Numeric multiplier.
- `exp`: Non-negative integer power.
- `next`: Pointer to the term with the next strictly smaller exponent.

```
+--------------------+      +--------------------+      +--------------------+
| coeff: 5           | ---> | coeff: -3          | ---> | coeff: 7           | ---> None
| exp:   3           |      | exp:   1           |      | exp:   0           |
+--------------------+      +--------------------+      +--------------------+
  5x^3 - 3x + 7
```

### Algorithm: Polynomial Addition (`add`)
1. Initialize two pointers: $p_1 = \text{poly}_1.\text{head}$ and $p_2 = \text{poly}_2.\text{head}$.
2. Initialize an empty result polynomial with `result_tail = None`.
3. While $p_1 \neq \text{None}$ and $p_2 \neq \text{None}$:
   - **Case A ($p_1.\text{exp} == p_2.\text{exp}$)**:
     - Compute $\text{sum\_coeff} = p_1.\text{coeff} + p_2.\text{coeff}$.
     - If $\text{sum\_coeff} \neq 0$: append term $(\text{sum\_coeff}, p_1.\text{exp})$ to result.
     - Advance both $p_1 \leftarrow p_1.\text{next}$ and $p_2 \leftarrow p_2.\text{next}$.
   - **Case B ($p_1.\text{exp} > p_2.\text{exp}$)**:
     - Append term $(p_1.\text{coeff}, p_1.\text{exp})$ to result.
     - Advance $p_1 \leftarrow p_1.\text{next}$.
   - **Case C ($p_2.\text{exp} > p_1.\text{exp}$)**:
     - Append term $(p_2.\text{coeff}, p_2.\text{exp})$ to result.
     - Advance $p_2 \leftarrow p_2.\text{next}$.
4. Drain remaining nodes from $p_1$ or $p_2$.
5. Return result polynomial.

### Pseudocode
```text
FUNCTION add(poly1, poly2):
    result = ALLOCATE Polynomial()
    p1 = poly1.head
    p2 = poly2.head
    WHILE p1 != None AND p2 != None DO:
        IF p1.exp == p2.exp THEN:
            c = p1.coeff + p2.coeff
            IF c != 0 THEN APPEND_TERM(result, c, p1.exp)
            p1 = p1.next; p2 = p2.next
        ELSE IF p1.exp > p2.exp THEN:
            APPEND_TERM(result, p1.coeff, p1.exp)
            p1 = p1.next
        ELSE:
            APPEND_TERM(result, p2.coeff, p2.exp)
            p2 = p2.next
    DRAIN remaining p1, p2 TO result
    RETURN result
END FUNCTION
```

### Dry Run
Add $P_1(x) = 3x^2 + 5x + 2$ and $P_2(x) = 4x^2 - 2x + 6$:
- $p_1 = (3, 2), p_2 = (4, 2)$: Equal exp $2 \implies c = 3 + 4 = 7$. Append $7x^2$. Advance both.
- $p_1 = (5, 1), p_2 = (-2, 1)$: Equal exp $1 \implies c = 5 + (-2) = 3$. Append $3x$. Advance both.
- $p_1 = (2, 0), p_2 = (6, 0)$: Equal exp $0 \implies c = 2 + 6 = 8$. Append $8$. Advance both.
- **Sum**: $7x^2 + 3x + 8$.

Cancellation: $(4x^3 + 2x - 7) + (-4x^3 - 2x + 7) \implies \text{all coefficients sum to } 0 \implies \text{Result} = 0$.

### Complexity Analysis
- **Addition Time**: Strictly $O(n + m)$ linear merge where $n$ and $m$ are the number of terms.
- **Auxiliary Space**: $O(n + m)$ for new result nodes.
- **Term Insertion**: $O(n)$ maintaining sorted exponent order.

### Real-Life Applications
- Computer Algebra Systems (CAS) like Mathematica, Maple, and SymPy for symbolic mathematical manipulation.
- Signal processing digital filters (FIR/IIR filter z-transforms).

---

## 9. Experiment 5: Text Editor Buffer

### Problem Statement
Develop an interactive, in-memory Text Editor Line Buffer in [text_editor_buffer.py](file:///home/jeet/Desktop/Data_structures/Lab03-Linked-Lists/Program05-TextEditorBuffer/text_editor_buffer.py) using a Doubly Linked List. The system must support inserting lines at arbitrary 1-based positions, deleting lines, editing lines, bidirectional cursor movement (`move_cursor_next`, `move_cursor_prev`), cursor tracking, and formatted document display without using Python lists as primary storage.

### Approach & Memory Organization
Each line of text is encapsulated inside a [`TextLineNode`](file:///home/jeet/Desktop/Data_structures/Lab03-Linked-Lists/Program05-TextEditorBuffer/text_editor_buffer.py#L24) containing `text`, `prev`, and `next`. 
- **Cursor Tracking**: Maintains a direct pointer reference, `cursor`, to the active line node and integer `cursor_line` (1-based index).
- **Why Doubly Linked List?**
  In an array of lines, inserting a line at Line 2 of a 100,000-line file requires shifting 99,998 array pointers rightward ($O(n)$ overhead). In a doubly linked list, once the cursor or target position is located, insertion or deletion requires only updating 4 pointer references ($O(1)$ time). Bidirectional cursor navigation (`Up` and `Down` arrow keys) is an immediate $O(1)$ operation via `cursor.prev` and `cursor.next`.

```
None <- +---------------------------+ <=> +---------------------------+ -> None
        | text: "Line 1: Hello"     |     | text: "Line 2: World"     |
        | prev: None | next: ref    |     | prev: ref | next: None    |
        +---------------------------+     +---------------------------+
          ^                                 ^
          head                              tail / cursor (Line 2)
```

### Algorithm

#### 1. Cursor Navigation (`move_cursor_next` / `move_cursor_prev`):
- `move_cursor_next()`: If `cursor is not None` and `cursor.next is not None`, set `cursor = cursor.next`, increment `cursor_line` by 1. Return `True`. Else return `False`.
- `move_cursor_prev()`: If `cursor is not None` and `cursor.prev is not None`, set `cursor = cursor.prev`, decrement `cursor_line` by 1. Return `True`. Else return `False`.

#### 2. Line Insertion at Position $k$ (`insert_line`):
1. If $k < 1$ or $k > \text{line\_count} + 1$, raise `IndexError`.
2. Allocate `new_node = TextLineNode(text)`.
3. If buffer empty: `head = tail = new_node`.
4. If $k == 1$: link before `head`, update `head`.
5. If $k == \text{line\_count} + 1$: link after `tail`, update `tail`.
6. Else: traverse to node at line $k$, splice `new_node` between `target.prev` and `target`.
7. Set `cursor = new_node`, `cursor_line = k`. Increment `_line_count`.

### Pseudocode
```text
FUNCTION insert_line(line_num, text):
    IF line_num < 1 OR line_num > count + 1 THEN THROW IndexError
    node = ALLOCATE TextLineNode(text)
    IF head == None THEN:
        head = tail = node
    ELSE IF line_num == 1 THEN:
        node.next = head; head.prev = node; head = node
    ELSE IF line_num == count + 1 THEN:
        tail.next = node; node.prev = tail; tail = node
    ELSE:
        target = GET_NODE(line_num)
        node.next = target; node.prev = target.prev
        target.prev.next = node; target.prev = node
    count = count + 1
    cursor = node; cursor_line = line_num
END FUNCTION
```

### Dry Run
1. Start with lines: `1: "First"`, `2: "Third"`. Cursor at line 2.
2. `insert_line(2, "Second")`:
   - Target is line 2 (`"Third"`).
   - Splice `"Second"` between `"First"` and `"Third"`.
   - Result: `1: "First"`, `2: "Second"`, `3: "Third"`.
   - Active cursor set to Line 2 (`"Second"`).
3. `move_cursor_next()`: Cursor moves to Line 3 (`"Third"`).
4. `move_cursor_next()`: At tail, returns `False`.

### Complexity Analysis
- **Cursor Up / Down Movement**: $O(1)$ time, $O(1)$ space.
- **Insert / Delete at Active Cursor**: $O(1)$ time, $O(1)$ space.
- **Insert / Delete at Arbitrary Line $k$**: $O(n)$ traversal, $O(1)$ relinking.
- **Display Buffer**: $O(n)$ time.

### Real-Life Applications
- Core line buffer architecture of text editors (e.g., Emacs buffer chains, Vim line structures).
- Subtitle synchronization and editing software.

---

## 10. Experiment 6: Playlist Manager

### Problem Statement
Develop an interactive Audio Playlist Manager in [playlist_manager.py](file:///home/jeet/Desktop/Data_structures/Lab03-Linked-Lists/Program06-PlaylistManager/playlist_manager.py) using a Circular Doubly Linked List (CDLL). The system must support track additions, track removal by title, circular forward navigation (`next_song`), circular backward navigation (`prev_song`), active track playback simulation, and song search.

### Architectural Design Decision: Why Circular Doubly Linked List?
In an audio playback application, users demand instantaneous responsiveness when clicking "Next Track" or "Previous Track". 
- In a **Singly Circular Linked List**, moving to the previous song requires an $O(n)$ traversal through the entire ring until reaching the node whose `next` references the active track. For large playlists, this induces noticeable latency.
- In a **Circular Doubly Linked List**, each [`SongNode`](file:///home/jeet/Desktop/Data_structures/Lab03-Linked-Lists/Program06-PlaylistManager/playlist_manager.py#L29) possesses both `prev` and `next` pointers forming two opposing circular rings. Thus, `next_song()` and `prev_song()` execute deterministically in **$O(1)$ constant time**, while wrapping around seamlessly at playlist boundaries.

```
       +-------------------------------------------------------------+
       |                                                             |
       v                                                             |
  +---------+  prev   +---------+  prev   +---------+  prev   +---------+
  | Song A  | <=====> | Song B  | <=====> | Song C  | <=====> | Song D  |
  +---------+  next   +---------+  next   +---------+  next   +---------+
       |                                                             ^
       +-------------------------------------------------------------+
```

### Algorithm

#### 1. Track Addition (`add_song`):
1. Clean inputs and allocate `new_song = SongNode(title, artist)`.
2. If `current_song is None`:
   - `new_song.next = new_song.prev = new_song`.
   - `current_song = new_song`.
3. Else:
   - Let `head = current_song`, `tail = current_song.prev`.
   - `tail.next = new_song; new_song.prev = tail`.
   - `new_song.next = head; head.prev = new_song`.
4. Increment `_size` by 1.

#### 2. Track Removal (`remove_song`):
1. If empty, return `False`.
2. Search circular ring for matching title. If not found, return `False`.
3. If `_size == 1`: set `current_song = None`.
4. Else:
   - `found.prev.next = found.next`.
   - `found.next.prev = found.prev`.
   - If `current_song == found`: advance `current_song = found.next`.
5. Decrement `_size` by 1. Return `True`.

### Pseudocode
```text
FUNCTION add_song(title, artist):
    node = ALLOCATE SongNode(title, artist)
    IF current_song == None THEN:
        node.next = node; node.prev = node
        current_song = node
    ELSE:
        head = current_song
        tail = current_song.prev
        tail.next = node; node.prev = tail
        node.next = head; head.prev = node
    size = size + 1
END FUNCTION

FUNCTION prev_song():
    IF current_song == None THEN RETURN None
    current_song = current_song.prev
    RETURN (current_song.title, current_song.artist)
END FUNCTION
```

### Dry Run
Playlist: `[Song 1] <=> [Song 2] <=> [Song 3] (circular)`. Active: `Song 1`.
- `next_song()`: Advances to `Song 2` in $O(1)$ time.
- `next_song()`: Advances to `Song 3` in $O(1)$ time.
- `next_song()`: Advances past boundary back to `Song 1` in $O(1)$ time.
- `prev_song()`: Follows `prev` pointer back to `Song 3` in $O(1)$ time.
- `remove_song("Song 3")`: Relinks `Song 2` directly to `Song 1`. Active track shifts to `Song 1`.

### Complexity Analysis
- **Next / Previous Track**: Strictly $O(1)$ time, $O(1)$ space.
- **Add Song**: $O(1)$ time, $O(1)$ space.
- **Remove Song by Title**: $O(n)$ search, $O(1)$ unlinking.
- **Play Active Track**: $O(1)$ time.

### Real-Life Applications
- Media players (Spotify, VLC, Apple Music) for continuous playlist looping and track skipping.
- Automotive infotainment cluster audio controllers.

---

## 11. Comparison of Linked-List Types

| Feature | Singly Linked List | Doubly Linked List | Circular Linked List (Singly) | Circular Doubly Linked List |
| :--- | :--- | :--- | :--- | :--- |
| **Pointers per Node** | 1 (`next`) | 2 (`prev`, `next`) | 1 (`next`) | 2 (`prev`, `next`) |
| **Traversal Direction** | Forward only | Bidirectional | Forward only (circular) | Bidirectional (circular) |
| **Terminal Pointer** | Points to `None` | `head.prev=None`, `tail.next=None` | Points back to `head` | `tail.next=head`, `head.prev=tail` |
| **End Operations (with Tail)**| Insert: $O(1)$, Delete: $O(n)$ | Insert: $O(1)$, Delete: $O(1)$ | Insert: $O(1)$, Delete: $O(n)$ | Insert: $O(1)$, Delete: $O(1)$ |
| **Preceding Node Access** | $O(n)$ traversal from head | $O(1)$ via `node.prev` | $O(n)$ traversal around cycle | $O(1)$ via `node.prev` |
| **Memory Overhead** | 1 reference per node | 2 references per node | 1 reference per node | 2 references per node |
| **Infinite Loop Risk** | Zero (guaranteed `None`) | Zero (guaranteed `None`) | High if cycle condition fails | High if cycle condition fails |
| **Best Suited For** | Simple stacks/queues, low RAM | Editors, LRU caches, history | Round-robin schedulers | Audio players, carousels |

---

## 12. Time and Space Complexity Analysis

### Operation Complexity Matrix

| Operation | Singly Linked List | Doubly Linked List (with Tail) | Circular Singly Linked List | Circular Doubly Linked List |
| :--- | :---: | :---: | :---: | :---: |
| **Insert at Beginning** | $O(1)$ | $O(1)$ | $O(1)$ with tail / $O(n)$ | $O(1)$ |
| **Insert at End** | $O(n)$ / $O(1)$ with tail | $O(1)$ | $O(1)$ with tail / $O(n)$ | $O(1)$ |
| **Insert at Position $k$**| $O(n)$ | $O(n/2) = O(n)$ | $O(n)$ | $O(n/2) = O(n)$ |
| **Delete at Beginning** | $O(1)$ | $O(1)$ | $O(1)$ with tail / $O(n)$ | $O(1)$ |
| **Delete at End** | $O(n)$ | $O(1)$ | $O(n)$ | $O(1)$ |
| **Delete at Position $k$**| $O(n)$ | $O(n/2) = O(n)$ | $O(n)$ | $O(n/2) = O(n)$ |
| **Search by Value** | $O(n)$ | $O(n)$ | $O(n)$ | $O(n)$ |
| **In-Place Reversal** | $O(n)$ | $O(n)$ | $O(n)$ | $O(n)$ |
| **Concatenation** | $O(n + m)$ | $O(m)$ | $O(m)$ | $O(m)$ |
| **Auxiliary Space** | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ |

---

## 13. Testing and Sample I/O

Every program was executed and verified against normal, boundary, and error cases.

### Experiment 1: Singly Linked List
```text
$ python3 Lab03-Linked-Lists/Program01-SinglyLinkedList/singly_linked_list.py
=================================================================
RUNNING COMPREHENSIVE TESTS: Singly Linked List (Program 01)
=================================================================
  [Test 01 Passed] Initialized empty list successfully.
  [Test 02 Passed] Caught delete_beginning on empty list.
  [Test 03 Passed] Caught delete_end on empty list.
  [Test 04 Passed] Caught delete_at_position on empty list.
  [Test 05 Passed] Insertions (beginning, middle, end) verified.
  [Test 06 Passed] Caught negative position insertion.
  [Test 07 Passed] Caught out-of-range position insertion.
  [Test 08 Passed] Search for present and missing values verified.
  [Test 09 Passed] Deletions (beginning, middle, end) verified.
  [Test 10 Passed] In-place reversal verified.
  [Test 11 Passed] Single-node list reversal verified.
  [Test 12 Passed] List concatenation verified.

All Program 01 automated tests PASSED successfully!

=================================================================
DEMONSTRATION: Singly Linked List (Program 01)
=================================================================
1. Created an empty Singly Linked List.
   Current List: Empty List

2. Inserting elements:
   insert_beginning(20) : 20 -> None
   insert_beginning(10) : 10 -> 20 -> None
   insert_end(40)       : 10 -> 20 -> 40 -> None
   insert_at_position(30, pos=2): 10 -> 20 -> 30 -> 40 -> None

3. Searching in the list:
   search(30) -> Found at zero-based index 2
   search(99) -> Not Found (returned -1)

4. Deleting elements:
   delete_beginning() -> Removed 10 : 20 -> 30 -> 40 -> None
   delete_end()       -> Removed 40 : 20 -> 30 -> None
   delete_at_position(0) -> Removed 20 : 30 -> None

5. Reversal:
   Before reversal: 30 -> 50 -> 60 -> 70 -> None
   After reversal : 70 -> 60 -> 50 -> 30 -> None

6. Concatenation:
   List A: 70 -> 60 -> 50 -> 30 -> None
   List B: 80 -> 90 -> None
   Concatenated List A: 70 -> 60 -> 50 -> 30 -> 80 -> 90 -> None
```

### Experiment 2: Doubly Linked List
```text
$ python3 Lab03-Linked-Lists/Program02-DoublyLinkedList/doubly_linked_list.py
=================================================================
RUNNING COMPREHENSIVE TESTS: Doubly Linked List (Program 02)
=================================================================
  [Test 01 Passed] Initialized empty doubly linked list.
  [Test 02 Passed] Caught delete_beginning on empty list.
  [Test 03 Passed] Caught delete_end on empty list.
  [Test 04 Passed] Single node insertion and pointer symmetry verified.
  [Test 05 Passed] Single node deletion leaving empty list verified.
  [Test 06 Passed] Insertions and bidirectional traversals verified.
  [Test 07 Passed] Search for present and absent keys verified.
  [Test 08 Passed] Deletions with bidirectional pointer checks verified.
  [Test 09 Passed] In-place reversal and pointer integrity verified.
  [Test 10 Passed] Concatenation with backward pointer integrity verified.

All Program 02 automated tests PASSED successfully!

=================================================================
DEMONSTRATION: Doubly Linked List (Program 02)
=================================================================
1. Inserting into Doubly Linked List:
   Forward  : None <- 10 <=> 20 <=> 30 <=> 40 -> None
   Backward : None <- 40 <=> 30 <=> 20 <=> 10 -> None

2. Searching elements:
   search(30) -> Found at index 2
   search(99) -> Not Found

3. Deleting elements:
   delete_beginning() -> Removed 10
   delete_end()       -> Removed 40
   Current List: None <- 20 <=> 30 -> None

4. In-Place Reversal:
   Before Reversal : None <- 20 <=> 30 <=> 50 <=> 60 -> None
   After Reversal  : None <- 60 <=> 50 <=> 30 <=> 20 -> None
   Reversed Backw. : None <- 20 <=> 30 <=> 50 <=> 60 -> None
```

### Experiment 3: Circular Linked List
```text
$ python3 Lab03-Linked-Lists/Program03-CircularLinkedList/circular_linked_list.py
=================================================================
RUNNING COMPREHENSIVE TESTS: Circular Linked List (Program 03)
=================================================================
  [Test 01 Passed] Initialized empty circular linked list.
  [Test 02 Passed] Caught delete_beginning on empty list.
  [Test 03 Passed] Caught delete_end on empty list.
  [Test 04 Passed] Single node insertion and self-referential cycle verified.
  [Test 05 Passed] Single node deletion leaving empty list verified.
  [Test 06 Passed] Single node delete_end verified.
  [Test 07 Passed] Insertions (beginning, middle, end) verified.
  [Test 08 Passed] Circular cycle closure verified (no infinite loop).
  [Test 09 Passed] Search for present and missing values verified.
  [Test 10 Passed] Deletions with cycle restoration verified.
  [Test 11 Passed] In-place circular reversal verified.
  [Test 12 Passed] Circular list concatenation verified.

All Program 03 automated tests PASSED successfully!

=================================================================
DEMONSTRATION: Circular Linked List (Program 03)
=================================================================
1. Inserting into Circular Linked List:
   List State: 10 -> 20 -> 30 -> 40 -> (circular back to 10)

2. Searching elements in circular ring:
   search(30) -> Found at index 2
   search(88) -> Not Found

3. Deleting elements from circular ring:
   delete_beginning() -> Removed 10
   delete_end()       -> Removed 40
   Current List: 20 -> 30 -> (circular back to 20)

4. In-Place Circular Reversal:
   Before Reversal : 20 -> 30 -> 50 -> 60 -> (circular back to 20)
   After Reversal  : 60 -> 50 -> 30 -> 20 -> (circular back to 60)
```

### Experiment 4: Polynomial Operations
```text
$ python3 Lab03-Linked-Lists/Program04-PolynomialOperations/polynomial_operations.py
=================================================================
RUNNING COMPREHENSIVE TESTS: Polynomial Operations (Program 04)
=================================================================
  [Test 01 Passed] Zero polynomial representation verified.
  [Test 02 Passed] Term insertion and descending exponent ordering verified.
  [Test 03 Passed] Like-exponent term combination verified.
  [Test 04 Passed] Automatic cancellation of zero coefficients verified.
  [Test 05 Passed] Polynomial addition with matching exponents verified.
  [Test 06 Passed] Polynomial addition with interleaved exponents verified.
  [Test 07 Passed] Complete cancellation to zero polynomial verified.
  [Test 08 Passed] Identity addition with zero polynomial verified.
  [Test 09 Passed] Polynomial evaluation verified.

All Program 04 automated tests PASSED successfully!

=================================================================
DEMONSTRATION: Polynomial Representation & Addition (Program 04)
=================================================================

--- Example 1: Matching Exponents ---
  P1(x) = 3x^2 + 5x + 2
  P2(x) = 4x^2 - 2x + 6
  P1(x) + P2(x) = 7x^2 + 3x + 8

--- Example 2: Interleaved Non-Matching Exponents ---
  P3(x) = 5x^4 + 2x^2 + 1
  P4(x) = 3x^3 + 4x
  P3(x) + P4(x) = 5x^4 + 3x^3 + 2x^2 + 4x + 1

--- Example 3: Full Cancellation to Zero ---
  P5(x) = 4x^3 + 2x - 7
  P6(x) = -4x^3 - 2x + 7
  P5(x) + P6(x) = 0 (is_zero: True)

--- Example 4: Evaluation at x = 3 ---
  Evaluating sum1 at x = 3: 7x^2 + 3x + 8 -> 80
```

### Experiment 5: Text Editor Buffer
```text
$ python3 Lab03-Linked-Lists/Program05-TextEditorBuffer/text_editor_buffer.py --test
=================================================================
RUNNING COMPREHENSIVE TESTS: Text Editor Buffer (Program 05)
=================================================================
  [Test 01 Passed] Initialized empty buffer verified.
  [Test 02 Passed] Caught delete on empty buffer.
  [Test 03 Passed] Line insertions (beginning, middle, end) verified.
  [Test 04 Passed] Bidirectional cursor navigation and bounds verified.
  [Test 05 Passed] Line editing and cursor relocation verified.
  [Test 06 Passed] Deletions at boundaries and single-line reduction verified.

All Program 05 automated tests PASSED successfully!
```

### Experiment 6: Playlist Manager
```text
$ python3 Lab03-Linked-Lists/Program06-PlaylistManager/playlist_manager.py --test
=================================================================
RUNNING COMPREHENSIVE TESTS: Playlist Manager (Program 06)
=================================================================
  [Test 01 Passed] Initialized empty playlist verified.
  [Test 02 Passed] Single-song continuous loop playback verified.
  [Test 03 Passed] Added multiple songs successfully.
  [Test 04 Passed] Forward and backward circular navigation verified.
  [Test 05 Passed] Song search (present and absent) verified.
  [Test 06 Passed] Song removal and active track auto-advancement verified.

All Program 06 automated tests PASSED successfully!
```

---

## 14. Real-Life Applications

1. **Memory Allocators (Dynamic Heaps)**:
   - Operating systems (Linux kernel glibc `malloc`) manage free blocks via circular doubly linked lists (free-lists). When allocating or freeing, coalescing adjacent blocks occurs in $O(1)$ time.
2. **CPU Multitasking & Schedulers**:
   - Round-robin CPU time-slicing uses circular linked lists where processes cycle through execution time slices indefinitely.
3. **Web Browsers**:
   - Backward and forward tab browsing stacks use doubly linked lists.
4. **Symbolic Mathematics & Scientific Computing**:
   - Sparse algebraic polynomial representations avoid allocating large zero-padded arrays for high-degree equations like $x^{1000} + 1$.
5. **Interactive Document & Code Editors**:
   - Modern editor gap buffers and line data structures use doubly linked lists to avoid moving megabytes of text data when users press `Enter` or `Backspace`.
6. **Streaming Media Applications**:
   - Media playlist engines (Spotify, VLC) use circular doubly linked lists to support infinite looping and rapid $O(1)$ track skipping.

---

## 15. Folder Structure

```text
Lab03-Linked-Lists/
├── Program01-SinglyLinkedList/
│   └── singly_linked_list.py
├── Program02-DoublyLinkedList/
│   └── doubly_linked_list.py
├── Program03-CircularLinkedList/
│   └── circular_linked_list.py
├── Program04-PolynomialOperations/
│   └── polynomial_operations.py
├── Program05-TextEditorBuffer/
│   └── text_editor_buffer.py
├── Program06-PlaylistManager/
│   └── playlist_manager.py
├── README.md
└── reflection.md
```

---

## 16. Execution Instructions

All programs run independently using pure Python 3:

```bash
# 1. Singly Linked List (Program 01)
python3 Lab03-Linked-Lists/Program01-SinglyLinkedList/singly_linked_list.py

# 2. Doubly Linked List (Program 02)
python3 Lab03-Linked-Lists/Program02-DoublyLinkedList/doubly_linked_list.py

# 3. Circular Linked List (Program 03)
python3 Lab03-Linked-Lists/Program03-CircularLinkedList/circular_linked_list.py

# 4. Polynomial Representation and Addition (Program 04)
python3 Lab03-Linked-Lists/Program04-PolynomialOperations/polynomial_operations.py

# 5. Text Editor Buffer (Program 05)
# Run Automated Self-Tests:
python3 Lab03-Linked-Lists/Program05-TextEditorBuffer/text_editor_buffer.py --test
# Run Interactive Console Menu:
python3 Lab03-Linked-Lists/Program05-TextEditorBuffer/text_editor_buffer.py

# 6. Playlist Manager (Program 06)
# Run Automated Self-Tests:
python3 Lab03-Linked-Lists/Program06-PlaylistManager/playlist_manager.py --test
# Run Interactive Console Menu:
python3 Lab03-Linked-Lists/Program06-PlaylistManager/playlist_manager.py
```

---

## 17. Learning Outcomes

1. **Mastery of Pointer Manipulation**: Developed concrete mental models for updating reference pointers, avoiding orphaned node memory leaks, and managing bidirectional reference symmetry.
2. **In-Place Reversal Techniques**: Mastered three-pointer tracking (`prev`, `curr`, `next`) for linear and circular in-place list reversal without allocating secondary storage.
3. **Cycle Safety**: Implemented robust cycle termination conditions in Circular Singly and Circular Doubly Linked Lists to prevent infinite loops during traversal, deletion, and concatenation.
4. **Algorithmic Divide-and-Conquer Merge**: Designed a two-pointer merge algorithm for polynomial addition running in optimal $O(n + m)$ time.
5. **Real-World System Design**: Engineered real-world interactive systems (Text Editor Buffer and Circular Playlist Manager), appreciating why doubly linked representations are selected for localized editing and navigation tasks over flat array buffers.

---

## 18. References

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. *Introduction to Algorithms* (3rd ed.). MIT Press, 2009. Chapter 10: Elementary Data Structures.
2. Sedgewick, R., & Wayne, K. *Algorithms* (4th ed.). Addison-Wesley Professional, 2011. Section 1.3: Bags, Queues, and Stacks.
3. Knuth, D. E. *The Art of Computer Programming, Volume 1: Fundamental Algorithms* (3rd ed.). Addison-Wesley, 1997. Section 2.2: Linked Allocation.
4. Python Software Foundation. *Python 3 Standard Library Documentation: Data Model and Object Identity*. https://docs.python.org/3/reference/datamodel.html

