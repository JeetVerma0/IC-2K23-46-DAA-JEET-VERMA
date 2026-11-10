# IC-307D: Data Structures and Algorithms Lab
## Unit 7: Graphs (CO3)

---

## 1. Introduction to Graph Data Structures

A **Graph** $G = (V, E)$ is a versatile, non-linear mathematical abstract data type (ADT) defined by:
- A non-empty set of **Vertices** (or nodes) $V$.
- A set of **Edges** (or arcs/links) $E$, where each edge connects an ordered or unordered pair of vertices $(u, v) \in V \times V$.

Unlike hierarchical trees, graphs do not enforce a root node, parent-child relationships, or cycle-free topology. Edges can interconnect vertices arbitrarily, enabling models of complex real-world networks.

```
       Undirected Graph                   Directed Graph (Digraph)
          (0) --- (1)                           (0) ---> (1)
           |   \   |                             |   ^    |
           |    \  |                             |    \   |
           |     \ |                             v     \  v
          (2) --- (3)                           (2) ---> (3)
```

### Core Graph Taxonomy
1. **Undirected Graph**: Edges are bidirectional. If $(u, v) \in E$, then $(v, u) \in E$.
2. **Directed Graph (Digraph)**: Edges have orientation. An edge $u \to v$ denotes a directed transition from source $u$ to target $v$.
3. **Weighted Graph**: Each edge $(u, v)$ carries an associated numeric cost, weight, or distance $w(u, v) \in \mathbb{R}$.
4. **Degree of a Vertex**:
   - In an undirected graph: The number of edges incident to vertex $v$ ($\text{deg}(v)$).
   - In a directed graph: **In-degree** ($\text{deg}^-(v)$, incoming edges) and **Out-degree** ($\text{deg}^+(v)$, outgoing edges).
5. **Path & Simple Path**: A sequence of vertices $\langle v_0, v_1, \dots, v_k \rangle$ such that $(v_{i-1}, v_i) \in E$. A simple path contains no repeated vertices.
6. **Cycle**: A path $\langle v_0, v_1, \dots, v_k \rangle$ where $v_0 = v_k$ and $k \ge 3$ (in undirected graphs) or $k \ge 1$ (in directed graphs).
7. **Connected Graph / Components**: An undirected graph is connected if a path exists between every pair of vertices. Disconnected graphs partition into maximal connected subgraphs called **Connected Components**.
8. **Directed Acyclic Graph (DAG)**: A directed graph with zero directed cycles, forming the theoretical prerequisite for topological ordering.

Graphs serve as the foundational model for telecommunication networks, social networks, road maps, web search rankings (PageRank), supply chain routing, dependency resolution, and circuit design.

---

## 2. Aim

To study, design, implement from first principles, empirically test, and analyze fundamental graph representations and algorithms in Python 3; to master Breadth-First Search (BFS) and Depth-First Search (DFS) in both recursive and iterative configurations; to implement Dijkstra's Single-Source Shortest Path algorithm with a custom binary min-heap; to build graph-based applications including a Social Network simulator, a 2D Maze Solver, and a DAG Course Prerequisite Scheduler with Kahn's topological sort and cycle detection.

---

## 3. Learning Objectives

- Master the trade-offs between **Adjacency Matrix** ($O(V^2)$ space, $O(1)$ edge lookup) and **Adjacency List** ($O(V + E)$ space, optimal for sparse networks).
- Design and implement iterative **Breadth-First Search (BFS)** using a custom manual FIFO queue, exploring vertices level-by-level and discovering unweighted shortest paths.
- Contrast **Recursive DFS** (implicit call stack) with **Iterative DFS** (explicit LIFO stack), analyzing vertex discovery orders and immunity to recursion limits.
- Formulate and implement **Dijkstra's Algorithm** using a custom binary min-heap priority queue, analyzing the relaxation invariant and mathematical reasons why negative weights fail.
- Model real-world relational networks: mutual social friendships, 2-hop friend-of-friend recommendations, and connected community clustering.
- Model a 2D spatial grid as an implicit graph and solve shortest-path maze navigation using BFS.
- Understand the algebraic properties of **Directed Acyclic Graphs (DAGs)**, calculate in-degrees, execute **Kahn's Topological Sort**, and detect circular prerequisite deadlocks.

---

## 4. Software Requirements

