# IC-307D: Data Structures and Algorithms Lab
## Unit 5: Queues (CO1)

---

## 1. Introduction to Queues and FIFO

A **Queue** is a fundamental linear abstract data type (ADT) characterized by the **First-In, First-Out (FIFO)** operational discipline. In a standard queue, elements are admitted at one designated terminal called the **rear** (or *tail*) and extracted from the opposing terminal called the **front** (or *head*).

```
          +-----------------------------------------------+
Enqueue ->| Element 3 | Element 2 | Element 1 | Element 0 | -> Dequeue
 (Rear)   +-----------------------------------------------+    (Front)
```

### The FIFO Principle
The entity residing in the queue for the longest duration is consistently the first candidate selected for processing and eviction. This mirrors physical service lines such as supermarket billing counters, ticket reservation booths, toll collection plazas, and print queues.

### Core Queue Operations
1. **`enqueue(x)`**: Inserts element `x` at the rear of the queue.
2. **`dequeue()`**: Removes and returns the element situated at the front of the queue.
3. **`peek()` / `front()`**: Inspects the element at the front without mutating the collection.
4. **`is_empty()`**: Evaluates whether the queue contains zero elements.
5. **`is_full()`**: Evaluates whether the queue has exhausted its maximum capacity (applicable to static and circular queues).
6. **`size()`**: Returns the count of elements currently resident in the queue.

### Boundary Conditions
- **Queue Overflow**: Occurs when attempting an `enqueue` onto a queue that has saturated its fixed capacity.
- **Queue Underflow**: Occurs when attempting a `dequeue` or `peek` on a queue containing zero elements.
- **False Overflow (Linear Array Limitation)**: In a naive static linear queue, as elements are enqueued and dequeued, the `front` and `rear` pointers advance forward. Once `rear` hits `capacity - 1`, subsequent enqueues trigger an overflow condition, even if previous `dequeue` operations have vacated slots at the front of the array. This critical drawback directly motivates the design of **Circular Queues**.

---

## 2. Aim

To study, design, implement from first principles, empirically verify, and document linear, circular, double-ended, and priority-driven queue data structures in Python 3; to evaluate array versus heap-backed priority mechanisms; and to engineer practical queue-driven applications including a dual-tier Customer Service ticketing engine and a preemptive Round Robin CPU process scheduling simulator.

---

## 3. Learning Objectives

- Master the theoretical mechanics and invariant rules governing **First-In, First-Out (FIFO)** pipelines.
- Understand the architectural differences between contiguous memory buffers (**Static Queue**) and dynamically linked nodes (**Dynamic Queue**).
- Overcome the false overflow limitation of linear arrays using modulo arithmetic in **Circular Queues**.
- Generalize double-ended data access patterns using a **Circular Array Deque**.
- Implement **Priority Queues** using both sorted arrays and binary min-heaps, analyzing the asymptotic tradeoffs between $O(n)$ and $O(\log n)$ performance.
- Guarantee strict **FIFO stability** across equal-priority items using monotonic sequence numbering.
- Simulate discrete-event queuing models: dual-tier customer prioritization and multi-process Round Robin scheduling.
- Compute fundamental operating system metrics: Arrival Time ($AT$), Burst Time ($BT$), Completion Time ($CT$), Turnaround Time ($TAT$), and Waiting Time ($WT$).

---

## 4. Software Requirements

- **Operating System**: Linux (Ubuntu 22.04 LTS / Debian 12 / POSIX-compliant) or Windows 10/11 / macOS.
- **Programming Language**: Python 3.8+ (Tested on Python 3.10 / 3.11).
- **External Dependencies**: None. Standard library built-ins only (no `queue.Queue`, `collections.deque`, or `heapq` for core data structure mechanics).
- **Terminal Shell**: Bash / Zsh / PowerShell.

---

## 5. Experiment 1: Static Queue

### Problem Statement
Implement a fixed-capacity linear queue using a contiguous Python list. Provide standard queue operations (`enqueue`, `dequeue`, `peek`, `display`, `is_empty`, `is_full`), handle overflow and underflow conditions, and demonstrate the architectural limitation of false overflow.

### Approach
A preallocated list of size `capacity` holds the queue items. Two pointer variables, `front` and `rear`, track the boundaries:
- `front`: Index of the oldest resident element (initialized to `-1`).
- `rear`: Index of the most recently inserted element (initialized to `-1`).
- `enqueue`: Increments `rear` and stores the element at `data[rear]`. If `front == -1`, set `front = 0`.
- `dequeue`: Retrieves `data[front]` and increments `front`. When `front > rear`, the queue becomes empty and both pointers reset to `-1`.
- **False Overflow Demonstration**: Once `rear == capacity - 1`, no further items can be enqueued, even if items have been dequeued from the front.

### Complexity
- **Time Complexity**:
  - `enqueue`: $O(1)$
  - `dequeue`: $O(1)$
  - `peek`: $O(1)$
  - `is_empty` / `is_full` / `size`: $O(1)$
  - `display`: $O(n)$
- **Auxiliary Space**: $O(1)$ auxiliary memory; $O(\text{capacity})$ total preallocated memory.

### Real-Life Applications
- Hardware input buffers with strict memory bounds (e.g., keyboard keystroke UART buffers).
- Fixed-size batch processing in embedded systems where dynamic heap allocation is prohibited.

---

## 6. Experiment 2: Dynamic Queue

### Problem Statement
Implement an unbounded dynamic queue using a custom singly-linked list. Implement a `QueueNode` class and a `DynamicQueue` class with `front` and `rear` pointers. Do not use Python lists for queue storage. Handle pointer updates correctly when the queue empties.

### Approach
Each queue entry is encapsulated within a `QueueNode` containing `data` and a `next` pointer.
- `front` references the node to be dequeued next.
- `rear` references the latest enqueued node.
- `enqueue`: Allocates a new node. If `is_empty()`, both `front` and `rear` point to the new node. Otherwise, `rear.next = new_node` and `rear = new_node`.
- `dequeue`: Advances `front = front.next`. If `front` becomes `None`, `rear` is also explicitly set to `None`, ensuring no dangling references remain.
- Memory scales organically on the heap; no overflow occurs unless system memory is exhausted.

### Complexity
- **Time Complexity**:
  - `enqueue`: $O(1)$
  - `dequeue`: $O(1)$
  - `peek`: $O(1)$
  - `is_empty` / `size`: $O(1)$
  - `display`: $O(n)$
