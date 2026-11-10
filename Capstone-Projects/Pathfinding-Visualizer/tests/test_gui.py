#!/usr/bin/env python3
"""
================================================================================
UNIT TESTS: GUI & ANIMATION CONTROLLER
================================================================================
Verifies Tkinter GUI instantiation, AnimationController state machine,
pause/resume/reset mechanisms, maze generation, and event handling.
================================================================================
"""

import os
import sys
import unittest

# Ensure pathfinding_visualizer and gui are importable
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

from gui import AnimationController, PathfindingVisualizerGUI
from pathfinding_visualizer import Grid, PathResult, bfs, dfs, dijkstra


class DummyTkWidget:
    """Mock widget to test AnimationController logic in headless/unit-test environments."""

    def __init__(self) -> None:
        self.callbacks = {}
        self.counter = 0

    def after(self, delay_ms: int, callback) -> str:
        self.counter += 1
        timer_id = f"timer_{self.counter}"
        self.callbacks[timer_id] = callback
        return timer_id

    def after_cancel(self, timer_id: str) -> None:
        if timer_id in self.callbacks:
            del self.callbacks[timer_id]

    def trigger_step(self, timer_id: str) -> None:
        if timer_id in self.callbacks:
            cb = self.callbacks.pop(timer_id)
            cb()


class TestAnimationController(unittest.TestCase):
    """Test AnimationController state transitions, callbacks, and playback control."""

    def setUp(self) -> None:
        self.mock_widget = DummyTkWidget()
        self.controller = AnimationController(self.mock_widget)

    def test_initial_state(self) -> None:
        self.assertEqual(self.controller.state, AnimationController.STATE_IDLE)
        self.assertFalse(self.controller.is_active())
        self.assertFalse(self.controller.is_running())
        self.assertFalse(self.controller.is_paused())

    def test_start_state_and_scheduling(self) -> None:
        dummy_result = PathResult("BFS", True, [(0, 0), (0, 1)], 2, [(0, 0), (0, 1)], 1.0)
        self.controller.start(
            dummy_result,
            on_node_explored=lambda n, i: None,
            on_path_step=lambda p, i: None,
            on_completed=lambda r: None,
        )
        self.assertEqual(self.controller.state, AnimationController.STATE_RUNNING)
        self.assertTrue(self.controller.is_running())
        self.assertIsNotNone(self.controller.timer_id)

    def test_pause_and_resume(self) -> None:
        dummy_result = PathResult("BFS", True, [(0, 0), (0, 1)], 2, [(0, 0), (0, 1)], 1.0)
        self.controller.start(dummy_result, lambda n, i: None, lambda p, i: None, lambda r: None)

        self.controller.pause()
        self.assertEqual(self.controller.state, AnimationController.STATE_PAUSED)
        self.assertTrue(self.controller.is_paused())
        self.assertIsNone(self.controller.timer_id)

        self.controller.resume()
        self.assertEqual(self.controller.state, AnimationController.STATE_RUNNING)
        self.assertTrue(self.controller.is_running())
        self.assertIsNotNone(self.controller.timer_id)

    def test_reset(self) -> None:
        dummy_result = PathResult("BFS", True, [(0, 0)], 1, [(0, 0)], 1.0)
        self.controller.start(dummy_result, lambda n, i: None, lambda p, i: None, lambda r: None)
        self.controller.reset()
        self.assertEqual(self.controller.state, AnimationController.STATE_IDLE)
        self.assertEqual(len(self.controller.visited_order), 0)
        self.assertEqual(len(self.controller.path), 0)

    def test_step_execution_and_completion(self) -> None:
        dummy_result = PathResult("BFS", True, [(0, 0), (0, 1)], 2, [(0, 0), (0, 1)], 1.0)
        explored_nodes = []
        path_nodes = []
        completed = []

        self.controller.set_speed(20)  # batch size = 1
        self.controller.start(
            dummy_result,
            on_node_explored=lambda n, i: explored_nodes.append(n),
            on_path_step=lambda p, i: path_nodes.append(p),
            on_completed=lambda r: completed.append(r),
        )

        # Trigger step 1 (explores (0, 0))
        t1 = self.controller.timer_id
        self.mock_widget.trigger_step(t1)
        self.assertEqual(explored_nodes, [(0, 0)])

        # Trigger step 2 (explores (0, 1))
        t2 = self.controller.timer_id
        self.mock_widget.trigger_step(t2)
        self.assertEqual(explored_nodes, [(0, 0), (0, 1)])

        # Trigger step 3 (path (0, 0))
        t3 = self.controller.timer_id
        self.mock_widget.trigger_step(t3)
        self.assertEqual(path_nodes, [(0, 0)])

        # Trigger step 4 (path (0, 1))
        t4 = self.controller.timer_id
        self.mock_widget.trigger_step(t4)
        self.assertEqual(path_nodes, [(0, 0), (0, 1)])

        # Trigger step 5 (completion)
        t5 = self.controller.timer_id
        self.mock_widget.trigger_step(t5)
        self.assertEqual(self.controller.state, AnimationController.STATE_COMPLETED)
        self.assertEqual(len(completed), 1)


