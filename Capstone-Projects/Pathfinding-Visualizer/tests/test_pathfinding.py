#!/usr/bin/env python3
"""
================================================================================
UNIT TESTS: PATHFINDING VISUALIZER & GRAPH ALGORITHMS
================================================================================
Test suite for manual data structures, grid representations, pathfinding
algorithms (BFS, DFS, Dijkstra), path reconstruction, edge cases, and benchmarks.

Author: Antigravity DSA Assistant
Course: IC-307D — Data Structures and Algorithms Lab
================================================================================
"""

import os
import sys
import unittest

# Ensure pathfinding_visualizer is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from pathfinding_visualizer import (
    Grid,
    MinHeap,
    PathResult,
    Queue,
    Stack,
    bfs,
    dfs,
    dijkstra,
    reconstruct_path,
    run_comparison,
)


class TestManualQueue(unittest.TestCase):
    """Unit tests for the manually implemented FIFO Queue."""

    def setUp(self) -> None:
        self.queue = Queue()

    def test_initial_state(self) -> None:
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(len(self.queue), 0)
        self.assertFalse(bool(self.queue))

    def test_enqueue_dequeue_order(self) -> None:
        items = ["A", "B", "C", "D"]
        for item in items:
            self.queue.enqueue(item)

        self.assertFalse(self.queue.is_empty())
        self.assertEqual(len(self.queue), 4)
        self.assertEqual(self.queue.peek(), "A")

        dequeued = []
        while not self.queue.is_empty():
            dequeued.append(self.queue.dequeue())

        self.assertEqual(dequeued, items)
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(len(self.queue), 0)

    def test_underflow_exceptions(self) -> None:
        with self.assertRaises(IndexError):
            self.queue.dequeue()
        with self.assertRaises(IndexError):
            self.queue.peek()


class TestManualStack(unittest.TestCase):
    """Unit tests for the manually implemented LIFO Stack."""

    def setUp(self) -> None:
        self.stack = Stack()

    def test_initial_state(self) -> None:
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(len(self.stack), 0)
        self.assertFalse(bool(self.stack))

    def test_push_pop_order(self) -> None:
        items = [10, 20, 30, 40]
        for item in items:
            self.stack.push(item)

        self.assertFalse(self.stack.is_empty())
        self.assertEqual(len(self.stack), 4)
        self.assertEqual(self.stack.peek(), 40)

        popped = []
        while not self.stack.is_empty():
            popped.append(self.stack.pop())

        self.assertEqual(popped, [40, 30, 20, 10])
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(len(self.stack), 0)

    def test_underflow_exceptions(self) -> None:
        with self.assertRaises(IndexError):
            self.stack.pop()
        with self.assertRaises(IndexError):
            self.stack.peek()


class TestManualMinHeap(unittest.TestCase):
    """Unit tests for the manually implemented Binary Min-Heap."""

    def setUp(self) -> None:
        self.heap = MinHeap()

    def test_initial_state(self) -> None:
        self.assertTrue(self.heap.is_empty())
        self.assertEqual(len(self.heap), 0)
        self.assertFalse(bool(self.heap))

    def test_push_and_pop_sorted_order(self) -> None:
        values = [(5.0, "five"), (1.5, "one-half"), (8.0, "eight"), (0.2, "point-two"), (3.0, "three")]
        for priority, item in values:
            self.heap.push(priority, item)

        self.assertEqual(len(self.heap), 5)
        self.assertEqual(self.heap.peek(), (0.2, "point-two"))

        extracted_priorities = []
        extracted_items = []
        while not self.heap.is_empty():
            p, it = self.heap.pop()
            extracted_priorities.append(p)
            extracted_items.append(it)

        self.assertEqual(extracted_priorities, [0.2, 1.5, 3.0, 5.0, 8.0])
        self.assertEqual(extracted_items, ["point-two", "one-half", "three", "five", "eight"])
        self.assertTrue(self.heap.is_empty())

    def test_tie_breaker_stability(self) -> None:
        # Pushing identical priorities should not raise comparison error on non-comparable payloads
        class CustomObj:
            def __init__(self, val: int) -> None:
                self.val = val

        self.heap.push(2.0, CustomObj(1))
        self.heap.push(2.0, CustomObj(2))
        self.heap.push(1.0, CustomObj(3))

        p1, obj1 = self.heap.pop()
        self.assertEqual(p1, 1.0)
        self.assertEqual(obj1.val, 3)

        p2, obj2 = self.heap.pop()
        self.assertEqual(p2, 2.0)
        self.assertEqual(obj2.val, 1)

    def test_underflow_exceptions(self) -> None:
        with self.assertRaises(IndexError):
            self.heap.pop()
        with self.assertRaises(IndexError):
            self.heap.peek()