- **Auxiliary Space**: $O(1)$ auxiliary space per operation; $O(n)$ heap space for $n$ nodes ($n \times (\text{data} + \text{pointer})$).

### Real-Life Applications
- Asynchronous task message brokers (RabbitMQ, Kafka consumer queues) where burst traffic requires unbounded dynamic buffer growth.
- Web server request queues managing incoming HTTP connections before worker thread dispatch.

---

## 7. Experiment 3: Circular Queue

### Problem Statement
Implement a fixed-capacity circular queue using a Python list. Eliminate the false overflow limitation of linear arrays by employing modular arithmetic to wrap pointers from the physical end of the array back to index `0`.

### Approach
A preallocated list of length `capacity` is managed using modular arithmetic:
$$\text{rear} = (\text{rear} + 1) \pmod{\text{capacity}}$$
$$\text{front} = (\text{front} + 1) \pmod{\text{capacity}}$$
- To distinguish between an **empty queue** and a **full queue** without sacrificing a buffer slot, an explicit counter variable `_count` is maintained.
- `is_empty()` returns `_count == 0`.
- `is_full()` returns `_count == capacity`.
- Front slots vacated by `dequeue` are reused seamlessly by subsequent `enqueue` operations.

```
       Index:   0     1     2     3     4
              +-----+-----+-----+-----+-----+
  Array:      | 50  |     |     | 30  | 40  |
              +-----+-----+-----+-----+-----+
                ^                 ^
                |                 |
              rear = 0          front = 3
  Wraparound: items wrap around the physical array boundary!
```

### Complexity
- **Time Complexity**:
  - `enqueue`: $O(1)$
  - `dequeue`: $O(1)$
  - `peek`: $O(1)$
  - `is_empty` / `is_full` / `size`: $O(1)$
  - `display`: $O(n)$
- **Auxiliary Space**: $O(1)$ auxiliary memory; $O(\text{capacity})$ total contiguous buffer.

### Real-Life Applications
- Operating system ring buffers for streaming audio, video playback, and network packet capture (e.g., Linux ring buffer `SO_RCVBUF`).
- Round-robin resource allocation in real-time embedded controllers.

---

## 8. Experiment 4: Deque (Double-Ended Queue)

### Problem Statement
Implement a double-ended queue (Deque) using a fixed-capacity circular array. Support insertion and deletion at both ends (`insert_front`, `insert_rear`, `delete_front`, `delete_rear`, `peek_front`, `peek_rear`).

### Approach
The circular array allows pointer movement in both clockwise (forward) and counter-clockwise (backward) directions:
- `insert_rear`: $\text{rear} = (\text{rear} + 1) \pmod{\text{capacity}}$
- `delete_front`: $\text{front} = (\text{front} + 1) \pmod{\text{capacity}}$
- `insert_front`: $\text{front} = (\text{front} - 1 + \text{capacity}) \pmod{\text{capacity}}$
- `delete_rear`: $\text{rear} = (\text{rear} - 1 + \text{capacity}) \pmod{\text{capacity}}$
- A Deque seamlessly subsumes both a FIFO Queue and a LIFO Stack:
  - Queue behavior: `insert_rear()` + `delete_front()`
  - Stack behavior: `insert_front()` + `delete_front()` OR `insert_rear()` + `delete_rear()`

### Complexity
- **Time Complexity**:
  - `insert_front` / `insert_rear`: $O(1)$
  - `delete_front` / `delete_rear`: $O(1)$
  - `peek_front` / `peek_rear`: $O(1)$
  - `is_empty` / `is_full`: $O(1)$
- **Auxiliary Space**: $O(1)$ auxiliary; $O(\text{capacity})$ total preallocated storage.

### Real-Life Applications
- Undo/Redo history buffers with bounded memory capacity (e.g., Photoshop or IDE command history).
- Sliding window maximum/minimum algorithms in algorithmic trading and digital signal processing.
- A-Steal work-stealing scheduling algorithms used by thread pools (e.g., Java ForkJoinPool, Go runtime).

---

## 9. Experiment 5: Array-Based Priority Queue

### Problem Statement
Implement a priority queue using an array. Follow the convention where a **lower numeric value indicates higher priority** (e.g., Priority 1 > Priority 5). Maintain strict FIFO stability for entries sharing identical priorities.

### Approach
Each element is stored as a `PriorityQueueItem(data, priority, arrival_order)`.
- A monotonic counter increments with every insertion, assigning a unique arrival timestamp.
- Insertion performs a linear scan to place the new item in ascending order:
  $$\text{Item}_A < \text{Item}_B \iff (\text{pri}_A < \text{pri}_B) \lor (\text{pri}_A == \text{pri}_B \land \text{seq}_A < \text{seq}_B)$$
- Index `0` always holds the highest-priority element, providing $O(1)$ peek access.
- Dequeue extracts index `0` and shifts subsequent elements.

### Complexity
- **Time Complexity**:
  - `insert`: $O(n)$ time due to linear search and list shift.
  - `remove_highest_priority`: $O(n)$ due to `pop(0)` shifting in a Python list (or $O(1)$ if sorted in reverse order).
  - `peek`: $O(1)$ time.
  - `is_empty` / `size`: $O(1)$.
- **Auxiliary Space**: $O(1)$ auxiliary; $O(n)$ to store $n$ items.

### Real-Life Applications
- Hospital triage management systems (Critical/Trauma patients served ahead of non-urgent consultations).
- Priority print spoolers where executive/confidential print jobs preempt regular batch printing.

---

## 10. Experiment 6: Heap-Based Priority Queue

### Problem Statement
Implement a priority queue using a custom binary min-heap without utilizing external libraries (`heapq`). Lower numeric value represents higher priority. Guarantee strict FIFO stability for equal priorities.

### Approach
A binary min-heap is mapped onto a contiguous list without explicit node pointers:
- Root is at index `0`.
- For any node at index $i$:
  - Parent: $\lfloor (i - 1) / 2 \rfloor$
  - Left Child: $2i + 1$
  - Right Child: $2i + 2$
- **Min-Heap Property**: Every parent's key is less than or equal to its children's keys.
- **Key Definition**: Each node stores a composite key `(priority, arrival_counter)`. Because tuples compare lexicographically in Python, equal priorities are tie-broken strictly by arrival order.
- **`insert(data, priority)`**: Appends to array end and invokes `_heapify_up(last_idx)`, comparing with parent and swapping until heap invariant holds ($O(\log n)$).
- **`remove_highest_priority()`**: Swaps root with last element, pops the minimum, and invokes `_heapify_down(0)`, sifting downward through smaller children ($O(\log n)$).