- **Operating System**: Linux (Ubuntu 22.04 LTS / Debian 12 / POSIX-compliant) or Windows 10/11 / macOS.
- **Language**: Python 3.8+ (Tested on Python 3.10 / 3.11).
- **External Dependencies**: None. Standard library built-ins only (strictly no `networkx`, `scipy`, `queue.Queue`, or `collections.deque` for core graph mechanics).
- **Terminal Shell**: Bash / Zsh / PowerShell.

---

## 5. Experiment 1: Adjacency Matrix

### Problem Statement
Implement a graph representation using an adjacency matrix. Provide methods to initialize a graph with $|V|$ vertices, add edges, remove edges, test edge existence, return neighbors, and display the formatted matrix. Support both directed and undirected configurations, validate vertex indices, and handle self-loops consistently.

### Approach
A 2D square matrix $M$ of size $|V| \times |V|$ is preallocated as a list of lists initialized with $0$:
- If an edge exists from $u$ to $v$, $M[u][v] = \text{weight}$ (default $1$).
- For undirected graphs, symmetry is maintained: $M[u][v] = M[v][u]$.
- For directed graphs, only $M[u][v]$ is updated.
- Self-loops set $M[u][u] = 1$.
- Vertex indices are validated against $0 \le u, v < |V|$, raising `IndexError` on out-of-bounds inputs.

### Complexity
- Edge Existence `has_edge(u, v)`: $O(1)$ time.
- Add / Remove Edge: $O(1)$ time.
- Iterate Neighbors of $u$: $O(V)$ time.
- Space Complexity: $O(V^2)$ contiguous space.

### Real-Life Applications
- Dense interconnection networks (e.g., crossbar switches, all-to-all communication topologies).
- Transition probability matrices in Markov chains and finite state automata.

---

## 6. Experiment 2: Adjacency List

### Problem Statement
Implement a graph using a dynamic adjacency list representation. Support dynamic vertex registration, edge additions, edge removals, vertex removals (with incident edge cleanup), neighbor queries, and formatted printing. Prevent duplicate edges and handle directed and undirected graphs.

### Approach
- An associative map binds each vertex identifier to a list of `EdgeNode(target, weight)` objects.
- Adding an edge checks if the target already exists; if present, its weight is updated, preventing duplicate records.
- For undirected graphs, symmetric edges are maintained in both lists.
- Removing a vertex removes the key and filters out all references to that vertex across all other adjacency lists.

### Complexity
- Add Vertex: $O(1)$ time.
- Add Edge: $O(\text{deg}(u))$ time to verify uniqueness.
- Remove Edge: $O(\text{deg}(u))$ time.
- Remove Vertex: $O(V + E)$ time.
- Space Complexity: $O(V + E)$ optimal space for sparse graphs.

### Real-Life Applications
- Web link graphs (billions of web pages where each page links to only dozens of URLs).
- Road networks (intersections connected by streets where degree is typically $\le 4$).

---

## 7. Experiment 3: Breadth-First Search (BFS)

### Problem Statement
Implement Breadth-First Search (BFS) iteratively using a custom manual FIFO queue (without `collections.deque`). Support single-source traversal, full traversal over disconnected graphs, and unweighted shortest-path reconstruction.

### Approach
1. Enqueue source $s$, mark $s$ as visited, and set tentative distances/parents.
2. While queue is not empty:
   - Dequeue vertex $u$ and record visitation.
   - For each unvisited neighbor $v$ of $u$:
     - Mark $v$ visited, record `parent[v] = u`, and enqueue $v$.
3. **Shortest Unweighted Path**: Because edges have uniform weight, BFS guarantees that when destination $d$ is first dequeued, the path recorded via parent pointers has the minimum number of edges.
4. **Disconnected Graphs**: An outer loop checks all vertices in $V$, initiating BFS on any unvisited node to cover all disconnected components.

### Complexity
- Time Complexity: $O(V + E)$ time.
- Auxiliary Space: $O(V)$ for the visited set, parent map, and manual queue.

### Real-Life Applications
- Web crawling (crawling web pages layer by layer up to depth $k$).
- Finding the fewest hops in packet routing and peer-to-peer file sharing.

---

## 8. Experiment 4: Recursive Depth-First Search (DFS)

### Problem Statement
Implement Depth-First Search recursively. Traverse vertices deeply along each branch before backtracking, track visited vertices, display traversal order, and handle disconnected graphs.

