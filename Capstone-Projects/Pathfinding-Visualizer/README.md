# PATHFINDING VISUALIZER
### A Graph-Based Pathfinding and Shortest Path Analysis System

**Course:** IC-307D: Data Structures and Algorithms Laboratory  
**Category:** Capstone Mini-Project  
**Environment:** Python 3.8+ (Python Standard Library & Tkinter Only — Zero External Dependencies)  

---

## 1. Project Overview

The **Pathfinding Visualizer** is a graph-theoretic simulation and benchmarking application developed to demonstrate the core principles of graph traversal and single-source shortest path algorithms. 

It provides both a **modern graphical desktop application (Tkinter)** and an **interactive terminal interface (CLI)**. Operating on a 2D grid modeled as an implicit planar graph, this project illustrates how foundational data structures—**Queues**, **Stacks**, and **Binary Min-Heaps**—directly dictate traversal wavefronts, space-time complexities, and optimality guarantees across:
1. **Breadth-First Search (BFS)**
2. **Depth-First Search (DFS)**
3. **Dijkstra's Shortest Path Algorithm**

All core data structures and algorithms are implemented **strictly from first principles** without relying on standard library shortcut containers such as `collections.deque`, `queue.PriorityQueue`, `heapq`, or graph frameworks like `NetworkX`.

---

## 2. Directory Structure

```text
Capstone-Projects/
└── Pathfinding-Visualizer/
    ├── gui.py                         # Modern Dark-Themed Tkinter GUI & AnimationController
    ├── pathfinding_visualizer.py      # Core data structures, graph algorithms & Terminal CLI
    ├── README.md                      # Comprehensive technical and algorithmic documentation
    ├── reflection.md                  # Theoretical reflection, design tradeoffs & empirical analysis
    └── tests/
        ├── test_pathfinding.py        # Automated test suite for core data structures & algorithms
        └── test_gui.py                # Automated tests for GUI, controller states & maze generation
```

---

## 3. Graphical Interface & Visual Design

The application features a modern dark-themed interface built strictly with Python's standard `tkinter` library.

### 3.1 Color Palette & Visual Coding

| State | Color | Hex Code | Visual Indicator |
| :--- | :--- | :---: | :--- |
| **Empty Terrain** | Dark Charcoal Base | `#1e1e2e` | Open passable cell with subtle border (`#26283b`) |
| **Start Node** | Emerald Green | `#2ecc71` | Distinct green cell marked with white **S** |
| **Destination Node** | Coral Red | `#e74c3c` | Distinct red cell marked with white **E** |
| **Wall / Obstacle** | Slate Charcoal | `#585b70` | Solid barrier blocking traversal |
| **Currently Exploring** | Amber Gold | `#f1c40f` | Active node popped from frontier and being inspected |
| **Visited / Explored** | Luminous Dodger Blue | `#3498db` | Cell closed and added to explored set |
| **Final Reconstructed Path** | Electric Cyan | `#00ffff` | Optimal / valid path trace from Start to Destination |

### 3.2 Layout Components
1. **Header Banner:** Displays project title, academic course badges, and architectural attributes.
2. **Left Control Sidebar:**
   - **Algorithm Selector:** Radio buttons with descriptions for BFS, DFS, and Dijkstra.
   - **Execution Controls:** `START VISUALIZATION`, `PAUSE`, `RESUME`, `RESET VISUALIZATION`, `CLEAR WALLS`, `MAZE`.
   - **Mouse Tool Selector:** Explicit buttons for *Draw Wall*, *Erase*, *Move Start (S)*, *Move End (E)*.
   - **Animation Speed Slider:** Dynamically updates step delay from $1\text{ ms}$ (instantaneous/batched) to $100\text{ ms}$ (slow deliberate inspection).
   - **Live Statistics Panel:** Real-time updates for *Status*, *Nodes Explored*, *Path Length*, *Traversal Cost*, and *Pure Compute Time*.
   - **Legend Card:** Instant color reference guide.
3. **Central Interactive Grid (Canvas):** High-performance Tkinter `Canvas` with cached element IDs for $O(1)$ cell color updates during animation. Dynamically adapts cell geometry to window resizing.
4. **Bottom Status Bar:** Shows live coordinate tracking `[Cell (r, c)]` and interaction hints.

---

## 4. Interactive Grid Features

- **Click & Drag Walls:** Left-click and drag across any empty cells to draw impassable barriers.
- **Erase Walls:** Right-click and drag (or Shift + Left-click drag) to delete walls.
- **Relocate Start & Destination:** Click and drag the **S** or **E** nodes directly to any new valid location on the grid.
- **Procedural Maze Generation:** Click the **MAZE** button to generate a structured braided labyrinth with loop openings via randomized depth-first search.
- **Collision Protection:** Start and Destination coordinates are strictly protected from being overwritten by wall drawing.
- **Concurrency Protection:** Incompatible controls and grid editing are automatically disabled while an algorithm is actively running.