```
                      [Pri:1, Seq:1]
                     /              \
         [Pri:2, Seq:3]            [Pri:1, Seq:2]
          /          \
    [Pri:5, Seq:4]  [Pri:3, Seq:5]
```

### Complexity
- **Time Complexity**:
  - `insert`: $O(\log n)$
  - `remove_highest_priority`: $O(\log n)$
  - `peek`: $O(1)$
  - `is_empty` / `size`: $O(1)$
  - `display`: $O(n)$
- **Auxiliary Space**: $O(1)$ auxiliary; $O(n)$ heap storage.

### Real-Life Applications
- Dijkstra's Shortest Path algorithm and Prim's Minimum Spanning Tree algorithm.
- Event-driven discrete simulation engines (handling scheduled event timestamps).

---

## 11. Experiment 7: Customer Service Queue Simulation

### Problem Statement
Simulate a customer service center handling dual service tiers (VIP Priority vs Regular) using custom queue data structures. Provide ticket generation, queue inspection, customer servicing, and service metrics reporting.

### Approach
- Built upon the custom dynamic singly-linked `CustomerQueue`.
- Entities:
  - `Customer(ticket_id, name, service_type, is_vip, arrival_step)`
  - Formatted ticket numbering: `VIP-101`, `REG-201`.
- Dual Queue Architecture:
  - `vip_queue`: High-priority service line.
  - `regular_queue`: Standard FIFO line.
- Service Dispatch Policy:
  - Whenever a service desk becomes available, the system checks `vip_queue` first.
  - If `vip_queue` has waiting customers, the next VIP is dequeued and served immediately.
  - Only when `vip_queue` is empty are customers dequeued from `regular_queue`.
  - Maintains a historical audit log capturing service completion timestamps and customer wait times.

### Complexity
- **Time Complexity**:
  - Register Customer: $O(1)$
  - Serve Customer: $O(1)$
  - Peek Next: $O(1)$
  - Display Dashboard: $O(n)$ where $n = n_{\text{vip}} + n_{\text{reg}}$
- **Auxiliary Space**: $O(n)$ where $n$ is total customers currently waiting or logged.

### Real-Life Applications
- Banking teller hall operations with dedicated High Net Worth / Premier counters.
- Airline airport check-in counters (First/Business Class vs Economy queues).

---

## 12. Experiment 8: Round Robin Process Scheduling

### Problem Statement
Simulate the CPU Round Robin (RR) preemptive scheduling algorithm using a custom FIFO ready queue. Accurately handle variable arrival times, time quantum preemption, process completion, and CPU idle intervals. Calculate and output detailed scheduling metrics.

### Key Scheduling Terminology
1. **Arrival Time ($AT$)**: The wall-clock time at which a process enters the system ready state.
2. **Burst Time ($BT$)**: Total CPU execution time required by the process to complete.
3. **Time Quantum ($TQ$)**: The maximum continuous time slice allocated to a process per dispatch.
4. **Completion Time ($CT$)**: The exact clock time when a process finishes all required burst execution.
5. **Turnaround Time ($TAT$)**: Total elapsed time from arrival to completion:
   $$TAT = CT - AT$$
6. **Waiting Time ($WT$)**: Total duration spent waiting inside the ready queue:
   $$WT = TAT - BT$$
7. **Average Turnaround Time ($Avg TAT$)**: $\frac{1}{n} \sum_{i=1}^n TAT_i$
8. **Average Waiting Time ($Avg WT$)**: $\frac{1}{n} \sum_{i=1}^n WT_i$

### Scheduling Algorithm Mechanics
1. Sort all incoming processes by $(AT, \text{PID})$.
2. Initialize `current_time = 0` and an empty FIFO `ready_queue`.
3. If earliest arrival $> \text{current\_time}$, log an `[IDLE]` block and advance `current_time` to arrival.
4. Enqueue all processes with $AT \le \text{current\_time}$.
5. While ready queue is not empty or unarrived processes remain:
   - Dequeue front process $P$.
   - Compute execution duration: $\text{exec\_time} = \min(TQ, P.\text{remaining\_time})$.
   - Advance `current_time += exec_time` and record execution segment in Gantt timeline.
   - Update $P.\text{remaining\_time} -= \text{exec\_time}$.
   - **Crucial Order of Enqueue**: Scan for newly arrived processes ($AT \le \text{current\_time}$) and enqueue them into `ready_queue` **before** re-enqueuing the preempted process $P$.
   - If $P.\text{remaining\_time} == 0$: process terminates; record $CT, TAT, WT$.
   - Else: re-enqueue $P$ to the rear of `ready_queue`.
   - If `ready_queue` is empty and unarrived processes exist, log CPU `[IDLE]` time and fast-forward `current_time`.

### Actual Benchmark Calculations from Program Execution
Consider the textbook four-process workload with $TQ = 2$:
- $P_1$: $AT = 0, BT = 5$
- $P_2$: $AT = 1, BT = 3$
- $P_3$: $AT = 2, BT = 1$
- $P_4$: $AT = 3, BT = 2$

#### Step-by-Step Execution Trace:
1. **$t = 0$**: $P_1$ arrives and enters Ready Queue: `[P1]`.
   $P_1$ runs from $t=0$ to $t=2$. Remaining $BT(P_1) = 3$.
2. **$t = 2$**: While $P_1$ ran, $P_2$ ($AT=1$) and $P_3$ ($AT=2$) arrived.
   Ready Queue receives new arrivals first, then preempted $P_1$: `[P2, P3, P1]`.
3. **$t = 2 \to 4$**: $P_2$ runs for slice 2 ($t=2$ to $t=4$). Remaining $BT(P_2) = 1$.
   During this slice, $P_4$ ($AT=3$) arrived.
   Ready Queue receives $P_4$, then preempted $P_2$: `[P3, P1, P4, P2]`.
4. **$t = 4 \to 5$**: $P_3$ runs for 1 unit (remaining $BT=1$).
   At $t = 5$, $P_3$ finishes!
   $$\mathbf{CT(P_3) = 5}, \quad TAT(P_3) = 5 - 2 = 3, \quad WT(P_3) = 3 - 1 = 2$$
   Ready Queue: `[P1, P4, P2]`.
5. **$t = 5 \to 7$**: $P_1$ runs for slice 2 ($t=5$ to $t=7$). Remaining $BT(P_1) = 1$.
   Ready Queue after re-enqueue: `[P4, P2, P1]`.