### Approach
- Initiated at vertex $u$: mark $u$ as visited and append to traversal order.
- For each neighbor $v$ of $u$:
  - If $v$ is not yet visited, recursively call `_dfs_helper(v)`.
- When all neighbors are visited, the function activation frame pops off the call stack, naturally backtracking to $u$'s parent.
- An outer loop sweeps across all vertices to visit all disconnected components.

### Complexity
- Time Complexity: $O(V + E)$ time.
- Auxiliary Space: $O(V)$ maximum call stack recursion depth.

### Real-Life Applications
- Cycle detection in software dependency managers.
- Pathfinding in puzzle games (Sudoku solvers, chess move search trees).

---

## 9. Experiment 5: Iterative Depth-First Search (DFS)

### Problem Statement
Implement Depth-First Search iteratively using an explicit LIFO stack. Eliminate recursion, track visited vertices, handle disconnected components, and analyze the relationship between stack-based and recursive visitation orders.

### Approach
- Push start vertex $s$ onto an explicit stack (`stack = [s]`).
- While stack is not empty:
  - Pop vertex $u$.
  - If $u$ is not visited:
    - Mark $u$ visited and record in traversal order.
    - Push unvisited neighbors onto the stack.
- **Ordering Detail**: Because stacks are LIFO, neighbors are pushed in **reverse-sorted order**, ensuring the first neighbor is popped and explored first, matching the canonical recursive sequence.
- Operates safely on heap memory, avoiding Python's default 1000-frame recursion limit.

### Complexity
- Time Complexity: $O(V + E)$ time.
- Auxiliary Space: $O(V)$ for visited set and explicit stack.

### Real-Life Applications
- Graph traversal in memory-constrained environments where stack overflows must be strictly prevented.
- Static code analysis engines scanning large call graphs.

---

## 10. Experiment 6: Weighted Graph and Dijkstra's Algorithm

### Problem Statement
Implement a weighted graph and Dijkstra's algorithm. Calculate shortest distances from a single source, reconstruct shortest paths, clearly display unreachable nodes ($\infty$), reject negative edge weights, and manage candidate vertices with a custom binary min-heap priority queue.

### Approach
- **Min-Heap**: Implements `insert` ($O(\log V)$) and `extract_min` ($O(\log V)$) storing `(distance, vertex)` tuples.
- **Relaxation Invariant**: For edge $u \to v$ with weight $w(u, v)$:
  $$\text{if } \text{dist}[u] + w(u, v) < \text{dist}[v] \implies \text{dist}[v] = \text{dist}[u] + w(u, v), \quad \text{pred}[v] = u$$
- **Negative Edge Rejection**: Dijkstra relies on the greedy invariant that once a vertex is extracted from the min-heap, its shortest path is permanently finalized. A negative edge could invalidate this assumption. Any negative weight input raises a `ValueError`.
- **Path Reconstruction**: Traces `predecessor[v]` backwards from destination to source, reversing the list.

### Complexity
- Time Complexity: $O((V + E) \log V)$ with binary min-heap.
- Auxiliary Space: $O(V)$ for distance table, predecessor map, and min-heap.

### Real-Life Applications
- GPS navigation systems (Google Maps, OpenStreetMap) computing shortest travel routes.
- Open Shortest Path First (OSPF) routing protocol in Internet routers.

---

## 11. Experiment 7: Social Network / Friendship Graph

### Problem Statement
Build an interactive Social Network simulator on an undirected adjacency list graph. Support user registration, friendship creation/removal, listing immediate friends, recommending friends-of-friends (FoF), computing degrees of separation (shortest chain via BFS), and discovering social clusters (connected components).

### Approach
- **Undirected Invariant**: Friendships are strictly mutual: adding $(u, v)$ updates both adjacency lists.
- **Friends of Friends (2-Hop Search)**:
  $$\text{FoF}(u) = \left( \bigcup_{v \in \text{Friends}(u)} \text{Friends}(v) \right) \setminus (\{u\} \cup \text{Friends}(u))$$
  Explores neighbors of neighbors while filtering out $u$ and $u$'s direct friends to generate recommendations.
- **Degrees of Separation**: Custom manual BFS queue finds the shortest chain connecting two users.
- **Social Clusters**: Full graph traversal extracts disconnected components representing isolated social communities.

### Complexity
- Add Friendship: $O(1)$.
- Friends of Friends: $O(\text{deg}(u) \cdot \text{max\_deg})$.
- Degrees of Separation: $O(V + E)$ via BFS.
- Social Clusters: $O(V + E)$.