class TestGridRepresentation(unittest.TestCase):
    """Unit tests for Grid operations, obstacles, boundaries, and validation."""

    def setUp(self) -> None:
        self.grid = Grid(rows=6, cols=8)

    def test_dimensions_and_defaults(self) -> None:
        self.assertEqual(self.grid.rows, 6)
        self.assertEqual(self.grid.cols, 8)
        self.assertEqual(self.grid.start, (0, 0))
        self.assertEqual(self.grid.destination, (5, 7))

    def test_boundary_checks(self) -> None:
        self.assertTrue(self.grid.in_bounds(0, 0))
        self.assertTrue(self.grid.in_bounds(5, 7))
        self.assertFalse(self.grid.in_bounds(-1, 0))
        self.assertFalse(self.grid.in_bounds(6, 0))
        self.assertFalse(self.grid.in_bounds(0, 8))

    def test_set_start_and_destination(self) -> None:
        ok, _ = self.grid.set_start(2, 3)
        self.assertTrue(ok)
        self.assertEqual(self.grid.start, (2, 3))

        ok, _ = self.grid.set_destination(4, 5)
        self.assertTrue(ok)
        self.assertEqual(self.grid.destination, (4, 5))

        # Start equal to destination rejected
        ok, _ = self.grid.set_start(4, 5)
        self.assertFalse(ok)

        # Out of bounds rejected
        ok, _ = self.grid.set_start(10, 10)
        self.assertFalse(ok)

    def test_obstacles(self) -> None:
        ok, _ = self.grid.add_obstacle(2, 2)
        self.assertTrue(ok)
        self.assertTrue(self.grid.is_obstacle(2, 2))
        self.assertFalse(self.grid.is_passable(2, 2))

        # Cannot place obstacle on start or destination
        ok_start, _ = self.grid.add_obstacle(0, 0)
        self.assertFalse(ok_start)
        ok_dest, _ = self.grid.add_obstacle(5, 7)
        self.assertFalse(ok_dest)

        # Remove obstacle
        ok_rem, _ = self.grid.remove_obstacle(2, 2)
        self.assertTrue(ok_rem)
        self.assertFalse(self.grid.is_obstacle(2, 2))

    def test_neighbors_cardinal_directions(self) -> None:
        # Corner cell (0, 0): Only Down (1, 0) and Right (0, 1) are in-bounds
        neighbors = self.grid.get_neighbors(0, 0)
        self.assertEqual(neighbors, [(1, 0), (0, 1)])

        # Center cell (2, 2) has 4 neighbors: Up, Down, Left, Right
        neighbors = self.grid.get_neighbors(2, 2)
        self.assertEqual(neighbors, [(1, 2), (3, 2), (2, 1), (2, 3)])

        # Block top neighbor (1, 2)
        self.grid.add_obstacle(1, 2)
        neighbors = self.grid.get_neighbors(2, 2)
        self.assertNotIn((1, 2), neighbors)
        self.assertEqual(neighbors, [(3, 2), (2, 1), (2, 3)])