6. **$t = 7 \to 9$**: $P_4$ runs for 2 units ($t=7$ to $t=9$). Remaining $BT(P_4) = 0$.
   At $t = 9$, $P_4$ finishes!
   $$\mathbf{CT(P_4) = 9}, \quad TAT(P_4) = 9 - 3 = 6, \quad WT(P_4) = 6 - 2 = 4$$
   Ready Queue: `[P2, P1]`.
7. **$t = 9 \to 10$**: $P_2$ runs for 1 unit ($t=9$ to $t=10$). Remaining $BT(P_2) = 0$.
   At $t = 10$, $P_2$ finishes!
   $$\mathbf{CT(P_2) = 10}, \quad TAT(P_2) = 10 - 1 = 9, \quad WT(P_2) = 9 - 3 = 6$$
   Ready Queue: `[P1]`.
8. **$t = 10 \to 11$**: $P_1$ runs for its final 1 unit ($t=10$ to $t=11$).
   At $t = 11$, $P_1$ finishes!
   $$\mathbf{CT(P_1) = 11}, \quad TAT(P_1) = 11 - 0 = 11, \quad WT(P_1) = 11 - 5 = 6$$

#### Metric Summary Table:
| PID | Arrival ($AT$) | Burst ($BT$) | Completion ($CT$) | Turnaround ($TAT = CT - AT$) | Waiting ($WT = TAT - BT$) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **P1** | 0 | 5 | **11** | $11 - 0 = \mathbf{11}$ | $11 - 5 = \mathbf{6}$ |
| **P2** | 1 | 3 | **10** | $10 - 1 = \mathbf{9}$ | $9 - 3 = \mathbf{6}$ |
| **P3** | 2 | 1 | **5** | $5 - 2 = \mathbf{3}$ | $3 - 1 = \mathbf{2}$ |
| **P4** | 3 | 2 | **9** | $9 - 3 = \mathbf{6}$ | $6 - 2 = \mathbf{4}$ |

#### System Averages:
$$\text{Average Turnaround Time} = \frac{11 + 9 + 3 + 6}{4} = \frac{29}{4} = \mathbf{7.25} \text{ time units}$$
$$\text{Average Waiting Time} = \frac{6 + 6 + 2 + 4}{4} = \frac{18}{4} = \mathbf{4.50} \text{ time units}$$

---

## 13. Comparison of Queue Implementations

| Feature / Metric | Static Queue | Dynamic Queue | Circular Queue | Deque (Circular) | Priority Queue (Array) | Priority Queue (Heap) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Underlying Structure** | Fixed Python list | Singly linked list | Fixed Python list | Fixed Python list | Sorted Python list | Binary min-heap array |
| **Capacity Bounded?** | Yes (Fixed) | No (Unbounded) | Yes (Fixed) | Yes (Fixed) | Optional | Optional |
| **Enqueue / Insert Time** | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ | $O(n)$ | $O(\log n)$ |
| **Dequeue / Extract Time** | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ | $O(n)$ (or $O(1)$) | $O(\log n)$ |
| **Peek Time** | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ |
| **False Overflow Risk?** | **Yes** (severe) | No | **No** (reused) | **No** (reused) | No | No |
| **Memory Overhead** | Low (contiguous) | High (pointer/node) | Low (contiguous) | Low (contiguous) | Low | Low |
| **Cache Locality** | Excellent | Poor (heap dispersed)| Excellent | Excellent | Moderate | Excellent |
| **Bidirectional Access?** | No | No | No | **Yes** | No | No |
| **Priority Support?** | No (FIFO only) | No (FIFO only) | No (FIFO only) | No (Both ends) | **Yes** ($O(n)$) | **Yes** ($O(\log n)$) |

---

## 14. Priority Queue and Heap Explanation

### Concept of Priority Queue
In standard queues, the eviction order is governed exclusively by arrival time ($t_{\text{arrival}}$). In a **Priority Queue**, every element is assigned an explicit priority key. Elements with superior priority are retrieved ahead of elements with inferior priority.

### Priority Conventions
- **Min-Priority Queue (Used Here)**: Lower numeric priority value = higher urgency ($1 > 2 > 3$).
- **Max-Priority Queue**: Higher numeric priority value = higher urgency ($100 > 50 > 10$).

### Comparison: Sorted Array vs Binary Heap

```
Sorted Array Priority Queue (Insert is O(n), Extract-Min is O(n) or O(1))
[ (Pri:1, A) , (Pri:2, B) , (Pri:2, C) , (Pri:3, D) , (Pri:5, E) ]
      ^
  Index 0 is highest priority

Binary Min-Heap Priority Queue (Insert is O(log n), Extract-Min is O(log n))
                  [Pri:1, A]
                 /          \
         [Pri:2, B]        [Pri:2, C]
         /        \
    [Pri:5, E]   [Pri:3, D]
```

1. **Sorted Array**:
   - `insert`: Finding insertion point and shifting elements requires $O(n)$ time.
   - `extract_min`: Accessing index 0 is $O(1)$, but shifting remaining elements takes $O(n)$ (unless kept in reverse order).
   - Inefficient for high-throughput streaming systems with large $n$.
2. **Binary Min-Heap**:
   - Represents a complete binary tree stored inside a contiguous array.
   - Height of complete binary tree with $n$ nodes is guaranteed to be $\lfloor \log_2 n \rfloor$.
   - `insert`: Appends element to end and bubbles up along tree height $\to O(\log n)$.
   - `extract_min`: Swaps root with leaf, pops leaf, and sifts downward along tree height $\to O(\log n)$.
   - Dramatically outperforms sorted arrays when $n$ is large.

### Guaranteeing FIFO Stability
A naive priority queue does not preserve FIFO order among items with identical priorities. To enforce fairness, each entry is tagged with a monotonic arrival sequence number:
$$\text{key} = (\text{priority}, \text{arrival\_counter})$$
Since Python evaluates tuples element-by-element:
- If $\text{pri}_A < \text{pri}_B \implies A \text{ has precedence}$.
- If $\text{pri}_A == \text{pri}_B \implies \text{the item with smaller } \text{arrival\_counter} \text{ has precedence}$.

---

## 15. Algorithm and Pseudocode for Every Experiment

### Experiment 1: Static Queue

#### Algorithm: `enqueue(item)`
1. If `rear == capacity - 1`: raise `OverflowError("Queue Overflow")`.
2. If `front == -1`: set `front = 0`.
3. Increment `rear = rear + 1`.
4. Set `data[rear] = item`.