### Real-Life Applications
- Social media platforms (LinkedIn connections, Facebook friend suggestions).
- Epidemic contact tracing and viral marketing network analysis.

---

## 12. Experiment 8: Maze Solver

### Problem Statement
Model a 2D grid maze as an implicit graph and find the shortest path from Start `'S'` to Destination `'E'` using BFS. Reconstruct and mark the path on the maze (`'*'`), and handle wall-blocked unreachable mazes.

### Approach
- **Grid-to-Graph Formulation**:
  - Each coordinate $(r, c)$ in the $R \times C$ grid is an implicit graph vertex.
  - Edges exist between adjacent open cells in four cardinal directions: Up $(-1, 0)$, Down $(+1, 0)$, Left $(0, -1)$, Right $(0, +1)$.
  - Wall cells `'#'` have degree 0 and are omitted from traversal.
- **Shortest Path Guarantee**: Because each orthogonal grid step represents an unweighted edge cost of 1, BFS guarantees discovering the shortest path.
- **Reconstruction**: `parent[(nr, nc)] = (r, c)` tracks discovery paths. The solution path is marked with `'*'` on the output grid.

### Complexity
- Time Complexity: $O(R \times C)$ time.
- Auxiliary Space: $O(R \times C)$ for visited set, queue, and parent map.

### Real-Life Applications
- Robotics path planning (automated warehouse vacuum/delivery robots navigating obstacles).
- Video game pathfinding (tile-based grid movement).

---

## 13. Experiment 9: Course Prerequisite Tracker

### Problem Statement
Model a university curriculum with prerequisite dependencies as a Directed Graph. Compute a valid study plan using Kahn's algorithm (Topological Sorting), detect circular prerequisite deadlocks (cycles), and identify the locked courses preventing graduation.

### Approach
- **DAG Formulation**: A directed edge $u \to v$ indicates that course $u$ must be completed before enrolling in course $v$.
- **Kahn's Algorithm (In-Degree BFS)**:
  1. Compute $\text{in\_degree}[v]$ for all vertices (number of incoming prerequisite edges).
  2. Enqueue all vertices with $\text{in\_degree} == 0$ into a manual FIFO queue (courses with zero prerequisites taken in Semester 1).
  3. While queue is not empty:
     - Dequeue course $u$ and append to schedule.
     - For each course $v$ dependent on $u$ ($u \to v$):
       - Decrement $\text{in\_degree}[v]$ by 1.
       - If $\text{in\_degree}[v]$ reaches 0, enqueue $v$.
- **Cycle Detection**: If the count of scheduled courses is $< |V|$, a circular prerequisite cycle exists ($A \to B \to C \to A$), and courses with $\text{in\_degree} > 0$ are reported as trapped in deadlock.

### Complexity
- Time Complexity: $O(V + E)$ time.
- Auxiliary Space: $O(V)$ for in-degree table and queue.

### Real-Life Applications
- Build automation systems (Makefile, Gradle, Bazel compiling dependent libraries in correct sequence).
- Package managers (APT, NPM, Pip resolving dependent packages without dependency cycles).

---

## 14. Graph Representation Comparison

| Feature / Metric | Adjacency Matrix | Adjacency List |
|:---|:---:|:---:|
| **Storage Structure** | 2D Array $|V| \times |V|$ | Map / Array of Linked / Dynamic Lists |
| **Space Complexity** | $\Theta(V^2)$ (Fixed) | $\Theta(V + E)$ (Optimal for sparse graphs) |
| **Edge Existence Test $(u, v)$** | $\mathbf{O(1)}$ (Instant matrix indexing) | $O(\text{deg}(u))$ (List scan) |
| **Add Edge $(u, v)$** | $O(1)$ | $O(1)$ |
| **Remove Edge $(u, v)$** | $O(1)$ | $O(\text{deg}(u))$ |
| **Iterate All Neighbors of $u$** | $O(V)$ (Must scan entire row) | $\mathbf{O(\text{deg}(u))}$ (Scan only actual edges) |
| **Sparse Graph Memory Efficiency**| Very Poor (mostly zeros) | **Excellent** |
| **Dense Graph Memory Efficiency** | Excellent (compact bits) | Slightly higher constant pointer overhead |
| **Dynamic Vertex Add/Remove** | Expensive ($O(V^2)$ matrix resizing) | Easy and dynamic |

---

## 15. BFS and DFS Comparison

