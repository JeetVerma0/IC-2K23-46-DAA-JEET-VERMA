#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 7: Graphs
Program 8: Maze Solver and Shortest Path Navigator using BFS

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
A 2D maze grid can be mathematically modeled as an implicit graph G = (V, E):
  - Vertices (V): Each open cell (r, c) in the grid represents a vertex.
  - Edges (E): An undirected edge exists between any two open cells that share
    an orthogonal boundary (North, South, East, West).
  - Obstacles (#): Wall cells contain no incoming or outgoing edges.

WHY BFS FINDS THE SHORTEST PATH:
Because each orthogonal step in a 2D grid has a uniform edge cost of 1,
Breadth-First Search (BFS) is mathematically GUARANTEED to find the path
with the minimum number of steps from Start 'S' to Destination 'E'.

ALGORITHM:
  1. Parse the grid; identify start coordinates (sr, sc) and end (er, ec).
  2. Enqueue (sr, sc) into a manual FIFO queue; initialize parent[sr, sc] = None.
  3. While queue is not empty:
     - Dequeue current coordinate (r, c).
     - If (r, c) == (er, ec), break; target found!
     - For each orthogonal delta (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
       nr, nc = r + dr, c + dc
       If 0 <= nr < rows, 0 <= nc < cols, cell is not '#' and not visited:
         Mark visited, set parent[(nr, nc)] = (r, c), enqueue (nr, nc).
  4. If destination found, backtrack via parent pointers to reconstruct path;
     mark path cells with '*' and display solved maze.
  5. If queue empties without reaching 'E', report destination as UNREACHABLE.

COMPLEXITIES:
  - Time Complexity : O(R * C) where R is rows and C is columns.
  - Space Complexity: O(R * C) for visited set, queue, and parent mapping.
================================================================================
"""

import sys
from typing import Any, Dict, List, Optional, Set, Tuple


class QueueNode:
    """Linked list node for custom manual FIFO queue."""

    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.next: Optional["QueueNode"] = None


class ManualQueue:
    """Custom manual dynamic FIFO queue."""

    def __init__(self) -> None:
        self._front: Optional[QueueNode] = None
        self._rear: Optional[QueueNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        return self._front is None

    def enqueue(self, item: Any) -> None:
        node = QueueNode(item)
        if self.is_empty():
            self._front = node
            self._rear = node
        else:
            assert self._rear is not None
            self._rear.next = node
            self._rear = node
        self._size += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")
        assert self._front is not None
        val = self._front.data
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return val


class MazeSolver:
    """Solves 2D grid mazes using Breadth-First Search graph traversal."""

    # Orthogonal movement vectors: Up, Down, Left, Right
    DIRECTIONS: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, maze_lines: List[str]) -> None:
        """
        Initialize the maze from a list of string rows.
        Legend:
          'S' = Start
          'E' = Destination
          '.' = Open passageway
          '#' = Wall obstacle
        """
        if not maze_lines or not maze_lines[0]:
            raise ValueError("Maze cannot be empty.")

        parsed_grid: List[List[str]] = []
        for line in maze_lines:
            s_line = line.strip()
            if " " in s_line:
                parsed_grid.append(s_line.split())
            else:
                parsed_grid.append(list(s_line))

        self.rows: int = len(parsed_grid)
        self.cols: int = len(parsed_grid[0])
        self.grid: List[List[str]] = parsed_grid

        self.start: Optional[Tuple[int, int]] = None
        self.end: Optional[Tuple[int, int]] = None

        # Find Start and End markers
        for r in range(self.rows):
            for c in range(self.cols):
                char = self.grid[r][c]
                if char == "S":
                    if self.start is not None:
                        raise ValueError("Multiple Start 'S' positions detected.")
                    self.start = (r, c)
                elif char == "E":
                    if self.end is not None:
                        raise ValueError("Multiple End 'E' positions detected.")
                    self.end = (r, c)

        if self.start is None:
            raise ValueError("Maze is missing a Start position 'S'.")
        if self.end is None:
            raise ValueError("Maze is missing an End position 'E'.")

    def solve(self) -> Tuple[Optional[List[Tuple[int, int]]], int]:
        """
        Find shortest path from Start to End using BFS.

        Returns:
            (path, total_steps): List of (r, c) tuples, or (None, -1) if unreachable.
        """
        assert self.start is not None and self.end is not None

        if self.start == self.end:
            return [self.start], 0

        queue = ManualQueue()
        queue.enqueue(self.start)

        visited: Set[Tuple[int, int]] = {self.start}
        parent: Dict[Tuple[int, int], Tuple[int, int]] = {}

        found = False
        while not queue.is_empty():
            curr_r, curr_c = queue.dequeue()

            if (curr_r, curr_c) == self.end:
                found = True
                break

            for dr, dc in self.DIRECTIONS:
                nr, nc = curr_r + dr, curr_c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid[nr][nc] != "#" and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        parent[(nr, nc)] = (curr_r, curr_c)
                        queue.enqueue((nr, nc))

        if not found:
            return None, -1

        # Reconstruct path from end to start
        path = []
        curr = self.end
        while curr != self.start:
            path.append(curr)
            curr = parent[curr]
        path.append(self.start)
        path.reverse()

        return path, len(path) - 1

    def display(self, path: Optional[List[Tuple[int, int]]] = None) -> None:
        """Display the maze, marking the solved path with '*'."""
        path_set = set(path) if path else set()
        print(f"\nMaze ({self.rows} x {self.cols}):")
        for r in range(self.rows):
            row_display = []
            for c in range(self.cols):
                coord = (r, c)
                char = self.grid[r][c]
                if coord in path_set and char not in ("S", "E"):
                    row_display.append("*")  # Mark solution path
                else:
                    row_display.append(char)
            print("  " + " ".join(row_display))


def get_sample_solvable_maze() -> List[str]:
    """Standard 7x9 solvable maze."""
    return [
        "S . # . . . # . .",
        "# . # . # . # . #",
        "# . . . # . . . #",
        "# # # . # # # . #",
        ". . # . . . # . .",
        ". # # # # . # # .",
        ". . . . . . . . E",
    ]


def get_sample_unsolvable_maze() -> List[str]:
    """Maze with complete wall blocking destination."""
    return [
        "S . . # . .",
        ". # . # . .",
        ". # . # # #",
        "# # . # . E",
    ]


def run_tests() -> None:
    """Automated unit verification test suite for Maze Solver."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Maze Solver (BFS Graph Traversal)")
    print("=" * 70)

    # Test 1: Solvable maze
    solver = MazeSolver(get_sample_solvable_maze())
    path, steps = solver.solve()
    assert path is not None
    assert path[0] == solver.start
    assert path[-1] == solver.end
    assert steps > 0
    print(f"[PASS] Test 1: Solvable maze verified (Found shortest path of {steps} steps).")

    # Test 2: Unsolvable maze
    unsolvable = MazeSolver(get_sample_unsolvable_maze())
    u_path, u_steps = unsolvable.solve()
    assert u_path is None
    assert u_steps == -1
    print("[PASS] Test 2: Unsolvable maze correctly handled (Returned None, -1).")

    # Test 3: Minimal adjacent maze
    mini_cell = MazeSolver(["S E"])
    p_mini, s_mini = mini_cell.solve()
    assert p_mini == [(0, 0), (0, 1)]
    assert s_mini == 1
    print("[PASS] Test 3: Minimal direct adjacent maze verified (1 step).")

    # Test 4: Missing start marker validation
    try:
        MazeSolver([". . #", ". E ."])
        assert False, "Should raise ValueError when missing Start 'S'"
    except ValueError:
        pass
    print("[PASS] Test 4: Missing start validation caught.")

    print("\nALL 4 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 55)
    print("           BFS MAZE SOLVER MENU")
    print("=" * 55)
    print(" 1. Display Current Maze")
    print(" 2. Solve Maze and Display Shortest Path")
    print(" 3. Load Sample Solvable Maze (7 x 9)")
    print(" 4. Load Sample Unsolvable Maze (Blocked by Walls)")
    print(" 5. Run Automated Tests (--test)")
    print(" 6. Exit")
    print("=" * 55)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 7 — 2D Maze Solver (BFS Shortest Path)")
    print("==========================================================")

    solver = MazeSolver(get_sample_solvable_maze())
    print("Loaded default sample 7x9 maze.")

    while True:
        print_menu()
        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            solver.display()

        elif choice == "2":
            path, steps = solver.solve()
            if path:
                print(f"\nSolution Found in {steps} steps!")
                print(f"Path Coordinates: {' -> '.join(map(str, path))}")
                solver.display(path)
            else:
                print("\nDestination 'E' is UNREACHABLE from Start 'S' (Blocked by walls).")
                solver.display()

        elif choice == "3":
            solver = MazeSolver(get_sample_solvable_maze())
            print("Loaded sample solvable maze.")

        elif choice == "4":
            solver = MazeSolver(get_sample_unsolvable_maze())
            print("Loaded sample blocked/unsolvable maze.")

        elif choice == "5":
            run_tests()

        elif choice == "6":
            print("Exiting Maze Solver Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 6.")


if __name__ == "__main__":
    main()