#### Algorithm: `dequeue()`
1. If `front == -1` or `front > rear`: raise `IndexError("Queue Underflow")`.
2. Retrieve `item = data[front]`; set `data[front] = None`.
3. Increment `front = front + 1`.
4. If `front > rear`: reset `front = -1`, `rear = -1`.
5. Return `item`.

```text
CLASS StaticQueue:
    CONSTRUCTOR(capacity):
        self.capacity = capacity
        self.data = ARRAY OF SIZE capacity (INITIALIZED TO NONE)
        self.front = -1
        self.rear = -1

    FUNCTION enqueue(item):
        IF self.rear == self.capacity - 1 THEN:
            RAISE OverflowError("Queue Overflow")
        IF self.front == -1 THEN:
            self.front = 0
        self.rear = self.rear + 1
        self.data[self.rear] = item

    FUNCTION dequeue():
        IF self.front == -1 OR self.front > self.rear THEN:
            RAISE IndexError("Queue Underflow")
        item = self.data[self.front]
        self.data[self.front] = None
        self.front = self.front + 1
        IF self.front > self.rear THEN:
            self.front = -1
            self.rear = -1
        RETURN item
```

---

### Experiment 2: Dynamic Queue

#### Algorithm: `enqueue(item)`
1. Allocate `new_node = QueueNode(item)`.
2. If `rear is None`:
   - `front = new_node`
   - `rear = new_node`
3. Else:
   - `rear.next = new_node`
   - `rear = new_node`
4. Increment `size = size + 1`.

#### Algorithm: `dequeue()`
1. If `front is None`: raise `IndexError("Queue Underflow")`.
2. `item = front.data`.
3. Advance `front = front.next`.
4. If `front is None`: set `rear = None`.
5. Decrement `size = size - 1`.
6. Return `item`.

```text
CLASS QueueNode:
    CONSTRUCTOR(data):
        self.data = data
        self.next = NONE

CLASS DynamicQueue:
    CONSTRUCTOR():
        self.front = NONE
        self.rear = NONE
        self.count = 0

    FUNCTION enqueue(item):
        node = NEW QueueNode(item)
        IF self.rear IS NONE THEN:
            self.front = node
            self.rear = node
        ELSE:
            self.rear.next = node
            self.rear = node
        self.count = self.count + 1

    FUNCTION dequeue():
        IF self.front IS NONE THEN:
            RAISE IndexError("Queue Underflow")
        item = self.front.data
        self.front = self.front.next
        IF self.front IS NONE THEN:
            self.rear = NONE
        self.count = self.count - 1
        RETURN item
```

---

### Experiment 3: Circular Queue

#### Algorithm: `enqueue(item)`
1. If `_count == capacity`: raise `OverflowError("Circular Queue Overflow")`.
2. If `_count == 0`: `front = 0`, `rear = 0`.
3. Else: `rear = (rear + 1) % capacity`.
4. `data[rear] = item`.
5. Increment `_count = _count + 1`.

#### Algorithm: `dequeue()`
1. If `_count == 0`: raise `IndexError("Circular Queue Underflow")`.
2. `item = data[front]`; `data[front] = None`.
3. Decrement `_count = _count - 1`.
4. If `_count == 0`: `front = -1`, `rear = -1`.
5. Else: `front = (front + 1) % capacity`.
6. Return `item`.

```text
CLASS CircularQueue:
    CONSTRUCTOR(capacity):
        self.capacity = capacity
        self.data = ARRAY OF SIZE capacity (ALL NONE)
        self.front = -1
        self.rear = -1
        self.count = 0

    FUNCTION enqueue(item):
        IF self.count == self.capacity THEN:
            RAISE OverflowError("Queue is full")
        IF self.count == 0 THEN:
            self.front = 0
            self.rear = 0
        ELSE:
            self.rear = (self.rear + 1) MOD self.capacity
        self.data[self.rear] = item
        self.count = self.count + 1

    FUNCTION dequeue():
        IF self.count == 0 THEN:
            RAISE IndexError("Queue is empty")
        item = self.data[self.front]
        self.data[self.front] = NONE
        self.count = self.count - 1
        IF self.count == 0 THEN:
            self.front = -1
            self.rear = -1
        ELSE:
            self.front = (self.front + 1) MOD self.capacity
        RETURN item
```

---

### Experiment 4: Deque (Circular Array)

#### Algorithm: `insert_front(item)`
1. If `_count == capacity`: raise `OverflowError`.
2. If `_count == 0`: `front = 0`, `rear = 0`.
3. Else: `front = (front - 1 + capacity) % capacity`.
4. `data[front] = item`.
5. Increment `_count = _count + 1`.

#### Algorithm: `delete_rear()`
1. If `_count == 0`: raise `IndexError`.
2. `item = data[rear]`; `data[rear] = None`.
3. Decrement `_count = _count - 1`.
4. If `_count == 0`: `front = -1`, `rear = -1`.
5. Else: `rear = (rear - 1 + capacity) % capacity`.
6. Return `item`.

```text
CLASS Deque:
    CONSTRUCTOR(capacity):
        self.capacity = capacity
        self.data = ARRAY OF SIZE capacity
        self.front = -1
        self.rear = -1
        self.count = 0

    FUNCTION insert_front(item):
        IF self.count == self.capacity THEN RAISE OverflowError()
        IF self.count == 0 THEN:
            self.front = 0; self.rear = 0
        ELSE:
            self.front = (self.front - 1 + self.capacity) MOD self.capacity
        self.data[self.front] = item
        self.count = self.count + 1

    FUNCTION delete_rear():
        IF self.count == 0 THEN RAISE IndexError()
        item = self.data[self.rear]
        self.data[self.rear] = NONE
        self.count = self.count - 1
        IF self.count == 0 THEN:
            self.front = -1; self.rear = -1
        ELSE:
            self.rear = (self.rear - 1 + self.capacity) MOD self.capacity
        RETURN item
```

---

### Experiment 5: Array-Based Priority Queue

```text
CLASS ArrayPriorityQueue:
    CONSTRUCTOR(capacity):
        self.capacity = capacity
        self.items = EMPTY LIST
        self.counter = 0

    FUNCTION insert(data, priority):
        IF self.capacity IS NOT NONE AND LENGTH(self.items) >= self.capacity THEN:
            RAISE OverflowError()
        self.counter = self.counter + 1
        new_item = Item(data, priority, self.counter)
        insert_idx = LENGTH(self.items)
        FOR i FROM 0 TO LENGTH(self.items) - 1:
            IF priority < self.items[i].priority THEN:
                insert_idx = i; BREAK
            ELSE IF priority == self.items[i].priority AND self.counter < self.items[i].seq THEN:
                insert_idx = i; BREAK
        INSERT new_item AT self.items[insert_idx]

    FUNCTION remove_highest_priority():
        IF LENGTH(self.items) == 0 THEN RAISE IndexError()
        RETURN self.items.POP(0).data
```