| Traversal Strategy | Breadth-First Search (BFS) | Depth-First Search (DFS) |
|:---|:---:|:---:|
| **Underlying Data Structure** | **FIFO Queue** | **LIFO Stack** (Call stack or explicit stack) |
| **Exploration Direction** | Wide / Level-by-level | Deep along a single branch before backtracking |
| **Shortest Path (Unweighted)** | **Guaranteed shortest path** | Does **not** guarantee shortest path |
| **Space Complexity** | $O(V)$ (Proportional to tree width) | $O(V)$ (Proportional to tree depth) |
| **Best Used For** | Shortest path, degrees of separation, peer-to-peer discovery | Topological sort, cycle detection, strongly connected components, maze exploration |
| **Cycle Detection** | Possible (cross edges) | Natural and standard (back edges) |

---

## 16. Dijkstra Algorithm Explanation

### The Greedy Principle
Dijkstra's algorithm solves Single-Source Shortest Paths by maintaining a set of settled vertices whose shortest distance from source $s$ is permanently known. At each step, it greedily selects the unsettled vertex $u$ with the minimum tentative distance $\text{dist}[u]$.

```text
Initialize dist[s] = 0, dist[v] = infinity for all v != s
Insert (0, s) into Min-Heap Priority Queue

While Priority Queue is not empty:
    Extract (curr_dist, u) with minimum distance
    If u already finalized, continue
    Mark u as finalized

    For each neighbor v of u with edge weight w(u, v):
        If dist[u] + w(u, v) < dist[v]:
            dist[v] = dist[u] + w(u, v)
            predecessor[v] = u
            Insert (dist[v], v) into Priority Queue
```

### Why Dijkstra Fails on Negative Edge Weights
Consider three vertices $A \xrightarrow{2} B$, $A \xrightarrow{5} C$, and $B \xrightarrow{-4} C$:
1. From source $A$: $\text{dist}[A]=0, \text{dist}[B]=2, \text{dist}[C]=5$.
2. Dijkstra extracts $B$ (distance 2), and relaxes $C$: $\text{dist}[C] = \min(5, 2 + (-4)) = -2$.
3. However, if $C$ had already been extracted and settled before discovering the negative edge through $B$, Dijkstra would never re-examine $C$, leaving its distance incorrect.
4. If a negative cycle exists, distances can decrease infinitely, causing loops.
5. Therefore, Dijkstra **strictly requires non-negative edge weights** ($w(u, v) \ge 0$). Graphs with negative weights require the **Bellman-Ford algorithm** ($O(V \cdot E)$).

---

## 17. Topological Sorting and Cycle Detection

### Formal Definition
A **Topological Sort** of a directed graph $G = (V, E)$ is a linear ordering of all vertices such that:
$$\forall (u, v) \in E, \quad u \text{ appears before } v \text{ in the ordering}$$

### Kahn's Algorithm Step-by-Step
1. Compute in-degree $\text{deg}^-(v)$ for every vertex $v \in V$.
2. Find all source vertices ($\text{deg}^-(v) == 0$) and enqueue them into a FIFO queue.
3. While queue is non-empty:
   - Dequeue $u$, append $u$ to result list.
   - For each outgoing edge $u \to v$:
     - Decrement $\text{deg}^-(v)$ by 1.
     - If $\text{deg}^-(v) == 0$, enqueue $v$.
4. **Cycle Invariant**:
   - If $|\text{result}| == |V|$: The graph is a **DAG**, and `result` is a valid topological ordering.
   - If $|\text{result}| < |V|$: The graph contains at least one **directed cycle**. The vertices remaining with $\text{deg}^-(v) > 0$ are locked in circular dependency deadlocks.

---

## 18. Time and Space Complexity Analysis