---

## 5. Non-Blocking Real-Time Animation Architecture

Animation is governed by an independent `AnimationController` utilizing Tkinter's event-driven `widget.after()` scheduler:

- **No `time.sleep()`:** The GUI event loop is never blocked, ensuring full UI responsiveness, smooth window resizing, and instant hover feedback during execution.
- **Two-Phase Animation:**
  1. *Exploration Phase:* Progressively illuminates explored cells in Dodger Blue (`#3498db`), actively highlighting the current inspection vertex in Gold (`#f1c40f`) and updating the live "Nodes Explored" counter.
  2. *Path Phase:* Backtracks the parent predecessor mapping and sequentially paints the reconstructed path in Electric Cyan (`#00ffff`), updating the live "Path Length" counter.
- **Full Playback Control:**
  - **Pause:** Halts animation immediately without losing the current exploration wavefront.
  - **Resume:** Continues step-by-step traversal from the exact paused index.
  - **Reset:** Clears explored and path cells, restoring the grid to its pre-run state while preserving walls and endpoints.

---

## 6. Graph Algorithms & Complexities

All algorithms are implemented manually in `pathfinding_visualizer.py`:

| Algorithm | Underlying Data Structure | Frontier Extraction | Space Complexity | Time Complexity | Optimality Guarantee |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Breadth-First Search (BFS)** | Manual Linked FIFO `Queue` | $O(1)$ | $O(V)$ | $O(V + E)$ | **Guaranteed Shortest Path** in unweighted graphs (minimal edge count) |
| **Depth-First Search (DFS)** | Manual Linked LIFO `Stack` | $O(1)$ | $O(V)$ | $O(V + E)$ | **Valid Path** (non-optimal, susceptible to winding routes) |
| **Dijkstra's Algorithm** | Manual Binary `MinHeap` | $O(\log V)$ | $O(V)$ | $O((V + E) \log V)$ | **Provably Optimal Path** on non-negative weighted graphs (matches BFS on $w=1$) |

> **Note on Performance Measurement:** Execution times displayed in the Statistics panel are captured using Python's high-resolution `time.perf_counter()` strictly around the algorithmic graph search. This represents true computational CPU time and excludes GUI animation rendering latency.

---

## 7. How to Launch and Use

### 7.1 Graphical Desktop Application (Recommended)
```bash
python3 Capstone-Projects/Pathfinding-Visualizer/gui.py
```
Or simply:
```bash
python3 Capstone-Projects/Pathfinding-Visualizer/pathfinding_visualizer.py
```
*(The main entrypoint detects the graphical environment and automatically launches the Tkinter GUI).*

### 7.2 Terminal CLI Interface
For headless or pure terminal environments:
```bash
python3 Capstone-Projects/Pathfinding-Visualizer/pathfinding_visualizer.py --cli
```

---

## 8. Automated Testing Suite

All features are covered by automated unit tests using Python's built-in `unittest` module.

```bash
python3 -m unittest discover -s Capstone-Projects/Pathfinding-Visualizer/tests -p "test_*.py" -v
```

### Test Coverage (38 Tests Passing):
- **Core Algorithms & Data Structures (`test_pathfinding.py`):**
  - FIFO Queue enqueue/dequeue order, peek, and underflow error handling.
  - LIFO Stack push/pop order, peek, and underflow error handling.
  - Binary Min-Heap ordering, heap property, tie-breaker counter stability, and underflow error handling.
  - BFS shortest path optimality on unweighted grids.
  - DFS valid path reachability and contiguous step verification.
  - Dijkstra path optimality on weighted graphs (taking a lower-cost detour over a higher-cost direct path).
  - Equivalence of BFS and Dijkstra path length on unweighted grids.
  - Obstacle navigation and complete obstacle enclosure (unreachable goal).
  - Start identical to Destination edge cases.
  - Out-of-bounds coordinate rejection.
  - Independent multi-algorithm comparison benchmarking.
- **GUI & Animation Controller (`test_gui.py`):**
  - Controller state machine (`IDLE` $\rightarrow$ `RUNNING` $\rightarrow$ `PAUSED` $\rightarrow$ `COMPLETED`).
  - Step-by-step callback invocation for nodes explored and final path.
  - Pause and Resume continuity without state loss.
  - Reset termination and timer cancellation.
  - Procedural braided maze generation (preserves Start and Destination).
  - Tkinter GUI instantiation, widget lifecycle, and tool switching.