---

### Experiment 6: Heap-Based Priority Queue

```text
CLASS HeapPriorityQueue:
    CONSTRUCTOR(capacity):
        self.capacity = capacity
        self.heap = EMPTY LIST
        self.counter = 0

    FUNCTION _parent(i): RETURN (i - 1) // 2
    FUNCTION _left(i):   RETURN 2 * i + 1
    FUNCTION _right(i):  RETURN 2 * i + 2

    FUNCTION insert(data, priority):
        IF self.capacity IS NOT NONE AND LENGTH(self.heap) >= self.capacity THEN:
            RAISE OverflowError()
        self.counter = self.counter + 1
        node = Node(data, priority, self.counter)
        self.heap.APPEND(node)
        self._heapify_up(LENGTH(self.heap) - 1)

    FUNCTION _heapify_up(index):
        WHILE index > 0:
            p = self._parent(index)
            IF self.heap[index].key() < self.heap[p].key() THEN:
                SWAP self.heap[index], self.heap[p]
                index = p
            ELSE: BREAK

    FUNCTION remove_highest_priority():
        IF LENGTH(self.heap) == 0 THEN RAISE IndexError()
        IF LENGTH(self.heap) == 1 THEN RETURN self.heap.POP().data
        root_data = self.heap[0].data
        self.heap[0] = self.heap.POP()
        self._heapify_down(0)
        RETURN root_data

    FUNCTION _heapify_down(index):
        n = LENGTH(self.heap)
        WHILE TRUE:
            smallest = index
            l = self._left(index)
            r = self._right(index)
            IF l < n AND self.heap[l].key() < self.heap[smallest].key() THEN smallest = l
            IF r < n AND self.heap[r].key() < self.heap[smallest].key() THEN smallest = r
            IF smallest != index THEN:
                SWAP self.heap[index], self.heap[smallest]
                index = smallest
            ELSE: BREAK
```

---

### Experiment 7: Customer Service Queue Simulation

```text
CLASS CustomerServiceSimulator:
    CONSTRUCTOR():
        self.vip_queue = NEW CustomerQueue("VIP")
        self.reg_queue = NEW CustomerQueue("Regular")
        self.step = 1

    FUNCTION register_customer(name, service, is_vip):
        IF is_vip THEN:
            ticket = "VIP-" + STR(vip_counter++)
            cust = NEW Customer(ticket, name, service, is_vip, self.step)
            self.vip_queue.enqueue(cust)
        ELSE:
            ticket = "REG-" + STR(reg_counter++)
            cust = NEW Customer(ticket, name, service, is_vip, self.step)
            self.reg_queue.enqueue(cust)
        self.step = self.step + 1
        RETURN cust

    FUNCTION serve_customer():
        IF NOT self.vip_queue.is_empty() THEN:
            cust = self.vip_queue.dequeue()
        ELSE IF NOT self.reg_queue.is_empty() THEN:
            cust = self.reg_queue.dequeue()
        ELSE:
            RETURN NONE
        wait_time = self.step - cust.arrival_step
        RECORD_HISTORY(cust, self.step, wait_time)
        self.step = self.step + 1
        RETURN cust
```

---

### Experiment 8: Round Robin Process Scheduling

```text
CLASS RoundRobinScheduler:
    CONSTRUCTOR(quantum):
        self.quantum = quantum
        self.processes = EMPTY LIST

    FUNCTION run_simulation():
        SORT self.processes BY (arrival_time, pid)
        ready_queue = NEW FIFOQueue()
        current_time = 0
        completed = 0
        n = LENGTH(self.processes)
        arr_idx = 0

        WHILE completed < n:
            IF ready_queue.is_empty():
                IF arr_idx < n:
                    current_time = MAX(current_time, self.processes[arr_idx].arrival_time)
                    WHILE arr_idx < n AND self.processes[arr_idx].arrival_time <= current_time:
                        ready_queue.enqueue(self.processes[arr_idx])
                        arr_idx = arr_idx + 1

            p = ready_queue.dequeue()
            exec_time = MIN(self.quantum, p.remaining_time)
            current_time = current_time + exec_time
            p.remaining_time = p.remaining_time - exec_time

            # Enqueue new arrivals first
            WHILE arr_idx < n AND self.processes[arr_idx].arrival_time <= current_time:
                ready_queue.enqueue(self.processes[arr_idx])
                arr_idx = arr_idx + 1

            # Check completion or re-enqueue
            IF p.remaining_time == 0 THEN:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                completed = completed + 1
            ELSE:
                ready_queue.enqueue(p)

        RETURN finished_processes
```

---

## 16. Dry Runs

### Dry Run 1: Circular Queue Wraparound
- **Capacity**: $4$
- Initial: `data = [None, None, None, None]`, `front = -1`, `rear = -1`, `count = 0`

| Step | Operation | `front` | `rear` | `count` | Array State `[0, 1, 2, 3]` | Explanation |
|:---:|:---|:---:|:---:|:---:|:---|:---|
| 1 | `enqueue(10)` | 0 | 0 | 1 | `[10, None, None, None]` | First element initialized |
| 2 | `enqueue(20)` | 0 | 1 | 2 | `[10, 20, None, None]` | `rear = (0+1)%4 = 1` |
| 3 | `enqueue(30)` | 0 | 2 | 3 | `[10, 20, 30, None]` | `rear = (1+1)%4 = 2` |
| 4 | `dequeue() -> 10` | 1 | 2 | 2 | `[None, 20, 30, None]` | `front = (0+1)%4 = 1`; slot 0 freed |
| 5 | `dequeue() -> 20` | 2 | 2 | 1 | `[None, None, 30, None]` | `front = (1+1)%4 = 2`; slot 1 freed |
| 6 | `enqueue(40)` | 2 | 3 | 2 | `[None, None, 30, 40]` | `rear = (2+1)%4 = 3` |
| 7 | **`enqueue(50)`** | 2 | **0** | 3 | `[50, None, 30, 40]` | **Wraparound!** `rear = (3+1)%4 = 0` |
| 8 | **`enqueue(60)`** | 2 | **1** | 4 | `[50, 60, 30, 40]` | **Wraparound!** `rear = (0+1)%4 = 1` (Full) |

---