| Program | Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
|:---|:---|:---:|:---:|:---:|:---:|
| **Program 1: Adjacency Matrix** | Edge Lookup / Add / Remove | $\Theta(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| | Neighbor Iteration | $\Theta(V)$ | $\Theta(V)$ | $O(V)$ | $O(1)$ |
| | Matrix Storage | $\Theta(V^2)$ | $\Theta(V^2)$ | $O(V^2)$ | $O(V^2)$ |
| **Program 2: Adjacency List** | Add / Remove Edge | $\Theta(1)$ | $\Theta(\text{deg}(u))$ | $O(\text{deg}(u))$ | $O(1)$ |
| | Neighbor Iteration | $\Theta(1)$ | $\Theta(\text{deg}(u))$ | $O(\text{deg}(u))$ | $O(1)$ |
| | Graph Storage | $\Theta(V + E)$ | $\Theta(V + E)$ | $O(V + E)$ | $O(V + E)$ |
| **Program 3: Breadth-First Search** | Single-Source BFS | $\Theta(V + E)$ | $\Theta(V + E)$ | $O(V + E)$ | $O(V)$ |
| | Shortest Unweighted Path | $\Theta(1)$ | $\Theta(V + E)$ | $O(V + E)$ | $O(V)$ |
| **Program 4: Recursive DFS** | Traversal | $\Theta(V + E)$ | $\Theta(V + E)$ | $O(V + E)$ | $O(V)$ (Call stack) |
| **Program 5: Iterative DFS** | Traversal | $\Theta(V + E)$ | $\Theta(V + E)$ | $O(V + E)$ | $O(V)$ (Explicit stack) |
| **Program 6: Dijkstra's Algorithm** | Single-Source Shortest Path | $\Theta(V \log V)$ | $\Theta((V + E) \log V)$ | $O((V + E) \log V)$ | $O(V)$ |
| **Program 7: Social Network** | Friends of Friends (FoF) | $\Theta(1)$ | $\Theta(\text{deg}^2)$ | $O(V)$ | $O(V)$ |
| | Connected Components | $\Theta(V + E)$ | $\Theta(V + E)$ | $O(V + E)$ | $O(V)$ |
| **Program 8: Maze Solver** | BFS Grid Navigation | $\Theta(1)$ | $\Theta(R \times C)$ | $O(R \times C)$ | $O(R \times C)$ |
| **Program 9: Course Prerequisites**| Kahn's Topological Sort | $\Theta(V + E)$ | $\Theta(V + E)$ | $O(V + E)$ | $O(V)$ |

---

## 19. Testing and Sample I/O

All nine programs include comprehensive unit test suites triggered via the `--test` CLI flag.

### Automated Test Suite Execution Transcript
```console
$ python3 Lab07-Graphs/Program01-AdjacencyMatrix/adjacency_matrix.py --test && \
  python3 Lab07-Graphs/Program02-AdjacencyList/adjacency_list.py --test && \
  python3 Lab07-Graphs/Program03-BFS/bfs.py --test && \
  python3 Lab07-Graphs/Program04-RecursiveDFS/recursive_dfs.py --test && \
  python3 Lab07-Graphs/Program05-IterativeDFS/iterative_dfs.py --test && \
  python3 Lab07-Graphs/Program06-Dijkstra/dijkstra.py --test && \
  python3 Lab07-Graphs/Program07-SocialNetwork/social_network.py --test && \
  python3 Lab07-Graphs/Program08-MazeSolver/maze_solver.py --test && \
  python3 Lab07-Graphs/Program09-CoursePrerequisites/course_prerequisites.py --test

======================================================================
RUNNING AUTOMATED TEST SUITE: Graph Adjacency Matrix
======================================================================
[PASS] Test 1: Undirected graph construction and symmetry verified.
[PASS] Test 2: Edge removal verified.
[PASS] Test 3: Directed graph asymmetry verified.
[PASS] Test 4: Self-loop handling verified.
[PASS] Test 5: Vertex boundary validation verified.
ALL 5 TEST CASES PASSED SUCCESSFULLY!

======================================================================
RUNNING AUTOMATED TEST SUITE: Graph Adjacency List
======================================================================
[PASS] Test 1: Undirected graph construction and symmetry verified.
[PASS] Test 2: Duplicate edge prevention and weight update verified.
[PASS] Test 3: Edge removal verified.
[PASS] Test 4: Directed graph asymmetry verified.
[PASS] Test 5: Vertex removal and incident edge cleanup verified.
ALL 5 TEST CASES PASSED SUCCESSFULLY!

======================================================================
RUNNING AUTOMATED TEST SUITE: Breadth-First Search (BFS)
======================================================================
[PASS] Test 1: Single-source BFS traversal verified -> [0, 1, 2, 3]
[PASS] Test 2: Disconnected components discovered -> [[0, 1, 2, 3], [4, 5]]
[PASS] Test 3: Shortest path 0 -> 3 verified -> [0, 1, 3]
[PASS] Test 4: Unreachable destination correctly returned None.
[PASS] Test 5: Same source and destination handled -> [2].
ALL 5 TEST CASES PASSED SUCCESSFULLY!

======================================================================
RUNNING AUTOMATED TEST SUITE: Recursive Depth-First Search (DFS)
======================================================================
[PASS] Test 1: Single-source recursive DFS verified -> [0, 1, 2, 3]
[PASS] Test 2: Recursive DFS from leaf vertex 3 verified -> [3, 1, 0, 2]
[PASS] Test 3: Disconnected components discovered -> [[0, 1, 2, 3], [4, 5]]
[PASS] Test 4: Single isolated vertex traversal verified.
[PASS] Test 5: Missing vertex exception handling verified.
ALL 5 TEST CASES PASSED SUCCESSFULLY!

======================================================================
RUNNING AUTOMATED TEST SUITE: Iterative Depth-First Search (DFS)
======================================================================
[PASS] Test 1: Iterative DFS verified -> [0, 1, 2, 3]
[PASS] Test 2: Iterative DFS from vertex 3 verified -> [3, 1, 0, 2]
[PASS] Test 3: Full iterative DFS across disconnected components verified -> [[0, 1, 2, 3], [4, 5]]
[PASS] Test 4: Missing vertex exception handling verified.
ALL 4 TEST CASES PASSED SUCCESSFULLY!

======================================================================
RUNNING AUTOMATED TEST SUITE: Weighted Graph & Dijkstra
======================================================================
[PASS] Test 1: Shortest distances verified -> {'A': 0.0, 'B': 4.0, 'D': 2.0, 'C': 5.0, 'E': 5.0, 'Z': inf}
[PASS] Test 2: Shortest path A -> C verified -> ['A', 'B', 'C'] (dist: 5.0)
[PASS] Test 3: Unreachable vertex 'Z' correctly reported as inf.
[PASS] Test 4: Negative edge weight rejection verified.
[PASS] Test 5: Undirected multi-path Dijkstra verified -> [1, 3, 6, 5] (dist: 20.0)
ALL 5 TEST CASES PASSED SUCCESSFULLY!

======================================================================
RUNNING AUTOMATED TEST SUITE: Social Network Graph
======================================================================
[PASS] Test 1: Immediate friends of Alice verified -> ['bob', 'eve']
[PASS] Test 2: Friends of Friends recommendation verified -> ['charlie']
[PASS] Test 3: Degrees of separation path verified -> ['alice', 'bob', 'charlie', 'david']
[PASS] Test 4: Disconnected users correctly identified (None).
[PASS] Test 5: Social communities discovered -> ['alice', 'bob', 'eve', 'charlie', 'david'] and ['frank', 'grace']
[PASS] Test 6: Friendship removal verified.
ALL 6 TEST CASES PASSED SUCCESSFULLY!

======================================================================
RUNNING AUTOMATED TEST SUITE: Maze Solver (BFS Graph Traversal)
======================================================================
[PASS] Test 1: Solvable maze verified (Found shortest path of 14 steps).
[PASS] Test 2: Unsolvable maze correctly handled (Returned None, -1).
[PASS] Test 3: Minimal direct adjacent maze verified (1 step).
[PASS] Test 4: Missing start validation caught.
ALL 4 TEST CASES PASSED SUCCESSFULLY!

======================================================================
RUNNING AUTOMATED TEST SUITE: Course Prerequisite Tracker
======================================================================
[PASS] Test 1: Valid topological schedule verified -> ['CS101', 'MATH101', 'CS102', 'MATH201', 'CS201', 'CS202', 'CS301']
[PASS] Test 2: Prerequisite cycle detected cleanly -> Locked courses: ['CS101', 'CS102', 'CS103']
[PASS] Test 3: Self-prerequisite rejection verified.
ALL 3 TEST CASES PASSED SUCCESSFULLY!
```

---

## 20. Real-Life Applications

1. **Routing and GPS Navigation**: Dijkstra's algorithm powers Google Maps, Apple Maps, and autonomous vehicle route planning over road network graphs.
2. **Social Media Recommendations**: Adjacency lists model social graphs on platforms like LinkedIn and Instagram to suggest 2nd-degree mutual connections and identify community clusters.
3. **Build Engines and Package Managers**: Kahn's algorithm performs topological sorting in tools like Linux APT, NPM, Webpack, and Makefiles to resolve software build dependencies and detect circular import errors.
4. **Autonomous Robotics and Gaming**: Grid-to-graph BFS and $A^*$ pathfinding guide game characters and robotic vacuum cleaners through physical mazes.
5. **Computer Networks**: OSPF (Open Shortest Path First) protocol uses Dijkstra's algorithm inside network routers to forward packets along the lowest-latency fiber-optic paths.

---

## 21. Folder Structure

```text
Lab07-Graphs/
├── Program01-AdjacencyMatrix/
│   └── adjacency_matrix.py
├── Program02-AdjacencyList/
│   └── adjacency_list.py
├── Program03-BFS/
│   └── bfs.py
├── Program04-RecursiveDFS/
│   └── recursive_dfs.py
├── Program05-IterativeDFS/
│   └── iterative_dfs.py
├── Program06-Dijkstra/
│   └── dijkstra.py
├── Program07-SocialNetwork/
│   └── social_network.py
├── Program08-MazeSolver/
│   └── maze_solver.py
├── Program09-CoursePrerequisites/
│   └── course_prerequisites.py
├── README.md
└── reflection.md
```

---

## 22. Execution Instructions

Every program is completely self-contained and executable in two modes: an **interactive CLI menu mode** and an **automated test mode** via `--test`.

### 1. Interactive CLI Mode
```bash
python3 Lab07-Graphs/Program01-AdjacencyMatrix/adjacency_matrix.py
python3 Lab07-Graphs/Program02-AdjacencyList/adjacency_list.py
python3 Lab07-Graphs/Program03-BFS/bfs.py
python3 Lab07-Graphs/Program04-RecursiveDFS/recursive_dfs.py
python3 Lab07-Graphs/Program05-IterativeDFS/iterative_dfs.py
python3 Lab07-Graphs/Program06-Dijkstra/dijkstra.py
python3 Lab07-Graphs/Program07-SocialNetwork/social_network.py
python3 Lab07-Graphs/Program08-MazeSolver/maze_solver.py
python3 Lab07-Graphs/Program09-CoursePrerequisites/course_prerequisites.py
```

### 2. Automated Test Verification Mode
```bash
python3 Lab07-Graphs/Program01-AdjacencyMatrix/adjacency_matrix.py --test
python3 Lab07-Graphs/Program02-AdjacencyList/adjacency_list.py --test
python3 Lab07-Graphs/Program03-BFS/bfs.py --test
python3 Lab07-Graphs/Program04-RecursiveDFS/recursive_dfs.py --test
python3 Lab07-Graphs/Program05-IterativeDFS/iterative_dfs.py --test
python3 Lab07-Graphs/Program06-Dijkstra/dijkstra.py --test
python3 Lab07-Graphs/Program07-SocialNetwork/social_network.py --test
python3 Lab07-Graphs/Program08-MazeSolver/maze_solver.py --test
python3 Lab07-Graphs/Program09-CoursePrerequisites/course_prerequisites.py --test
```

---

## 23. Learning Outcomes

By completing Unit 7, students have achieved:
1. **Graph Representation Fluency**: Deep understanding of Adjacency Matrix ($O(V^2)$) vs Adjacency List ($O(V + E)$) representations, density trade-offs, and memory implications.
2. **Traversal Mastery**: Fluency in Breadth-First Search (FIFO queue) and Depth-First Search (call stack vs explicit stack), including disconnected component discovery.
3. **Single-Source Shortest Paths**: Competence in implementing Dijkstra's algorithm from first principles with custom binary min-heaps, understanding the relaxation invariant, and grasping the mathematical failure modes of negative edge weights.
4. **Relational & Spatial Modeling**: Ability to formulate practical real-world problems as graphs: social networks (FoF recommendations, degrees of separation), 2D mazes (implicit grid graphs), and academic curricula.
5. **DAGs and Topological Sort**: Practical implementation of Kahn's in-degree BFS algorithm, understanding partial orderings, and detecting circular deadlocks.

---

## 24. References

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press. Chapter 20: Elementary Graph Algorithms (BFS, DFS, Topological Sort), Chapter 22: Single-Source Shortest Paths (Dijkstra's Algorithm).
2. Dijkstra, E. W. (1959). *A note on two problems in connexion with graphs*. Numerische Mathematik, 1(1): 269–271.
3. Kahn, A. B. (1962). *Topological sorting of large networks*. Communications of the ACM, 5(11): 558–562.
4. Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2013). *Data Structures and Algorithms in Python*. John Wiley & Sons. Chapter 14: Graph Algorithms.

