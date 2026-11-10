#!/usr/bin/env python3
"""
================================================================================
PATHFINDING VISUALIZER
A Graph-Based Pathfinding and Shortest Path Analysis System
================================================================================
Course: Data Structures and Algorithms Laboratory (IC-307D)
Language: Python 3.8+ (Standard Library Only)
Zero External Dependencies: collections.deque, heapq, and NetworkX are NOT used.
All foundational data structures (Queue, Stack, Binary Min-Heap) are implemented
manually from first principles.
================================================================================
"""

import math
import os
import random
import sys
import time
from typing import Any, Callable, Dict, Generator, List, Optional, Set, Tuple


# ==============================================================================
# 1. MANUAL DATA STRUCTURES
# ==============================================================================

class QueueNode:
    """A singly-linked node used in the manual FIFO Queue."""

    def __init__(self, data: Any, next_node: Optional["QueueNode"] = None) -> None:
        self.data: Any = data
        self.next: Optional["QueueNode"] = next_node


class Queue:
    """
    Manually implemented First-In, First-Out (FIFO) Queue.
    
    Theoretical Background:
      - Enqueue operation appends to the rear in O(1) time.
      - Dequeue operation removes from the front in O(1) time.
      - Guarantees breadth-first (level-by-level) exploration in unweighted graphs.
    """

    def __init__(self) -> None:
        self._front: Optional[QueueNode] = None
        self._rear: Optional[QueueNode] = None
        self._size: int = 0

    def enqueue(self, item: Any) -> None:
        """Add an item to the rear of the queue."""
        new_node = QueueNode(item)
        if self._rear is None:
            self._front = self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node
        self._size += 1

    def dequeue(self) -> Any:
        """
        Remove and return the front item from the queue.
        Raises IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError("dequeue from an empty Queue")
        assert self._front is not None
        removed_data = self._front.data
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return removed_data

    def peek(self) -> Any:
        """Return the front item without removing it."""
        if self.is_empty():
            raise IndexError("peek into an empty Queue")
        assert self._front is not None
        return self._front.data

    def is_empty(self) -> bool:
        """Check whether the queue contains any items."""
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __repr__(self) -> str:
        items = []
        curr = self._front
        while curr:
            items.append(repr(curr.data))
            curr = curr.next
        return f"Queue([{', '.join(items)}])"


class StackNode:
    """A singly-linked node used in the manual LIFO Stack."""

    def __init__(self, data: Any, next_node: Optional["StackNode"] = None) -> None:
        self.data: Any = data
        self.next: Optional["StackNode"] = next_node


class Stack:
    """
    Manually implemented Last-In, First-Out (LIFO) Stack.
    
    Theoretical Background:
      - Push operation prepends to the top in O(1) time.
      - Pop operation removes from the top in O(1) time.
      - Backtracking property powers Depth-First Search (DFS).
    """

    def __init__(self) -> None:
        self._top: Optional[StackNode] = None
        self._size: int = 0

    def push(self, item: Any) -> None:
        """Push an item onto the top of the stack."""
        self._top = StackNode(item, self._top)
        self._size += 1

    def pop(self) -> Any:
        """
        Remove and return the top item from the stack.
        Raises IndexError if the stack is empty.
        """
        if self.is_empty():
            raise IndexError("pop from an empty Stack")
        assert self._top is not None
        removed_data = self._top.data
        self._top = self._top.next
        self._size -= 1
        return removed_data

    def peek(self) -> Any:
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("peek into an empty Stack")
        assert self._top is not None
        return self._top.data

    def is_empty(self) -> bool:
        """Check whether the stack contains any items."""
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __repr__(self) -> str:
        items = []
        curr = self._top
        while curr:
            items.append(repr(curr.data))
            curr = curr.next
        return f"Stack([{', '.join(items)}])"


class MinHeap:
    """
    Manually implemented Binary Min-Heap Priority Queue.
    
    Theoretical Background:
      - Complete binary tree maintained inside a contiguous dynamic array.
      - Parent-child indices for node at index i:
          Parent(i)      = (i - 1) // 2
          LeftChild(i)   = 2 * i + 1
          RightChild(i)  = 2 * i + 2
      - Heap Property: Every node is less than or equal to its children.
      - Push (Insertion): Appended at bottom, sifted up in O(log N) time.
      - Pop (Extraction of Minimum): Root replaced by last item, sifted down in O(log N) time.
      - Tie-breaker counter guarantees strict order consistency and avoids
        comparing non-comparable payload objects.
    """

    def __init__(self) -> None:
        # Each entry is a tuple: (priority, insertion_order, item)
        self._heap: List[Tuple[float, int, Any]] = []
        self._counter: int = 0

    def push(self, priority: float, item: Any) -> None:
        """Insert an item with an associated numeric priority into the min-heap."""
        entry = (priority, self._counter, item)
        self._counter += 1
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)

    def pop(self) -> Tuple[float, Any]:
        """
        Extract and return the item with the minimum priority as (priority, item).
        Raises IndexError if the heap is empty.
        """
        if self.is_empty():
            raise IndexError("pop from an empty MinHeap")

        # Swap root with last element
        self._swap(0, len(self._heap) - 1)
        min_entry = self._heap.pop()

        if self._heap:
            self._sift_down(0)

        return min_entry[0], min_entry[2]

    def peek(self) -> Tuple[float, Any]:
        """Return the minimum (priority, item) without removing it."""
        if self.is_empty():
            raise IndexError("peek into an empty MinHeap")
        min_entry = self._heap[0]
        return min_entry[0], min_entry[2]

    def is_empty(self) -> bool:
        """Check whether the heap is empty."""
        return len(self._heap) == 0

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return not self.is_empty()

    def _swap(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            # Compare (priority, counter)
            if self._heap[idx] < self._heap[parent]:
                self._swap(idx, parent)
                idx = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        size = len(self._heap)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx

            if left < size and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < size and self._heap[right] < self._heap[smallest]:
                smallest = right

            if smallest != idx:
                self._swap(idx, smallest)
                idx = smallest
            else:
                break


# ==============================================================================
# 2. GRID REPRESENTATION
# ==============================================================================

class Grid:
    """
    Two-dimensional Grid representing an unweighted or weighted pathfinding map.
    
    Coordinates are represented as (row, col) tuples with 0-based indexing:
      row in [0, rows - 1], col in [0, cols - 1].
      
    Movement Rules:
      Four cardinal directions:
        Up:    (-1,  0)
        Down:  ( 1,  0)
        Left:  ( 0, -1)
        Right: ( 0,  1)
    """

    EMPTY: str = "."
    START: str = "S"
    DEST: str = "E"
    OBSTACLE: str = "#"
    VISITED: str = "V"
    PATH: str = "*"

    # Movement vectors: Up, Down, Left, Right
    DIRECTIONS: List[Tuple[int, int]] = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1),   # Right
    ]

    def __init__(self, rows: int = 10, cols: int = 20) -> None:
        if rows < 1 or cols < 1:
            raise ValueError("Grid dimensions must be at least 1x1")
        self.rows: int = rows
        self.cols: int = cols
        self.start: Optional[Tuple[int, int]] = (0, 0)
        self.destination: Optional[Tuple[int, int]] = (rows - 1, cols - 1)
        self.obstacles: Set[Tuple[int, int]] = set()
        # Non-negative cell traversal costs (default = 1.0)
        self.weights: Dict[Tuple[int, int], float] = {}

    def in_bounds(self, r: int, c: int) -> bool:
        """Check if (r, c) lies strictly within the grid boundaries."""
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_obstacle(self, r: int, c: int) -> bool:
        """Check if (r, c) is an obstacle."""
        return (r, c) in self.obstacles

    def is_passable(self, r: int, c: int) -> bool:
        """Check if (r, c) is inside bounds and not an obstacle."""
        return self.in_bounds(r, c) and not self.is_obstacle(r, c)

    def set_start(self, r: int, c: int) -> Tuple[bool, str]:
        """Set the start coordinate after validating bounds and collisions."""
        if not self.in_bounds(r, c):
            return False, f"Coordinate ({r}, {c}) is outside the grid bounds."
        if (r, c) in self.obstacles:
            return False, f"Coordinate ({r}, {c}) is an obstacle."
        if (r, c) == self.destination:
            return False, "Start coordinate cannot be identical to destination."
        self.start = (r, c)
        return True, "Start position updated successfully."

    def set_destination(self, r: int, c: int) -> Tuple[bool, str]:
        """Set the destination coordinate after validating bounds and collisions."""
        if not self.in_bounds(r, c):
            return False, f"Coordinate ({r}, {c}) is outside the grid bounds."
        if (r, c) in self.obstacles:
            return False, f"Coordinate ({r}, {c}) is an obstacle."
        if (r, c) == self.start:
            return False, "Destination coordinate cannot be identical to start."
        self.destination = (r, c)
        return True, "Destination position updated successfully."

    def add_obstacle(self, r: int, c: int) -> Tuple[bool, str]:
        """Add an obstacle cell."""
        if not self.in_bounds(r, c):
            return False, f"Coordinate ({r}, {c}) is outside the grid bounds."
        if (r, c) == self.start:
            return False, "Cannot place obstacle on top of Start position."
        if (r, c) == self.destination:
            return False, "Cannot place obstacle on top of Destination position."
        self.obstacles.add((r, c))
        return True, f"Obstacle added at ({r}, {c})."

    def remove_obstacle(self, r: int, c: int) -> Tuple[bool, str]:
        """Remove an obstacle cell."""
        if not self.in_bounds(r, c):
            return False, f"Coordinate ({r}, {c}) is outside the grid bounds."
        if (r, c) in self.obstacles:
            self.obstacles.remove((r, c))
            return True, f"Obstacle removed from ({r}, {c})."
        return False, f"No obstacle exists at ({r}, {c})."

    def clear_obstacles(self) -> None:
        """Remove all obstacles from the grid."""
        self.obstacles.clear()

    def set_weight(self, r: int, c: int, weight: float) -> Tuple[bool, str]:
        """Set a non-negative traversal cost for entering cell (r, c)."""
        if not self.in_bounds(r, c):
            return False, f"Coordinate ({r}, {c}) is outside the grid bounds."
        if weight < 0:
            return False, "Weight must be non-negative."
        if (r, c) in self.obstacles:
            return False, "Cannot assign weight to an obstacle."
        self.weights[(r, c)] = float(weight)
        return True, f"Cell ({r}, {c}) weight set to {weight}."

    def get_cost(self, r: int, c: int) -> float:
        """Return the movement cost into cell (r, c). Defaults to 1.0."""
        return self.weights.get((r, c), 1.0)

    def get_neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        """
        Return the 4-connected passable neighbors of (r, c) in canonical order:
        Up, Down, Left, Right.
        """
        neighbors: List[Tuple[int, int]] = []
        for dr, dc in self.DIRECTIONS:
            nr, nc = r + dr, c + dc
            if self.is_passable(nr, nc):
                neighbors.append((nr, nc))
        return neighbors

    def reset_grid(self) -> None:
        """Reset obstacles and weights, keeping grid dimensions and default endpoints."""
        self.obstacles.clear()
        self.weights.clear()
        self.start = (0, 0)
        self.destination = (self.rows - 1, self.cols - 1)

    def clone(self) -> "Grid":
        """Create a deep clone of the grid with its obstacles and weights."""
        new_grid = Grid(self.rows, self.cols)
        new_grid.start = self.start
        new_grid.destination = self.destination
        new_grid.obstacles = set(self.obstacles)
        new_grid.weights = dict(self.weights)
        return new_grid

    def generate_maze(self, mode: str = "braided", seed: Optional[int] = None) -> None:
        """
        Procedural maze generation preserving start and destination.
        
        Modes:
          - 'braided': Carves labyrinth corridors with loop openings via randomized DFS.
          - 'scatter': Creates an obstacle field with ~28% density.
        """
        if seed is not None:
            random.seed(seed)

        self.clear_obstacles()
        s = self.start
        d = self.destination

        if mode == "scatter":
            for r in range(self.rows):
                for c in range(self.cols):
                    if (r, c) != s and (r, c) != d:
                        if random.random() < 0.28:
                            self.add_obstacle(r, c)
            return

        # Braided Labyrinth Maze
        walls: Set[Tuple[int, int]] = set()
        for r in range(self.rows):
            for c in range(self.cols):
                if r % 2 == 1 or c % 2 == 1:
                    walls.add((r, c))

        visited: Set[Tuple[int, int]] = set()
        start_r = (s[0] // 2) * 2 if s else 0
        start_c = (s[1] // 2) * 2 if s else 0
        start_cell = (start_r, start_c)

        stack = [start_cell]
        visited.add(start_cell)
        if start_cell in walls:
            walls.remove(start_cell)

        while stack:
            cr, cc = stack[-1]
            neighbors = []
            for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) not in visited:
                    wall_r = cr + dr // 2
                    wall_c = cc + dc // 2
                    neighbors.append((nr, nc, wall_r, wall_c))

            if neighbors:
                nr, nc, wr, wc = random.choice(neighbors)
                visited.add((nr, nc))
                if (wr, wc) in walls:
                    walls.remove((wr, wc))
                if (nr, nc) in walls:
                    walls.remove((nr, nc))
                stack.append((nr, nc))
            else:
                stack.pop()

        # Remove ~18% interior walls to create loops (braids)
        removable = [
            w for w in walls
            if 1 <= w[0] < self.rows - 1 and 1 <= w[1] < self.cols - 1 and random.random() < 0.18
        ]
        for w in removable:
            walls.remove(w)

        # Protect start and destination
        for p in (s, d):
            if p:
                if p in walls:
                    walls.remove(p)
                for dr, dc in self.DIRECTIONS:
                    adj = (p[0] + dr, p[1] + dc)
                    if adj in walls and random.random() < 0.5:
                        walls.remove(adj)

        for r, c in walls:
            if (r, c) != s and (r, c) != d:
                self.add_obstacle(r, c)

    def render_to_matrix(
        self,
        visited_nodes: Optional[Set[Tuple[int, int]]] = None,
        path: Optional[List[Tuple[int, int]]] = None,
        current_node: Optional[Tuple[int, int]] = None,
    ) -> List[List[str]]:
        """Compute the 2D character matrix representation of the grid."""
        matrix = [[self.EMPTY for _ in range(self.cols)] for _ in range(self.rows)]

        # Display weighted indicators if weight is customized
        for (wr, wc), w in self.weights.items():
            if self.in_bounds(wr, wc) and (wr, wc) not in self.obstacles:
                matrix[wr][wc] = str(int(w)) if w == int(w) and 1 <= w <= 9 else "~"

        # Mark obstacles
        for r, c in self.obstacles:
            if self.in_bounds(r, c):
                matrix[r][c] = self.OBSTACLE

        # Mark visited nodes
        if visited_nodes:
            for r, c in visited_nodes:
                if self.in_bounds(r, c) and matrix[r][c] not in (self.START, self.DEST, self.OBSTACLE):
                    matrix[r][c] = self.VISITED

        # Mark reconstructed path
        if path:
            for r, c in path:
                if self.in_bounds(r, c) and matrix[r][c] not in (self.START, self.DEST):
                    matrix[r][c] = self.PATH

        # Mark start and destination
        if self.start and self.in_bounds(*self.start):
            matrix[self.start[0]][self.start[1]] = self.START

        if self.destination and self.in_bounds(*self.destination):
            matrix[self.destination[0]][self.destination[1]] = self.DEST

        # Mark current node being actively explored
        if current_node and self.in_bounds(*current_node):
            if current_node != self.start and current_node != self.destination:
                matrix[current_node[0]][current_node[1]] = "@"

        return matrix

    def render(
        self,
        visited_nodes: Optional[Set[Tuple[int, int]]] = None,
        path: Optional[List[Tuple[int, int]]] = None,
        current_node: Optional[Tuple[int, int]] = None,
        use_color: bool = True,
    ) -> str:
        """Render the grid to a human-readable ASCII/ANSI-colored string."""
        matrix = self.render_to_matrix(visited_nodes, path, current_node)

        # ANSI Colors
        C_RESET = "\033[0m" if use_color else ""
        C_START = "\033[1;32m" if use_color else ""     # Bold Green
        C_DEST = "\033[1;31m" if use_color else ""      # Bold Red
        C_OBST = "\033[1;37;40m" if use_color else ""   # White on dark
        C_VISIT = "\033[36m" if use_color else ""       # Cyan
        C_PATH = "\033[1;33m" if use_color else ""      # Bold Yellow
        C_CURR = "\033[1;35m" if use_color else ""      # Bold Magenta
        C_EMPTY = "\033[90m" if use_color else ""       # Dim Gray
        C_HEADER = "\033[1;34m" if use_color else ""    # Bold Blue

        lines: List[str] = []

        # Column indices header
        col_header = "     " + "".join(f"{c % 10} " for c in range(self.cols))
        lines.append(f"{C_HEADER}{col_header}{C_RESET}")
        lines.append("    +" + "--" * self.cols + "+")

        for r in range(self.rows):
            row_str = [f"{C_HEADER}{r:2d}{C_RESET} | "]
            for c in range(self.cols):
                ch = matrix[r][c]
                if ch == self.START:
                    row_str.append(f"{C_START}S{C_RESET} ")
                elif ch == self.DEST:
                    row_str.append(f"{C_DEST}E{C_RESET} ")
                elif ch == self.OBSTACLE:
                    row_str.append(f"{C_OBST}#{C_RESET} ")
                elif ch == self.PATH:
                    row_str.append(f"{C_PATH}*{C_RESET} ")
                elif ch == "@":
                    row_str.append(f"{C_CURR}@{C_RESET} ")
                elif ch == self.VISITED:
                    row_str.append(f"{C_VISIT}v{C_RESET} ")
                elif ch == self.EMPTY:
                    row_str.append(f"{C_EMPTY}.{C_RESET} ")
                else:
                    row_str.append(f"{ch} ")
            row_str.append("|")
            lines.append("".join(row_str))

        lines.append("    +" + "--" * self.cols + "+")

        # Legend
        legend = (
            f"Legend: {C_START}S{C_RESET}=Start  "
            f"{C_DEST}E{C_RESET}=End  "
            f"{C_OBST}#{C_RESET}=Obstacle  "
            f"{C_PATH}*{C_RESET}=Final Path  "
            f"{C_VISIT}v{C_RESET}=Visited  "
            f"{C_CURR}@{C_RESET}=Exploring  "
            f"{C_EMPTY}.{C_RESET}=Empty"
        )
        lines.append(legend)

        return "\n".join(lines)


# ==============================================================================
# 3. PATHFINDING RESULT & PATH RECONSTRUCTION
# ==============================================================================

class PathResult:
    """Encapsulates the output and benchmark statistics of a pathfinding run."""

    def __init__(
        self,
        algorithm: str,
        found: bool,
        path: List[Tuple[int, int]],
        visited_count: int,
        visited_order: List[Tuple[int, int]],
        execution_time_ms: float,
        path_cost: float = 0.0,
        message: str = "",
    ) -> None:
        self.algorithm: str = algorithm
        self.found: bool = found
        self.path: List[Tuple[int, int]] = path
        # Length in edges (steps) = len(nodes) - 1 for paths with at least 1 step
        self.path_length: int = max(0, len(path) - 1) if found and path else 0
        self.visited_count: int = visited_count
        self.visited_order: List[Tuple[int, int]] = visited_order
        self.execution_time_ms: float = execution_time_ms
        self.path_cost: float = path_cost
        self.message: str = message

    def summary(self) -> str:
        status = "FOUND" if self.found else "NOT FOUND"
        return (
            f"[{self.algorithm}] Status: {status} | "
            f"Path Steps: {self.path_length} | "
            f"Total Cost: {self.path_cost:.2f} | "
            f"Visited Nodes: {self.visited_count} | "
            f"Time: {self.execution_time_ms:.4f} ms"
        )


def reconstruct_path(
    parent_map: Dict[Tuple[int, int], Optional[Tuple[int, int]]],
    start: Tuple[int, int],
    destination: Tuple[int, int],
) -> List[Tuple[int, int]]:
    """
    Backtrack from destination to start using the parent predecessor mapping.
    
    Returns:
      A list of coordinates [start, ..., destination] forming the path.
      Returns [start] if start == destination.
      Returns empty list [] if destination was never reached or unreachable.
    """
    if start == destination:
        return [start]

    if destination not in parent_map:
        return []

    path: List[Tuple[int, int]] = []
    curr: Optional[Tuple[int, int]] = destination

    while curr is not None:
        path.append(curr)
        curr = parent_map.get(curr)

    path.reverse()

    # Integrity verification: Path must begin at start and end at destination
    if path and path[0] == start and path[-1] == destination:
        return path
    return []


def calculate_path_cost(grid: Grid, path: List[Tuple[int, int]]) -> float:
    """Calculate the cumulative cost of traversing the reconstructed path."""
    if not path or len(path) <= 1:
        return 0.0
    # Cost to enter each cell following the start node
    return sum(grid.get_cost(r, c) for r, c in path[1:])


# ==============================================================================
# 4. PATHFINDING ALGORITHMS
# ==============================================================================

def bfs(
    grid: Grid,
    start: Optional[Tuple[int, int]] = None,
    destination: Optional[Tuple[int, int]] = None,
    step_callback: Optional[Callable[[Tuple[int, int], Set[Tuple[int, int]], int], None]] = None,
) -> PathResult:
    """
    Breadth-First Search (BFS) using a manual FIFO Queue.
    
    Guarantees:
      - Finds the SHORTEST path in an UNWEIGHTED grid (minimal edge count).
      - Explores vertices level-by-level in expanding concentric frontiers.
    
    Complexity:
      - Time Complexity: O(V + E) where V = rows * cols, E <= 4 * V.
      - Space Complexity: O(V) for the visited set and FIFO queue.
    """
    t_start = time.perf_counter()

    s = start if start is not None else grid.start
    d = destination if destination is not None else grid.destination

    if s is None or d is None:
        t_end = time.perf_counter()
        return PathResult("BFS", False, [], 0, [], (t_end - t_start) * 1000, 0.0, "Start or destination undefined.")

    # Validation & Edge Cases
    if not grid.in_bounds(*s) or not grid.in_bounds(*d):
        t_end = time.perf_counter()
        return PathResult("BFS", False, [], 0, [], (t_end - t_start) * 1000, 0.0, "Coordinates out of bounds.")

    if grid.is_obstacle(*s) or grid.is_obstacle(*d):
        t_end = time.perf_counter()
        return PathResult("BFS", False, [], 0, [], (t_end - t_start) * 1000, 0.0, "Start or destination is an obstacle.")

    if s == d:
        t_end = time.perf_counter()
        return PathResult("BFS", True, [s], 1, [s], (t_end - t_start) * 1000, 0.0, "Start is equal to destination.")

    queue = Queue()
    queue.enqueue(s)

    visited: Set[Tuple[int, int]] = {s}
    parent_map: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {s: None}
    visited_order: List[Tuple[int, int]] = []

    target_reached = False

    while not queue.is_empty():
        curr = queue.dequeue()
        visited_order.append(curr)

        if step_callback is not None:
            step_callback(curr, visited, len(queue))

        if curr == d:
            target_reached = True
            break

        for neighbor in grid.get_neighbors(*curr):
            if neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = curr
                queue.enqueue(neighbor)

    t_end = time.perf_counter()
    execution_time_ms = (t_end - t_start) * 1000.0

    if target_reached:
        path = reconstruct_path(parent_map, s, d)
        cost = calculate_path_cost(grid, path)
        return PathResult("BFS", True, path, len(visited_order), visited_order, execution_time_ms, cost, "Shortest path found.")
    else:
        return PathResult("BFS", False, [], len(visited_order), visited_order, execution_time_ms, 0.0, "Destination unreachable.")


def dfs(
    grid: Grid,
    start: Optional[Tuple[int, int]] = None,
    destination: Optional[Tuple[int, int]] = None,
    step_callback: Optional[Callable[[Tuple[int, int], Set[Tuple[int, int]], int], None]] = None,
) -> PathResult:
    """
    Depth-First Search (DFS) using a manual LIFO Stack.
    
    Properties:
      - Explores deeply along each branch before backtracking.
      - Finds a VALID path if reachable; does NOT guarantee shortest path.
      - Useful for topological ordering, cycle detection, and maze generation.
    
    Complexity:
      - Time Complexity: O(V + E).
      - Space Complexity: O(V) for visited set and call/stack frames.
    """
    t_start = time.perf_counter()

    s = start if start is not None else grid.start
    d = destination if destination is not None else grid.destination

    if s is None or d is None:
        t_end = time.perf_counter()
        return PathResult("DFS", False, [], 0, [], (t_end - t_start) * 1000, 0.0, "Start or destination undefined.")

    # Validation & Edge Cases
    if not grid.in_bounds(*s) or not grid.in_bounds(*d):
        t_end = time.perf_counter()
        return PathResult("DFS", False, [], 0, [], (t_end - t_start) * 1000, 0.0, "Coordinates out of bounds.")

    if grid.is_obstacle(*s) or grid.is_obstacle(*d):
        t_end = time.perf_counter()
        return PathResult("DFS", False, [], 0, [], (t_end - t_start) * 1000, 0.0, "Start or destination is an obstacle.")

    if s == d:
        t_end = time.perf_counter()
        return PathResult("DFS", True, [s], 1, [s], (t_end - t_start) * 1000, 0.0, "Start is equal to destination.")

    stack = Stack()
    stack.push(s)

    visited: Set[Tuple[int, int]] = set()
    parent_map: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {s: None}
    visited_order: List[Tuple[int, int]] = []

    target_reached = False

    while not stack.is_empty():
        curr = stack.pop()

        if curr in visited:
            continue

        visited.add(curr)
        visited_order.append(curr)

        if step_callback is not None:
            step_callback(curr, visited, len(stack))

        if curr == d:
            target_reached = True
            break

        # Neighbors pushed in reverse order so that canonical order (Up, Down, Left, Right)
        # is popped and explored first.
        neighbors = grid.get_neighbors(*curr)
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                # Update parent pointer only if not already discovered
                if neighbor not in parent_map:
                    parent_map[neighbor] = curr
                stack.push(neighbor)

    t_end = time.perf_counter()
    execution_time_ms = (t_end - t_start) * 1000.0

    if target_reached:
        path = reconstruct_path(parent_map, s, d)
        cost = calculate_path_cost(grid, path)
        return PathResult("DFS", True, path, len(visited_order), visited_order, execution_time_ms, cost, "Valid path found (non-optimal).")
    else:
        return PathResult("DFS", False, [], len(visited_order), visited_order, execution_time_ms, 0.0, "Destination unreachable.")


def dijkstra(
    grid: Grid,
    start: Optional[Tuple[int, int]] = None,
    destination: Optional[Tuple[int, int]] = None,
    step_callback: Optional[Callable[[Tuple[int, int], Set[Tuple[int, int]], int], None]] = None,
) -> PathResult:
    """
    Dijkstra's Algorithm using a manual Binary Min-Heap Priority Queue.
    
    Guarantees:
      - Finds the OPTIMAL SHORTEST PATH for any graph with non-negative edge weights.
      - Provably explores nodes in monotonically non-decreasing order of cost from start.
      - In an unweighted grid (uniform weight = 1), produces identical path length to BFS.
    
    Complexity:
      - Time Complexity: O((V + E) log V) with a binary min-heap.
      - Space Complexity: O(V) for distances map, parent map, and heap storage.
    """
    t_start = time.perf_counter()

    s = start if start is not None else grid.start
    d = destination if destination is not None else grid.destination

    if s is None or d is None:
        t_end = time.perf_counter()
        return PathResult("Dijkstra", False, [], 0, [], (t_end - t_start) * 1000, 0.0, "Start or destination undefined.")

    # Validation & Edge Cases
    if not grid.in_bounds(*s) or not grid.in_bounds(*d):
        t_end = time.perf_counter()
        return PathResult("Dijkstra", False, [], 0, [], (t_end - t_start) * 1000, 0.0, "Coordinates out of bounds.")

    if grid.is_obstacle(*s) or grid.is_obstacle(*d):
        t_end = time.perf_counter()
        return PathResult("Dijkstra", False, [], 0, [], (t_end - t_start) * 1000, 0.0, "Start or destination is an obstacle.")

    if s == d:
        t_end = time.perf_counter()
        return PathResult("Dijkstra", True, [s], 1, [s], (t_end - t_start) * 1000, 0.0, "Start is equal to destination.")

    min_heap = MinHeap()
    min_heap.push(0.0, s)

    distances: Dict[Tuple[int, int], float] = {s: 0.0}
    parent_map: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {s: None}
    visited: Set[Tuple[int, int]] = set()
    visited_order: List[Tuple[int, int]] = []

    target_reached = False

    while not min_heap.is_empty():
        current_dist, curr = min_heap.pop()

        # If already visited with an optimal path, skip stale heap entries
        if curr in visited:
            continue

        visited.add(curr)
        visited_order.append(curr)

        if step_callback is not None:
            step_callback(curr, visited, len(min_heap))

        if curr == d:
            target_reached = True
            break

        for neighbor in grid.get_neighbors(*curr):
            if neighbor in visited:
                continue

            movement_cost = grid.get_cost(*neighbor)
            new_distance = current_dist + movement_cost

            if new_distance < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_distance
                parent_map[neighbor] = curr
                min_heap.push(new_distance, neighbor)

    t_end = time.perf_counter()
    execution_time_ms = (t_end - t_start) * 1000.0

    if target_reached:
        path = reconstruct_path(parent_map, s, d)
        cost = distances.get(d, calculate_path_cost(grid, path))
        return PathResult("Dijkstra", True, path, len(visited_order), visited_order, execution_time_ms, cost, "Optimal shortest path found.")
    else:
        return PathResult("Dijkstra", False, [], len(visited_order), visited_order, execution_time_ms, 0.0, "Destination unreachable.")


# ==============================================================================
# 5. ALGORITHM COMPARISON SUITE
# ==============================================================================

def run_comparison(grid: Grid) -> Dict[str, PathResult]:
    """
    Run BFS, DFS, and Dijkstra independently on the identical grid state.
    
    Measures:
      - Path reachability (Found vs Not Found)
      - Path length (edge count)
      - Total path cost (weighted sum)
      - Visited nodes count (exploration efficiency)
      - Execution time via time.perf_counter() in milliseconds
    """
    results: Dict[str, PathResult] = {}
    results["BFS"] = bfs(grid)
    results["DFS"] = dfs(grid)
    results["Dijkstra"] = dijkstra(grid)
    return results


def format_comparison_table(results: Dict[str, PathResult]) -> str:
    """Format comparison benchmark results into a clean text table."""
    lines: List[str] = []
    lines.append("+" + "-" * 78 + "+")
    lines.append(f"| {'Algorithm':<14} | {'Status':<10} | {'Steps':<7} | {'Cost':<9} | {'Visited':<9} | {'Time (ms)':<12} |")
    lines.append("+" + "-" * 78 + "+")

    for name, res in results.items():
        status = "FOUND" if res.found else "NO PATH"
        steps_str = str(res.path_length) if res.found else "N/A"
        cost_str = f"{res.path_cost:.2f}" if res.found else "N/A"
        visited_str = str(res.visited_count)
        time_str = f"{res.execution_time_ms:.4f}"
        lines.append(f"| {name:<14} | {status:<10} | {steps_str:<7} | {cost_str:<9} | {visited_str:<9} | {time_str:<12} |")

    lines.append("+" + "-" * 78 + "+")
    return "\n".join(lines)


# ==============================================================================
# 6. TERMINAL VISUALIZER & ANIMATION ENGINE
# ==============================================================================

class TerminalVisualizer:
    """Manages console rendering, animation delays, and live step visualization."""

    SPEED_PRESETS = {
        "1": ("Instant (0 ms)", 0.0),
        "2": ("Fast (15 ms)", 0.015),
        "3": ("Normal (40 ms)", 0.040),
        "4": ("Slow (100 ms)", 0.100),
    }

    def __init__(self, use_color: bool = True) -> None:
        self.use_color: bool = use_color
        self.delay: float = 0.025  # default 25ms delay
        self.enable_animation: bool = True

    def clear_screen(self) -> None:
        """Clear the console screen."""
        if os.name == "nt":
            os.system("cls")
        else:
            # ANSI escape codes for clear screen and reset cursor position
            sys.stdout.write("\033[H\033[2J")
            sys.stdout.flush()

    def run_animated_algorithm(self, grid: Grid, algo_name: str) -> PathResult:
        """Execute an algorithm while streaming live step updates to the terminal."""
        step_count = 0

        def step_callback(curr: Tuple[int, int], visited_nodes: Set[Tuple[int, int]], frontier_size: int) -> None:
            nonlocal step_count
            step_count += 1

            if not self.enable_animation or self.delay <= 0:
                return

            self.clear_screen()
            print("=" * 60)
            print(f" PATHFINDING VISUALIZATION: {algo_name.upper()}")
            print("=" * 60)
            print(f" Exploring Node : ({curr[0]:2d}, {curr[1]:2d})")
            print(f" Visited So Far : {len(visited_nodes)} cells")
            print(f" Frontier Size  : {frontier_size} items")
            print(f" Steps Elapsed  : {step_count}")
            print("-" * 60)
            print(grid.render(visited_nodes=visited_nodes, current_node=curr, use_color=self.use_color))
            print("-" * 60)
            time.sleep(self.delay)

        if algo_name == "BFS":
            result = bfs(grid, step_callback=step_callback)
        elif algo_name == "DFS":
            result = dfs(grid, step_callback=step_callback)
        elif algo_name == "Dijkstra":
            result = dijkstra(grid, step_callback=step_callback)
        else:
            raise ValueError(f"Unknown algorithm: {algo_name}")

        # Render final state
        self.clear_screen()
        print("=" * 60)
        print(f" FINAL RESULT: {algo_name.upper()}")
        print("=" * 60)
        print(result.summary())
        print("-" * 60)
        visited_set = set(result.visited_order)
        print(grid.render(visited_nodes=visited_set, path=result.path, use_color=self.use_color))
        print("=" * 60)
        if result.found:
            print(f" Path Coordinates ({len(result.path)} nodes):")
            path_str = " -> ".join(f"({r},{c})" for r, c in result.path)
            if len(path_str) > 120:
                print(f" {path_str[:115]} ... -> ({result.path[-1][0]},{result.path[-1][1]})")
            else:
                print(f" {path_str}")
        else:
            print(" No valid path could reach the destination.")
        print()
        return result


# ==============================================================================
# 7. INTERACTIVE MENU INTERFACE
# ==============================================================================

class PathfindingCLI:
    """Interactive command-line interface for the Pathfinding Visualizer."""

    def __init__(self) -> None:
        self.grid: Grid = Grid(rows=10, cols=20)
        self.visualizer: TerminalVisualizer = TerminalVisualizer()
        self.selected_algo: str = "BFS"
        self._load_default_obstacles()

    def _load_default_obstacles(self) -> None:
        """Generate a clean initial obstacle wall demonstrating path redirection."""
        for r in range(2, 8):
            self.grid.add_obstacle(r, 8)
        self.grid.add_obstacle(2, 9)
        self.grid.add_obstacle(2, 10)

    def print_banner(self) -> None:
        print(r"""
  ____       _   _     __ _           _ _             
 |  _ \ __ _| |_| |__ / _(_)_ __   __| (_)_ __   __ _ 
 | |_) / _` | __| '_ \ |_| | '_ \ / _` | | '_ \ / _` |
 |  __/ (_| | |_| | | |  _| | | | | (_| | | | | | (_| |
 |_|   \__,_|\__|_| |_|_| |_|_| |_|\__,_|_|_| |_|\__, |
  __     ___                 _ _                  |___/ 
  \ \   / (_)___ _   _  __ _| (_)_______ _ __           
   \ \ / /| / __| | | |/ _` | | |_  / _ \ '__|          
    \ V / | \__ \ |_| | (_| | | |/ /  __/ |             
     \_/  |_|___/\__,_|\__,_|_|_/___\___|_|             
        """)
        print(" Graph-Based Pathfinding & Shortest Path Analysis System")
        print(" Manual Data Structures: Linked Queue, Linked Stack, Binary Min-Heap")
        print("=" * 70)

    def print_menu(self) -> None:
        start_str = f"({self.grid.start[0]}, {self.grid.start[1]})" if self.grid.start else "None"
        dest_str = f"({self.grid.destination[0]}, {self.grid.destination[1]})" if self.grid.destination else "None"
        anim_str = f"{self.visualizer.delay * 1000:.0f} ms" if self.visualizer.enable_animation and self.visualizer.delay > 0 else "Instant"

        print(f"\n[CURRENT CONFIG] Grid: {self.grid.rows}x{self.grid.cols} | Start: {start_str} | Dest: {dest_str} | Obstacles: {len(self.grid.obstacles)} | Algo: {self.selected_algo} | Delay: {anim_str}")
        print("-" * 70)
        print(" 1.  Create New Grid Dimensions       8.  Select Depth-First Search (DFS)")
        print(" 2.  Set Start Position               9.  Select Dijkstra's Algorithm")
        print(" 3.  Set Destination Position         10. Run Selected Algorithm")
        print(" 4.  Add Obstacle(s)                  11. Compare All 3 Algorithms (Benchmark)")
        print(" 5.  Remove Obstacle(s)               12. Reset Grid / Clear Obstacles")
        print(" 6.  Display Current Grid             13. Load Preset Scenario")
        print(" 7.  Select Breadth-First (BFS)       14. Configure Animation Speed")
        print(" 0.  Exit Application")
        print("-" * 70)

    def handle_create_grid(self) -> None:
        print("\n--- CREATE NEW GRID ---")
        try:
            r_str = input(f"Enter number of rows [default {self.grid.rows}]: ").strip()
            c_str = input(f"Enter number of columns [default {self.grid.cols}]: ").strip()
            rows = int(r_str) if r_str else self.grid.rows
            cols = int(c_str) if c_str else self.grid.cols
            if rows < 2 or cols < 2:
                print("Error: Grid dimensions must be at least 2x2.")
                return
            if rows > 40 or cols > 80:
                print("Warning: Large grids may exceed terminal display width.")
            self.grid = Grid(rows, cols)
            print(f"Success: Created new {rows}x{cols} grid with Start (0,0) and Destination ({rows-1},{cols-1}).")
        except ValueError:
            print("Error: Please enter valid positive integers for dimensions.")

    def handle_set_start(self) -> None:
        print("\n--- SET START POSITION ---")
        try:
            inp = input(f"Enter row and col (e.g. '0 0' or '0, 0'): ").strip()
            parts = [int(p) for p in inp.replace(",", " ").split()]
            if len(parts) != 2:
                print("Error: Expected exactly two numbers: <row> <col>.")
                return
            success, msg = self.grid.set_start(parts[0], parts[1])
            print(f"{'Success' if success else 'Error'}: {msg}")
        except ValueError:
            print("Error: Invalid coordinate input.")

    def handle_set_destination(self) -> None:
        print("\n--- SET DESTINATION POSITION ---")
        try:
            inp = input(f"Enter row and col (e.g. '{self.grid.rows-1} {self.grid.cols-1}'): ").strip()
            parts = [int(p) for p in inp.replace(",", " ").split()]
            if len(parts) != 2:
                print("Error: Expected exactly two numbers: <row> <col>.")
                return
            success, msg = self.grid.set_destination(parts[0], parts[1])
            print(f"{'Success' if success else 'Error'}: {msg}")
        except ValueError:
            print("Error: Invalid coordinate input.")

    def handle_add_obstacles(self) -> None:
        print("\n--- ADD OBSTACLES ---")
        print("Options:")
        print("  1. Add single cell (e.g. '3 4')")
        print("  2. Add horizontal wall: row col_start col_end (e.g. '5 2 12')")
        print("  3. Add vertical wall: col row_start row_end (e.g. '7 1 8')")
        print("  4. Generate random obstacle field")
        sub_choice = input("Select obstacle mode (1-4): ").strip()

        if sub_choice == "1":
            inp = input("Enter row and col: ").strip()
            parts = [int(p) for p in inp.replace(",", " ").split()]
            if len(parts) == 2:
                success, msg = self.grid.add_obstacle(parts[0], parts[1])
                print(f"{'Success' if success else 'Error'}: {msg}")
            else:
                print("Error: Expected 2 numbers.")
        elif sub_choice == "2":
            inp = input("Enter row col_start col_end: ").strip()
            parts = [int(p) for p in inp.replace(",", " ").split()]
            if len(parts) == 3:
                r, c1, c2 = parts
                c_start, c_end = min(c1, c2), max(c1, c2)
                added = 0
                for c in range(c_start, c_end + 1):
                    ok, _ = self.grid.add_obstacle(r, c)
                    if ok:
                        added += 1
                print(f"Added {added} obstacle cells along row {r}.")
            else:
                print("Error: Expected 3 numbers.")
        elif sub_choice == "3":
            inp = input("Enter col row_start row_end: ").strip()
            parts = [int(p) for p in inp.replace(",", " ").split()]
            if len(parts) == 3:
                c, r1, r2 = parts
                r_start, r_end = min(r1, r2), max(r1, r2)
                added = 0
                for r in range(r_start, r_end + 1):
                    ok, _ = self.grid.add_obstacle(r, c)
                    if ok:
                        added += 1
                print(f"Added {added} obstacle cells along column {c}.")
            else:
                print("Error: Expected 3 numbers.")
        elif sub_choice == "4":
            pct_str = input("Enter density percentage (10-40, default 20): ").strip()
            pct = int(pct_str) if pct_str else 20
            pct = max(5, min(60, pct))
            added = 0
            for r in range(self.grid.rows):
                for c in range(self.grid.cols):
                    if (r, c) != self.grid.start and (r, c) != self.grid.destination:
                        if random.randint(1, 100) <= pct:
                            self.grid.add_obstacle(r, c)
                            added += 1
            print(f"Generated {added} random obstacles (~{pct}% density).")
        else:
            print("Invalid option.")

    def handle_remove_obstacles(self) -> None:
        print("\n--- REMOVE OBSTACLES ---")
        print("Options: 1. Remove single cell  2. Clear ALL obstacles")
        sub = input("Select option (1-2): ").strip()
        if sub == "1":
            inp = input("Enter row and col: ").strip()
            parts = [int(p) for p in inp.replace(",", " ").split()]
            if len(parts) == 2:
                success, msg = self.grid.remove_obstacle(parts[0], parts[1])
                print(f"{'Success' if success else 'Error'}: {msg}")
            else:
                print("Error: Expected 2 numbers.")
        elif sub == "2":
            self.grid.clear_obstacles()
            print("All obstacles cleared.")

    def handle_display_grid(self) -> None:
        print("\n--- CURRENT GRID STATE ---")
        print(self.grid.render(use_color=self.visualizer.use_color))

    def handle_load_preset(self) -> None:
        print("\n--- PRESET SCENARIOS ---")
        print(" 1. Wall Barrier (Navigating around a divider)")
        print(" 2. Winding Maze (Tests deep vs level traversal)")
        print(" 3. Weighted Mud Pit (Dijkstra optimal vs BFS step-count)")
        print(" 4. Unreachable Island (Surrounded by walls)")
        choice = input("Select preset (1-4): ").strip()

        if choice == "1":
            self.grid = Grid(10, 20)
            self.grid.set_start(4, 2)
            self.grid.set_destination(4, 17)
            for r in range(1, 9):
                self.grid.add_obstacle(r, 10)
            print("Loaded Preset 1: Wall Barrier.")
        elif choice == "2":
            self.grid = Grid(11, 21)
            self.grid.set_start(1, 1)
            self.grid.set_destination(9, 19)
            # Maze walls
            for c in range(1, 19):
                self.grid.add_obstacle(3, c)
                self.grid.add_obstacle(7, c + 1)
            for r in range(3, 8):
                self.grid.add_obstacle(r, 10)
            self.grid.remove_obstacle(3, 5)
            self.grid.remove_obstacle(7, 15)
            print("Loaded Preset 2: Winding Maze.")
        elif choice == "3":
            self.grid = Grid(7, 15)
            self.grid.set_start(3, 1)
            self.grid.set_destination(3, 13)
            # Center direct path has high weight (mud = cost 10)
            for c in range(3, 12):
                self.grid.set_weight(3, c, 10.0)
            print("Loaded Preset 3: Weighted Mud Pit (Center cost = 10, Detours cost = 1).")
        elif choice == "4":
            self.grid = Grid(9, 15)
            self.grid.set_start(1, 1)
            self.grid.set_destination(4, 10)
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if (dr, dc) != (0, 0):
                        self.grid.add_obstacle(4 + dr, 10 + dc)
            print("Loaded Preset 4: Unreachable Island (Destination is walled off).")
        else:
            print("Invalid preset selection.")

    def handle_configure_speed(self) -> None:
        print("\n--- CONFIGURE ANIMATION SPEED ---")
        print(" 1. Instant (0 ms - no rendering delay)")
        print(" 2. Fast (15 ms)")
        print(" 3. Normal (40 ms)")
        print(" 4. Slow (100 ms)")
        print(" 5. Custom millisecond value")
        choice = input("Select speed (1-5): ").strip()

        if choice in TerminalVisualizer.SPEED_PRESETS:
            label, delay = TerminalVisualizer.SPEED_PRESETS[choice]
            self.visualizer.delay = delay
            self.visualizer.enable_animation = (delay > 0)
            print(f"Animation set to: {label}")
        elif choice == "5":
            try:
                ms = float(input("Enter delay in milliseconds (0 - 500): ").strip())
                self.visualizer.delay = max(0.0, ms / 1000.0)
                self.visualizer.enable_animation = (ms > 0)
                print(f"Custom delay set to {ms:.1f} ms.")
            except ValueError:
                print("Error: Invalid number.")
        else:
            print("Invalid speed choice.")

    def handle_comparison(self) -> None:
        print("\n" + "=" * 80)
        print(" ALGORITHM PERFORMANCE BENCHMARK (BFS vs DFS vs Dijkstra)")
        print("=" * 80)
        print(" Running independent executions on the current grid configuration...\n")

        results = run_comparison(self.grid)
        table_str = format_comparison_table(results)
        print(table_str)

        print("\n--- THEORETICAL & EMPIRICAL ANALYSIS ---")
        print(" * Breadth-First Search (BFS):")
        print("   - Optimality: Guaranteed shortest path in unweighted graphs.")
        print("   - Data Structure: FIFO Queue (O(1) enqueue and dequeue).")
        print(f"   - Visited: {results['BFS'].visited_count} cells | Path: {results['BFS'].path_length} steps | Time: {results['BFS'].execution_time_ms:.4f} ms.")

        print("\n * Depth-First Search (DFS):")
        print("   - Optimality: Non-optimal. Deeply dives along branches; susceptible to tortuous routes.")
        print("   - Data Structure: LIFO Stack (O(1) push and pop).")
        print(f"   - Visited: {results['DFS'].visited_count} cells | Path: {results['DFS'].path_length} steps | Time: {results['DFS'].execution_time_ms:.4f} ms.")

        print("\n * Dijkstra's Algorithm:")
        print("   - Optimality: Provably optimal for all non-negative edge and cell weights.")
        print("   - Data Structure: Binary Min-Heap Priority Queue (O(log V) insertion/extraction).")
        print(f"   - Visited: {results['Dijkstra'].visited_count} cells | Path: {results['Dijkstra'].path_length} steps | Time: {results['Dijkstra'].execution_time_ms:.4f} ms.")

        print("\nNote: Execution times are measured using time.perf_counter(). Runtimes vary based on")
        print("CPU frequency, thermal throttling, cache lines, and system workload.")
        print("=" * 80)

    def run(self) -> None:
        """Main application execution loop."""
        self.visualizer.clear_screen()
        self.print_banner()

        while True:
            self.print_menu()
            choice = input("\nEnter your choice (0-14): ").strip()

            if choice == "0":
                print("\nExiting Pathfinding Visualizer. Thank you!")
                break
            elif choice == "1":
                self.handle_create_grid()
            elif choice == "2":
                self.handle_set_start()
            elif choice == "3":
                self.handle_set_destination()
            elif choice == "4":
                self.handle_add_obstacles()
            elif choice == "5":
                self.handle_remove_obstacles()
            elif choice == "6":
                self.handle_display_grid()
            elif choice == "7":
                self.selected_algo = "BFS"
                print("Selected: Breadth-First Search (BFS)")
            elif choice == "8":
                self.selected_algo = "DFS"
                print("Selected: Depth-First Search (DFS)")
            elif choice == "9":
                self.selected_algo = "Dijkstra"
                print("Selected: Dijkstra's Algorithm")
            elif choice == "10":
                self.visualizer.run_animated_algorithm(self.grid, self.selected_algo)
            elif choice == "11":
                self.handle_comparison()
            elif choice == "12":
                self.grid.clear_obstacles()
                self.grid.weights.clear()
                print("Grid reset: obstacles and custom weights cleared.")
            elif choice == "13":
                self.handle_load_preset()
            elif choice == "14":
                self.handle_configure_speed()
            else:
                print("Error: Unknown option. Please choose a valid number from the menu.")


def main() -> None:
    """Launch the GUI by default if DISPLAY is available, else launch CLI."""
    if "--cli" in sys.argv:
        cli = PathfindingCLI()
        cli.run()
        return

    # Try launching GUI
    try:
        _current_dir = os.path.dirname(os.path.abspath(__file__))
        if _current_dir not in sys.path:
            sys.path.insert(0, _current_dir)
        from gui import launch_gui
        launch_gui()
    except Exception as exc:
        if "--gui" in sys.argv:
            print(f"Error launching Graphical interface: {exc}")
            sys.exit(1)
        cli = PathfindingCLI()
        cli.run()


if __name__ == "__main__":
    main()