### Dry Run 2: Heap Priority Queue Insertion & Extraction
Insert operations: `insert("A", pri=3)`, `insert("B", pri=1)`, `insert("C", pri=2)`

1. **Insert ("A", pri=3, seq=1)**:
   - Heap: `[ (3, 1, "A") ]`. Root is at index 0.
2. **Insert ("B", pri=1, seq=2)**:
   - Append to index 1: `[ (3, 1, "A"), (1, 2, "B") ]`.
   - `_heapify_up(1)`: Parent is index 0 `(3, 1)`.
   - Key `(1, 2) < (3, 1)` $\implies$ Swap!
   - Heap: `[ (1, 2, "B"), (3, 1, "A") ]`.
3. **Insert ("C", pri=2, seq=3)**:
   - Append to index 2: `[ (1, 2, "B"), (3, 1, "A"), (2, 3, "C") ]`.
   - `_heapify_up(2)`: Parent is index 0 `(1, 2)`.
   - Key `(2, 3) >= (1, 2)` $\implies$ Heap property holds.
4. **Extract-Min (`remove_highest_priority()`)**:
   - Save root `"B"`.
   - Move last item `"C"` to root: `[ (2, 3, "C"), (3, 1, "A") ]`.
   - `_heapify_down(0)`: Left child is index 1 `(3, 1)`.
   - `(2, 3) < (3, 1)` $\implies$ Heap property holds.
   - Return `"B"`. Next root is `"C"`.

---

## 17. Time and Space Complexity

| Program / Algorithm | Operation | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
|:---|:---|:---:|:---:|:---:|:---:|
| **Program 1: Static Queue** | `enqueue` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| | `dequeue` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| | `peek` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| **Program 2: Dynamic Queue** | `enqueue` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| | `dequeue` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| | `peek` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| **Program 3: Circular Queue** | `enqueue` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| | `dequeue` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| | `peek` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| **Program 4: Deque** | `insert_front` / `insert_rear` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| | `delete_front` / `delete_rear` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| | `peek_front` / `peek_rear` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| **Program 5: Array Priority Queue** | `insert` | $\Theta(1)$ | $\Theta(n)$ | $O(n)$ | $O(1)$ |
| | `remove_highest` | $\Theta(n)$ | $\Theta(n)$ | $O(n)$ | $O(1)$ |
| | `peek` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| **Program 6: Heap Priority Queue** | `insert` | $\Theta(1)$ | $\Theta(\log n)$ | $O(\log n)$ | $O(1)$ |
| | `remove_highest` | $\Theta(1)$ | $\Theta(\log n)$ | $O(\log n)$ | $O(1)$ |
| | `peek` | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| **Program 7: Customer Service** | Register / Serve | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(n)$ |
| **Program 8: Process Scheduling** | Round Robin Simulation | $\Theta(n + \sum BT / TQ)$ | $\Theta(n + \sum BT / TQ)$ | $O(n + \sum BT / TQ)$ | $O(n)$ |

---

## 18. Testing and Sample I/O

All eight programs contain comprehensive automated unit test suites triggered via the `--test` CLI argument.

### Automated Test Suite Execution Log

```console
$ python3 Lab05-Queues/Program01-StaticQueue/static_queue.py --test && \
  python3 Lab05-Queues/Program02-DynamicQueue/dynamic_queue.py --test && \
  python3 Lab05-Queues/Program03-CircularQueue/circular_queue.py --test && \
  python3 Lab05-Queues/Program04-Deque/deque.py --test && \
  python3 Lab05-Queues/Program05-ArrayPriorityQueue/array_priority_queue.py --test && \
  python3 Lab05-Queues/Program06-HeapPriorityQueue/heap_priority_queue.py --test && \
  python3 Lab05-Queues/Program07-CustomerServiceSimulation/customer_service.py --test && \
  python3 Lab05-Queues/Program08-ProcessScheduling/process_scheduling.py --test

=================================================================
RUNNING COMPREHENSIVE TESTS: Static Queue (Program 01)
=================================================================
  [Test 01 Passed] Caught non-positive capacity.
  [Test 02 Passed] Caught dequeue underflow: Queue Underflow: Cannot dequeue from an empty queue.
  [Test 03 Passed] Caught peek underflow: Queue Underflow: Cannot peek into an empty queue.
  [Test 04 Passed] Enqueue, peek, and is_full verified.
  [Test 05 Passed] Caught queue overflow: Queue Overflow: Cannot enqueue into full linear queue (Capacity: 3). Even if elements were dequeued, linear arrays cannot reuse front slots.
  [Test 06 Passed] Strict FIFO dequeue order verified.
  [Test 07 Passed] Linear queue limitation (false overflow) demonstrated.

All Program 01 automated tests PASSED successfully!
=================================================================
RUNNING COMPREHENSIVE TESTS: Dynamic Queue (Program 02)
=================================================================
  [Test 01 Passed] Caught dequeue underflow: Queue Underflow: Cannot dequeue from an empty dynamic queue.
  [Test 02 Passed] Caught peek underflow: Queue Underflow: Cannot peek into an empty dynamic queue.
  [Test 03 Passed] Single-element enqueue verified.
  [Test 04 Passed] Dequeue to empty correctly cleared front and rear.
  [Test 05 Passed] FIFO order and size tracking verified.
  [Test 06 Passed] Dynamic heap scaling and deallocation verified.

All Program 02 automated tests PASSED successfully!
=================================================================
RUNNING COMPREHENSIVE TESTS: Circular Queue (Program 03)
=================================================================
  [Test 01 Passed] Caught dequeue underflow: Circular Queue Underflow: Cannot dequeue from an empty queue.
  [Test 02 Passed] Full capacity enqueue verified.
  [Test 03 Passed] Caught circular queue overflow: Circular Queue Overflow: All 4 slots are occupied.
  [Test 04 Passed] Dequeued elements freeing front physical slots.
  [Test 05 Passed] Modular wraparound and slot reuse successfully verified.
  [Test 06 Passed] Complete FIFO dequeue across wraparound boundary verified.

All Program 03 automated tests PASSED successfully!
======================================================================
RUNNING AUTOMATED TEST SUITE: Circular Array Deque
======================================================================
[PASS] Test 1: Initial state verified.
[PASS] Test 2: Standard FIFO queue operations verified.
[PASS] Test 3: Bidirectional front/rear additions & removals verified.
[PASS] Test 4: Capacity limit & Overflow handling verified.
[PASS] Test 5: Circular modular wraparound verified.
[PASS] Test 6: Underflow handling verified.

ALL 6 TEST CASES PASSED SUCCESSFULLY!
======================================================================
======================================================================
RUNNING AUTOMATED TEST SUITE: Array Priority Queue
======================================================================
[PASS] Test 1: Initial state verified.
[PASS] Test 2: Priority ordering verified.
[PASS] Test 3: FIFO stability for identical priorities verified.
[PASS] Test 4: Capacity limit and overflow verified.
[PASS] Test 5: Removal in order & underflow handling verified.

ALL 5 TEST CASES PASSED SUCCESSFULLY!
======================================================================
======================================================================
RUNNING AUTOMATED TEST SUITE: Binary Min-Heap Priority Queue
======================================================================
[PASS] Test 1: Initial state verified.
[PASS] Test 2: Min-heap ordering verified.
[PASS] Test 3: FIFO tie-breaking for equal priorities verified.
[PASS] Test 4: Capacity limit & overflow verified.
[PASS] Test 5: Full extraction sequence and underflow handling verified.

ALL 5 TEST CASES PASSED SUCCESSFULLY!
======================================================================
======================================================================
RUNNING AUTOMATED TEST SUITE: Customer Service Queue Simulation
======================================================================
[PASS] Test 1: Initial state verified.
[PASS] Test 2: Regular customer arrival and FIFO order verified.
[PASS] Test 3: VIP priority precedence verified.
[PASS] Test 4: Strict service priority order and empty queue handling verified.
[PASS] Test 5: Historical reporting and metrics verified.

ALL 5 TEST CASES PASSED SUCCESSFULLY!
======================================================================
======================================================================
RUNNING AUTOMATED TEST SUITE: Round Robin Process Scheduler
======================================================================
[PASS] Test 1: Textbook multi-process Round Robin scheduling verified.
[PASS] Test 2: CPU idle period and delayed arrival verified.
[PASS] Test 3: Large quantum (degenerates to FCFS) verified.

ALL 3 TEST CASES PASSED SUCCESSFULLY!
======================================================================
```