class TestPathfindingAlgorithms(unittest.TestCase):
    """Comprehensive tests for BFS, DFS, and Dijkstra on various grid topologies."""

    def setUp(self) -> None:
        self.grid = Grid(rows=5, cols=5)
        self.grid.set_start(0, 0)
        self.grid.set_destination(4, 4)

    def _verify_valid_contiguous_path(
        self, grid: Grid, path: list, start: tuple, destination: tuple
    ) -> None:
        """Helper to verify that a reconstructed path is valid and contiguous."""
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], destination)

        for i in range(len(path) - 1):
            curr = path[i]
            nxt = path[i + 1]
            self.assertFalse(grid.is_obstacle(*curr))
            self.assertFalse(grid.is_obstacle(*nxt))
            dr = abs(nxt[0] - curr[0])
            dc = abs(nxt[1] - curr[1])
            # Exactly 1 step in cardinal direction (Manhattan distance = 1)
            self.assertEqual(dr + dc, 1, f"Invalid step from {curr} to {nxt}")

    def test_bfs_shortest_path_unweighted(self) -> None:
        # On a 5x5 grid from (0,0) to (4,4), Manhattan distance is 4 + 4 = 8 steps
        res = bfs(self.grid)
        self.assertTrue(res.found)
        self.assertEqual(res.path_length, 8)
        self._verify_valid_contiguous_path(self.grid, res.path, (0, 0), (4, 4))

    def test_dfs_valid_path(self) -> None:
        res = dfs(self.grid)
        self.assertTrue(res.found)
        # DFS produces a valid path (not necessarily shortest)
        self._verify_valid_contiguous_path(self.grid, res.path, (0, 0), (4, 4))
        self.assertGreaterEqual(res.path_length, 8)

    def test_dijkstra_unweighted_matches_bfs(self) -> None:
        res_bfs = bfs(self.grid)
        res_dijk = dijkstra(self.grid)
        self.assertTrue(res_dijk.found)
        # On uniform unweighted grid, Dijkstra must find an identical path length to BFS
        self.assertEqual(res_dijk.path_length, res_bfs.path_length)
        self.assertEqual(res_dijk.path_length, 8)
        self._verify_valid_contiguous_path(self.grid, res_dijk.path, (0, 0), (4, 4))

    def test_navigation_around_obstacles(self) -> None:
        # Create a vertical wall dividing the grid with an opening at the bottom
        # Obstacles at (0,2), (1,2), (2,2), (3,2)
        for r in range(4):
            self.grid.add_obstacle(r, 2)

        for algo_fn in (bfs, dfs, dijkstra):
            res = algo_fn(self.grid)
            self.assertTrue(res.found, f"{algo_fn.__name__} failed to find path around wall.")
            self._verify_valid_contiguous_path(self.grid, res.path, (0, 0), (4, 4))
            # The path must pass through the gap at row 4
            self.assertIn((4, 2), res.path)

    def test_unreachable_destination(self) -> None:
        # Enclose the destination (4, 4) completely: (3, 4) and (4, 3)
        self.grid.add_obstacle(3, 4)
        self.grid.add_obstacle(4, 3)

        for algo_fn in (bfs, dfs, dijkstra):
            res = algo_fn(self.grid)
            self.assertFalse(res.found, f"{algo_fn.__name__} found path to unreachable node.")
            self.assertEqual(res.path, [])
            self.assertEqual(res.path_length, 0)
            self.assertGreater(res.visited_count, 0)

    def test_start_equal_to_destination(self) -> None:
        # Edge case: start == dest
        self.grid.start = (2, 2)
        self.grid.destination = (2, 2)

        for algo_fn in (bfs, dfs, dijkstra):
            res = algo_fn(self.grid)
            self.assertTrue(res.found)
            self.assertEqual(res.path, [(2, 2)])
            self.assertEqual(res.path_length, 0)
            self.assertEqual(res.visited_count, 1)

    def test_invalid_and_out_of_bounds_positions(self) -> None:
        res_bfs = bfs(self.grid, start=(-1, 0), destination=(4, 4))
        self.assertFalse(res_bfs.found)
        self.assertIn("out of bounds", res_bfs.message.lower())

        res_dfs = dfs(self.grid, start=(0, 0), destination=(10, 10))
        self.assertFalse(res_dfs.found)
        self.assertIn("out of bounds", res_dfs.message.lower())

        res_dijk = dijkstra(self.grid, start=None, destination=None)
        # If grid has start=None
        self.grid.start = None
        res_dijk2 = dijkstra(self.grid)
        self.assertFalse(res_dijk2.found)

    def test_start_or_dest_is_obstacle(self) -> None:
        grid = Grid(4, 4)
        grid.obstacles.add((0, 0))
        res = bfs(grid, start=(0, 0), destination=(3, 3))
        self.assertFalse(res.found)
        self.assertIn("obstacle", res.message.lower())

    def test_dijkstra_weighted_grid_optimal_cost(self) -> None:
        """
        Dijkstra vs BFS on a weighted graph:
        BFS minimizes EDGE COUNT (steps).
        Dijkstra minimizes TOTAL COST.
        
        Setup:
          A 3x3 grid:
            (0,0) -> Start
            (0,2) -> End
          Direct path across row 0: (0,0) -> (0,1) -> (0,2) [2 steps].
          Detour path across row 1: (0,0) -> (1,0) -> (1,1) -> (1,2) -> (0,2) [4 steps].
          
          If cell (0,1) has high weight (cost = 50.0), while row 1 cells have weight = 1.0:
            Direct path cost: 50 + 1 = 51.
            Detour path cost: 1 + 1 + 1 + 1 = 4.
            
          Dijkstra MUST take the 4-step detour because 4 < 51.
          BFS MUST take the 2-step direct path because 2 < 4.
        """
        w_grid = Grid(3, 3)
        w_grid.set_start(0, 0)
        w_grid.set_destination(0, 2)
        w_grid.set_weight(0, 1, 50.0)

        res_bfs = bfs(w_grid)
        res_dijk = dijkstra(w_grid)

        self.assertTrue(res_bfs.found)
        self.assertTrue(res_dijk.found)

        # BFS chooses fewest steps
        self.assertEqual(res_bfs.path_length, 2)
        self.assertEqual(res_bfs.path, [(0, 0), (0, 1), (0, 2)])
        self.assertEqual(res_bfs.path_cost, 51.0)

        # Dijkstra chooses lowest total cost
        self.assertEqual(res_dijk.path_cost, 4.0)
        self.assertEqual(res_dijk.path_length, 4)
        self.assertEqual(res_dijk.path, [(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)])
        self.assertNotIn((0, 1), res_dijk.path)

    def test_reconstruct_path_edge_cases(self) -> None:
        # 1. start == dest
        self.assertEqual(reconstruct_path({}, (1, 1), (1, 1)), [(1, 1)])

        # 2. destination not in parent map
        self.assertEqual(reconstruct_path({(0, 0): None}, (0, 0), (3, 3)), [])

        # 3. Disconnected parent chain
        parent_map = {(2, 2): (1, 1), (1, 1): None}
        # Start requested is (0, 0), but chain terminates at (1, 1)
        self.assertEqual(reconstruct_path(parent_map, (0, 0), (2, 2)), [])

    def test_run_comparison_suite(self) -> None:
        results = run_comparison(self.grid)
        self.assertIn("BFS", results)
        self.assertIn("DFS", results)
        self.assertIn("Dijkstra", results)

        for name, res in results.items():
            self.assertTrue(res.found)
            self.assertGreater(res.visited_count, 0)
            self.assertGreaterEqual(res.execution_time_ms, 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