class TestMazeGeneration(unittest.TestCase):
    """Test procedural maze generation on the Grid."""

    def test_braided_maze_generation(self) -> None:
        grid = Grid(15, 25)
        grid.set_start(1, 1)
        grid.set_destination(13, 23)
        grid.generate_maze(mode="braided", seed=100)

        self.assertGreater(len(grid.obstacles), 20)
        # Ensure start and destination are never obstacles
        self.assertNotIn(grid.start, grid.obstacles)
        self.assertNotIn(grid.destination, grid.obstacles)

    def test_scatter_maze_generation(self) -> None:
        grid = Grid(10, 20)
        grid.set_start(0, 0)
        grid.set_destination(9, 19)
        grid.generate_maze(mode="scatter", seed=100)

        self.assertGreater(len(grid.obstacles), 10)
        self.assertNotIn((0, 0), grid.obstacles)
        self.assertNotIn((9, 19), grid.obstacles)


@unittest.skipUnless(TKINTER_AVAILABLE, "Tkinter is not available in environment")
class TestPathfindingVisualizerGUI(unittest.TestCase):
    """Test actual Tkinter GUI initialization, widget setup, and interactions."""

    def setUp(self) -> None:
        try:
            self.root = tk.Tk()
            self.root.withdraw()  # Run headless without window popup
            self.gui = PathfindingVisualizerGUI(self.root)
        except tk.TclError:
            self.skipTest("No X11 display / Wayland display available for Tk initialization.")

    def tearDown(self) -> None:
        if hasattr(self, "root") and self.root:
            self.root.destroy()

    def test_gui_initialization(self) -> None:
        self.assertEqual(self.gui.grid_rows, 22)
        self.assertEqual(self.gui.grid_cols, 45)
        self.assertIsNotNone(self.gui.grid.start)
        self.assertIsNotNone(self.gui.grid.destination)
        self.assertIsNotNone(self.gui.canvas)
        self.assertEqual(len(self.gui.canvas_rects), 22)
        self.assertEqual(len(self.gui.canvas_rects[0]), 45)

    def test_algorithm_switching(self) -> None:
        self.gui.selected_algo_var.set("DFS")
        self.gui._on_algorithm_selected()
        self.assertEqual(self.gui.stat_labels["Algorithm"].cget("text"), "DFS")

        self.gui.selected_algo_var.set("Dijkstra")
        self.gui._on_algorithm_selected()
        self.assertEqual(self.gui.stat_labels["Algorithm"].cget("text"), "Dijkstra")

    def test_cell_actions(self) -> None:
        # Drawing wall at (5, 5)
        self.gui._apply_cell_action((5, 5), self.gui.TOOL_WALL)
        self.assertTrue(self.gui.grid.is_obstacle(5, 5))

        # Erasing wall at (5, 5)
        self.gui._apply_cell_action((5, 5), self.gui.TOOL_ERASE)
        self.assertFalse(self.gui.grid.is_obstacle(5, 5))

        # Cannot place wall on start or destination
        self.gui._apply_cell_action(self.gui.grid.start, self.gui.TOOL_WALL)
        self.assertFalse(self.gui.grid.is_obstacle(*self.gui.grid.start))

    def test_clear_walls_and_reset(self) -> None:
        self.gui.grid.add_obstacle(2, 2)
        self.gui.grid.add_obstacle(3, 3)
        self.gui.on_click_clear_walls()
        self.assertEqual(len(self.gui.grid.obstacles), 0)

    def test_start_and_reset_visualization(self) -> None:
        self.gui.on_click_start()
        self.assertTrue(self.gui.animator.is_active())

        # Reset cancels animation
        self.gui.on_click_reset_visualization()
        self.assertFalse(self.gui.animator.is_active())
        self.assertEqual(self.gui.animator.state, AnimationController.STATE_IDLE)


if __name__ == "__main__":
    unittest.main(verbosity=2)