---

## 19. Real-Life Applications

1. **Operating System Schedulers**: Round Robin CPU scheduling, multi-level feedback queues (MLFQ), and I/O disk request elevators.
2. **Networking Protocols**: Router packet buffers, traffic shaping (Leaky Bucket and Token Bucket algorithms), and TCP socket receiver windows.
3. **Cloud Infrastructure and Microservices**: Asynchronous message queues (Amazon SQS, Apache Kafka, RabbitMQ) decoupling producers from consumer clusters.
4. **Media Players & Streaming**: Audio/video jitter buffers using circular queues to ensure uninterrupted playback.
5. **Call Centers & Customer Support**: Multi-tier telephone switchboards prioritizing premium enterprise callers over standard tier inquiries.

---

## 20. Folder Structure

```text
Lab05-Queues/
├── Program01-StaticQueue/
│   └── static_queue.py
├── Program02-DynamicQueue/
│   └── dynamic_queue.py
├── Program03-CircularQueue/
│   └── circular_queue.py
├── Program04-Deque/
│   └── deque.py
├── Program05-ArrayPriorityQueue/
│   └── array_priority_queue.py
├── Program06-HeapPriorityQueue/
│   └── heap_priority_queue.py
├── Program07-CustomerServiceSimulation/
│   └── customer_service.py
├── Program08-ProcessScheduling/
│   └── process_scheduling.py
├── README.md
└── reflection.md
```

---

## 21. Execution Instructions

All programs can be run interactively through a menu-driven terminal interface, or validated immediately through built-in automated test suites using the `--test` flag.

### 1. Interactive Menu Mode
Execute any script directly:
```bash
python3 Lab05-Queues/Program01-StaticQueue/static_queue.py
python3 Lab05-Queues/Program02-DynamicQueue/dynamic_queue.py
python3 Lab05-Queues/Program03-CircularQueue/circular_queue.py
python3 Lab05-Queues/Program04-Deque/deque.py
python3 Lab05-Queues/Program05-ArrayPriorityQueue/array_priority_queue.py
python3 Lab05-Queues/Program06-HeapPriorityQueue/heap_priority_queue.py
python3 Lab05-Queues/Program07-CustomerServiceSimulation/customer_service.py
python3 Lab05-Queues/Program08-ProcessScheduling/process_scheduling.py
```

### 2. Automated Self-Testing Mode
Execute automated unit verification across all programs:
```bash
python3 Lab05-Queues/Program01-StaticQueue/static_queue.py --test
python3 Lab05-Queues/Program02-DynamicQueue/dynamic_queue.py --test
python3 Lab05-Queues/Program03-CircularQueue/circular_queue.py --test
python3 Lab05-Queues/Program04-Deque/deque.py --test
python3 Lab05-Queues/Program05-ArrayPriorityQueue/array_priority_queue.py --test
python3 Lab05-Queues/Program06-HeapPriorityQueue/heap_priority_queue.py --test
python3 Lab05-Queues/Program07-CustomerServiceSimulation/customer_service.py --test
python3 Lab05-Queues/Program08-ProcessScheduling/process_scheduling.py --test
```

---

## 22. Learning Outcomes

By completing Unit 5, students have successfully achieved:
1. **FIFO Invariant Mastery**: Rigorous understanding of queue semantics, boundary transitions, and pointer synchronizations across both contiguous and linked architectures.
2. **Circular Buffer Fluency**: Ability to employ modular arithmetic to eliminate false overflow and build high-performance circular buffers.
3. **Double-Ended Adaptability**: Mastery of bidirectional insertion and removal using Deque structures.
4. **Priority Queue Engineering**: Practical competence implementing binary min-heaps from first principles, preserving strict FIFO stability via sequence numbers, and evaluating $O(n)$ versus $O(\log n)$ asymptotic tradeoffs.
5. **Applied Systems Simulation**: Direct application of queues to discrete-event simulations, including multi-tier customer ticketing and operating system CPU scheduling with complete metric derivation ($AT, BT, CT, TAT, WT$).

---

## 23. References

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press. Chapter 10: Elementary Data Structures (Queues, Stacks), Chapter 6: Heapsort & Priority Queues.
2. Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). Wiley. Chapter 5: CPU Scheduling (Round Robin, Ready Queues).
3. Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2013). *Data Structures and Algorithms in Python*. John Wiley & Sons. Chapter 6: Stacks, Queues, and Deques.
4. Knuth, D. E. (1997). *The Art of Computer Programming, Volume 1: Fundamental Algorithms* (3rd ed.). Addison-Wesley. Section 2.2: Linear Data Structures.

