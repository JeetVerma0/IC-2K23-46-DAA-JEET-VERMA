#!/usr/bin/env python3
"""
================================================================================
PATHFINDING VISUALIZER — GRAPHICAL APPLICATION (TKINTER)
A Graph-Based Pathfinding and Shortest Path Analysis System
================================================================================
Course: Data Structures and Algorithms Laboratory (IC-307D)
Language: Python 3.8+ (Standard Library: tkinter Only)
Zero External GUI Frameworks. Zero Third-Party Graph Packages.
All algorithms (BFS, DFS, Dijkstra) are reused directly from the manual core.
Non-blocking, event-driven step-by-step animation via Tkinter's root.after().
================================================================================
"""

import os
import sys
import time
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

# Ensure local module directory is in sys.path
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

try:
    import tkinter as tk
    from tkinter import font as tkfont
    from tkinter import messagebox, ttk
except ImportError as err:
    print(f"Error: Tkinter library is required to launch the GUI ({err}).")
    sys.exit(1)

from pathfinding_visualizer import (
    Grid,
    PathResult,
    bfs,
    dfs,
    dijkstra,
)


# ==============================================================================
# COLOR PALETTE (Modern Dark Theme — Catppuccin / Tokyo Dark Inspired)
# ==============================================================================

class Theme:
    # Canvas & Backgrounds
    BG_BASE: str = "#181825"        # Main window background
    BG_CARD: str = "#1e1e2e"        # Card / panel background
    BG_SIDEBAR: str = "#181825"     # Sidebar frame
    BORDER: str = "#313244"         # Widget & grid borders
    GRID_LINE: str = "#26283b"      # Subtle cell boundary

    # Grid Cell Colors
    CELL_EMPTY: str = "#1e1e2e"     # Empty passable terrain
    CELL_WALL: str = "#585b70"      # Impassable barrier wall
    CELL_START: str = "#2ecc71"     # Emerald Green (Start Node)
    CELL_DEST: str = "#e74c3c"      # Coral Red (Destination Node)
    CELL_EXPLORING: str = "#f1c40f" # Amber Gold (Currently exploring)
    CELL_VISITED: str = "#3498db"   # Luminous Dodger Blue (Visited)
    CELL_PATH: str = "#00ffff"      # Bright Electric Cyan (Final Path)

    # Text & Indicators
    TEXT_PRIMARY: str = "#cdd6f4"   # Bright crisp text
    TEXT_SECONDARY: str = "#a6adc8" # Subdued descriptor
    TEXT_MUTED: str = "#6c7086"     # Footnotes and hints
    TEXT_ACCENT: str = "#89b4fa"    # Highlight blue

    # Button Colors
    BTN_PRIMARY: str = "#27ae60"    # Start (Green)
    BTN_PRIMARY_HOVER: str = "#2ecc71"
    BTN_WARNING: str = "#d35400"    # Pause (Amber)
    BTN_WARNING_HOVER: str = "#e67e22"
    BTN_DANGER: str = "#c0392b"     # Clear (Red)
    BTN_DANGER_HOVER: str = "#e74c3c"
    BTN_SECONDARY: str = "#45475a"  # Reset / Utility (Gray)
    BTN_SECONDARY_HOVER: str = "#585b70"
    BTN_PURPLE: str = "#8e44ad"     # Maze (Purple)
    BTN_PURPLE_HOVER: str = "#9b59b6"


# ==============================================================================
# ANIMATION CONTROLLER
# ==============================================================================

class AnimationController:
    """
    Manages non-blocking step-by-step playback of pathfinding exploration
    and path reconstruction using Tkinter's event-loop after() mechanism.
    
    Guarantees:
      - Never calls time.sleep() inside the GUI main thread.
      - Supports Start, Pause, Resume, Reset, and dynamic speed adjustment.
      - Prevents concurrent executions via strict state management.
    """

    STATE_IDLE: str = "IDLE"
    STATE_RUNNING: str = "RUNNING"
    STATE_PAUSED: str = "PAUSED"
    STATE_COMPLETED: str = "COMPLETED"

    def __init__(self, master_widget: tk.Widget) -> None:
        self.master: tk.Widget = master_widget
        self.state: str = self.STATE_IDLE
        self.delay_ms: int = 20

        self.result: Optional[PathResult] = None
        self.visited_order: List[Tuple[int, int]] = []
        self.path: List[Tuple[int, int]] = []

        self.visited_idx: int = 0
        self.path_idx: int = 0
        self.timer_id: Optional[str] = None

        # Callbacks
        self.on_node_explored: Optional[Callable[[Tuple[int, int], int], None]] = None
        self.on_path_step: Optional[Callable[[Tuple[int, int], int], None]] = None
        self.on_completed: Optional[Callable[[PathResult], None]] = None
        self.on_state_changed: Optional[Callable[[str], None]] = None

    def set_speed(self, delay_ms: int) -> None:
        """Dynamically update animation speed interval."""
        self.delay_ms = max(1, delay_ms)

    def is_running(self) -> bool:
        return self.state == self.STATE_RUNNING

    def is_paused(self) -> bool:
        return self.state == self.STATE_PAUSED

    def is_active(self) -> bool:
        return self.state in (self.STATE_RUNNING, self.STATE_PAUSED)

    def _set_state(self, new_state: str) -> None:
        self.state = new_state
        if self.on_state_changed:
            self.on_state_changed(new_state)

    def start(
        self,
        result: PathResult,
        on_node_explored: Callable[[Tuple[int, int], int], None],
        on_path_step: Callable[[Tuple[int, int], int], None],
        on_completed: Callable[[PathResult], None],
    ) -> None:
        """Initialize and launch animation of an algorithm result."""
        if self.is_active():
            self.reset()

        self.result = result
        self.visited_order = list(result.visited_order)
        self.path = list(result.path) if result.found else []

        self.visited_idx = 0
        self.path_idx = 0

        self.on_node_explored = on_node_explored
        self.on_path_step = on_path_step
        self.on_completed = on_completed

        self._set_state(self.STATE_RUNNING)
        self._schedule_step()

    def pause(self) -> None:
        """Pause the running animation."""
        if self.state == self.STATE_RUNNING:
            if self.timer_id is not None:
                self.master.after_cancel(self.timer_id)
                self.timer_id = None
            self._set_state(self.STATE_PAUSED)

    def resume(self) -> None:
        """Resume animation from the paused step."""
        if self.state == self.STATE_PAUSED:
            self._set_state(self.STATE_RUNNING)
            self._schedule_step()

    def reset(self) -> None:
        """Cancel any pending animation and reset state to IDLE."""
        if self.timer_id is not None:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None
        self.result = None
        self.visited_order.clear()
        self.path.clear()
        self.visited_idx = 0
        self.path_idx = 0
        self._set_state(self.STATE_IDLE)

    def _schedule_step(self) -> None:
        if self.state != self.STATE_RUNNING:
            return
        self.timer_id = self.master.after(self.delay_ms, self._step)

    def _step(self) -> None:
        if self.state != self.STATE_RUNNING:
            return

        # Adaptive batching: When speed is high (<10ms), process multiple nodes per tick
        batch_size = 1
        if self.delay_ms <= 3:
            batch_size = 6
        elif self.delay_ms <= 8:
            batch_size = 3

        # Phase 1: Exploration
        if self.visited_idx < len(self.visited_order):
            for _ in range(batch_size):
                if self.visited_idx >= len(self.visited_order):
                    break
                curr_node = self.visited_order[self.visited_idx]
                self.visited_idx += 1
                if self.on_node_explored:
                    self.on_node_explored(curr_node, self.visited_idx)
            self._schedule_step()
            return

        # Phase 2: Final Path Reconstruction Animation
        if self.path_idx < len(self.path):
            curr_path_node = self.path[self.path_idx]
            self.path_idx += 1
            if self.on_path_step:
                self.on_path_step(curr_path_node, self.path_idx)
            # Path draws with a slightly more deliberate pace for clarity
            path_delay = max(15, self.delay_ms)
            self.timer_id = self.master.after(path_delay, self._step)
            return

        # Phase 3: Completion
        self._set_state(self.STATE_COMPLETED)
        if self.on_completed and self.result is not None:
            self.on_completed(self.result)


# ==============================================================================
# MAIN GUI APPLICATION
# ==============================================================================

class PathfindingVisualizerGUI:
    """
    Tkinter Graphical Application for Pathfinding and Shortest Path Analysis.
    """

    TOOL_WALL: str = "wall"
    TOOL_ERASE: str = "erase"
    TOOL_START: str = "start"
    TOOL_DEST: str = "dest"

    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.root.title("Pathfinding Visualizer — IC-307D DSA Laboratory")
        self.root.geometry("1240x820")
        self.root.minsize(980, 680)
        self.root.configure(bg=Theme.BG_BASE)

        # Initialize Default 22x45 Grid
        self.grid_rows: int = 22
        self.grid_cols: int = 45
        self.grid: Grid = Grid(rows=self.grid_rows, cols=self.grid_cols)
        self.grid.set_start(11, 6)
        self.grid.set_destination(11, 38)

        # Default obstacle wall
        for r in range(4, 18):
            self.grid.add_obstacle(r, 22)

        # Application State
        self.selected_algo_var: tk.StringVar = tk.StringVar(value="BFS")
        self.current_tool: str = self.TOOL_WALL
        self.is_mouse_down: bool = False
        self.dragging_node: Optional[str] = None  # "start" or "dest"
        self.last_cell: Optional[Tuple[int, int]] = None

        # Tracking Exploration Nodes on Canvas
        self.canvas_rects: List[List[int]] = []
        self.canvas_texts: List[List[int]] = []
        self.last_explored_cell: Optional[Tuple[int, int]] = None
        self.explored_cells: Set[Tuple[int, int]] = set()
        self.path_cells: Set[Tuple[int, int]] = set()

        # Canvas Dimensions
        self.cell_w: float = 20.0
        self.cell_h: float = 20.0
        self.canvas_offset_x: float = 10.0
        self.canvas_offset_y: float = 10.0

        # Animation Controller
        self.animator: AnimationController = AnimationController(self.root)
        self.animator.on_state_changed = self._on_animator_state_changed

        # Configure Fonts
        self._init_fonts()

        # Build GUI Components
        self._create_header()
        self._create_main_layout()
        self._create_status_bar()

        # Canvas Event Bindings
        self._bind_canvas_events()

        # Initial Draw
        self.root.update_idletasks()
        self._rebuild_canvas_grid()
        self._update_stats_display(None, status_override="READY")

    def _init_fonts(self) -> None:
        self.font_title = tkfont.Font(family="Helvetica", size=15, weight="bold")
        self.font_subtitle = tkfont.Font(family="Helvetica", size=9)
        self.font_section = tkfont.Font(family="Helvetica", size=10, weight="bold")
        self.font_body = tkfont.Font(family="Helvetica", size=9)
        self.font_btn = tkfont.Font(family="Helvetica", size=9, weight="bold")
        self.font_stat_val = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.font_cell = tkfont.Font(family="Helvetica", size=8, weight="bold")

    # ==========================================================================
    # UI CONSTRUCTION
    # ==========================================================================

    def _create_header(self) -> None:
        header_frame = tk.Frame(self.root, bg=Theme.BG_CARD, height=64, padx=18, pady=8)
        header_frame.pack(side=tk.TOP, fill=tk.X)

        title_box = tk.Frame(header_frame, bg=Theme.BG_CARD)
        title_box.pack(side=tk.LEFT)

        lbl_title = tk.Label(
            title_box,
            text="PATHFINDING VISUALIZER",
            font=self.font_title,
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_CARD,
        )
        lbl_title.pack(anchor="w")

        lbl_sub = tk.Label(
            title_box,
            text="Graph-Based Traversal & Shortest Path Analysis System • Manual Queue, Stack & Min-Heap",
            font=self.font_subtitle,
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_CARD,
        )
        lbl_sub.pack(anchor="w")

        # Top Right Badges
        badges_box = tk.Frame(header_frame, bg=Theme.BG_CARD)
        badges_box.pack(side=tk.RIGHT, pady=4)

        b1 = tk.Label(badges_box, text="IC-307D DSA Lab", font=self.font_body, fg="#89b4fa", bg="#313244", padx=8, pady=3)
        b1.pack(side=tk.LEFT, padx=4)
        b2 = tk.Label(badges_box, text="Zero External Dependencies", font=self.font_body, fg="#a6e3a1", bg="#313244", padx=8, pady=3)
        b2.pack(side=tk.LEFT, padx=4)

    def _create_main_layout(self) -> None:
        self.main_container = tk.Frame(self.root, bg=Theme.BG_BASE)
        self.main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=12, pady=10)

        # Left Control Sidebar
        self.sidebar_frame = tk.Frame(self.main_container, bg=Theme.BG_CARD, width=330, padx=14, pady=12)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.sidebar_frame.pack_propagate(False)

        # Right Grid Canvas Frame
        self.canvas_container = tk.Frame(self.main_container, bg=Theme.BG_CARD, padx=8, pady=8)
        self.canvas_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._build_sidebar_contents()
        self._build_canvas()

    def _build_sidebar_contents(self) -> None:
        # 1. Algorithm Selection Box
        self._create_section_label(self.sidebar_frame, "ALGORITHM SELECTION")

        algo_box = tk.Frame(self.sidebar_frame, bg=Theme.BG_CARD)
        algo_box.pack(fill=tk.X, pady=(4, 10))

        algos = [
            ("BFS", "Breadth-First Search (Shortest Unweighted)"),
            ("DFS", "Depth-First Search (Deep Traversal)"),
            ("Dijkstra", "Dijkstra's Algorithm (Optimal Min-Cost)"),
        ]

        self.algo_radios = []
        for val, desc in algos:
            r_frame = tk.Frame(algo_box, bg=Theme.BG_CARD)
            r_frame.pack(fill=tk.X, pady=2)
            rb = tk.Radiobutton(
                r_frame,
                text=val,
                variable=self.selected_algo_var,
                value=val,
                font=self.font_btn,
                fg=Theme.TEXT_PRIMARY,
                bg=Theme.BG_CARD,
                selectcolor=Theme.BORDER,
                activebackground=Theme.BG_CARD,
                activeforeground=Theme.TEXT_PRIMARY,
                command=self._on_algorithm_selected,
            )
            rb.pack(side=tk.LEFT)
            lbl_desc = tk.Label(r_frame, text=f"— {desc}", font=self.font_subtitle, fg=Theme.TEXT_SECONDARY, bg=Theme.BG_CARD)
            lbl_desc.pack(side=tk.LEFT, padx=4)
            self.algo_radios.append(rb)

        # 2. Action Buttons Box
        self._create_section_label(self.sidebar_frame, "CONTROLS & EXECUTION")

        btn_box = tk.Frame(self.sidebar_frame, bg=Theme.BG_CARD)
        btn_box.pack(fill=tk.X, pady=(4, 10))

        self.btn_start = self._create_button(btn_box, "▶ START VISUALIZATION", Theme.BTN_PRIMARY, Theme.BTN_PRIMARY_HOVER, self.on_click_start)
        self.btn_start.pack(fill=tk.X, pady=3)

        pause_box = tk.Frame(btn_box, bg=Theme.BG_CARD)
        pause_box.pack(fill=tk.X, pady=2)

        self.btn_pause = self._create_button(pause_box, "⏸ PAUSE", Theme.BTN_WARNING, Theme.BTN_WARNING_HOVER, self.on_click_pause)
        self.btn_pause.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        self.btn_resume = self._create_button(pause_box, "⏯ RESUME", Theme.BTN_SECONDARY, Theme.BTN_SECONDARY_HOVER, self.on_click_resume)
        self.btn_resume.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))
        self.btn_resume.config(state=tk.DISABLED)

        self.btn_reset = self._create_button(btn_box, "↺ RESET VISUALIZATION", Theme.BTN_SECONDARY, Theme.BTN_SECONDARY_HOVER, self.on_click_reset_visualization)
        self.btn_reset.pack(fill=tk.X, pady=2)

        util_box = tk.Frame(btn_box, bg=Theme.BG_CARD)
        util_box.pack(fill=tk.X, pady=2)

        self.btn_clear = self._create_button(util_box, "✕ CLEAR WALLS", Theme.BTN_DANGER, Theme.BTN_DANGER_HOVER, self.on_click_clear_walls)
        self.btn_clear.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        self.btn_maze = self._create_button(util_box, "⚡ MAZE", Theme.BTN_PURPLE, Theme.BTN_PURPLE_HOVER, self.on_click_generate_maze)
        self.btn_maze.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))

        # 3. Interactive Mouse Tool Selector
        self._create_section_label(self.sidebar_frame, "MOUSE EDITING TOOL")

        tool_box = tk.Frame(self.sidebar_frame, bg=Theme.BG_CARD)
        tool_box.pack(fill=tk.X, pady=(4, 10))

        self.tool_buttons = {}
        tool_defs = [
            (self.TOOL_WALL, "Draw Wall", Theme.CELL_WALL),
            (self.TOOL_ERASE, "Erase", "#2a2b3d"),
            (self.TOOL_START, "Move Start (S)", Theme.CELL_START),
            (self.TOOL_DEST, "Move End (E)", Theme.CELL_DEST),
        ]

        row1 = tk.Frame(tool_box, bg=Theme.BG_CARD)
        row1.pack(fill=tk.X, pady=2)
        row2 = tk.Frame(tool_box, bg=Theme.BG_CARD)
        row2.pack(fill=tk.X, pady=2)

        for i, (tool_id, label, color) in enumerate(tool_defs):
            parent = row1 if i < 2 else row2
            btn = tk.Button(
                parent,
                text=label,
                font=self.font_subtitle,
                fg=Theme.TEXT_PRIMARY,
                bg=color,
                activebackground=Theme.BORDER,
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda t=tool_id: self._select_tool(t),
            )
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
            self.tool_buttons[tool_id] = btn

        self._select_tool(self.TOOL_WALL)

        # 4. Animation Speed Slider
        self._create_section_label(self.sidebar_frame, "ANIMATION SPEED")

        speed_frame = tk.Frame(self.sidebar_frame, bg=Theme.BG_CARD)
        speed_frame.pack(fill=tk.X, pady=(2, 10))

        self.lbl_speed_val = tk.Label(
            speed_frame,
            text="Interval: 20 ms (Fast)",
            font=self.font_subtitle,
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_CARD,
        )
        self.lbl_speed_val.pack(anchor="w")

        self.speed_slider = ttk.Scale(
            speed_frame,
            from_=1,
            to=100,
            value=20,
            orient=tk.HORIZONTAL,
            command=self._on_speed_slider_change,
        )
        self.speed_slider.pack(fill=tk.X, pady=3)

        # 5. Live Statistics Panel
        self._create_section_label(self.sidebar_frame, "STATISTICS & BENCHMARK")

        self.stats_frame = tk.Frame(self.sidebar_frame, bg=Theme.BORDER, padx=1, pady=1)
        self.stats_frame.pack(fill=tk.X, pady=(4, 10))

        stats_inner = tk.Frame(self.stats_frame, bg=Theme.BG_BASE, padx=10, pady=8)
        stats_inner.pack(fill=tk.X)

        self.stat_labels: Dict[str, tk.Label] = {}
        stat_rows = [
            ("Status", "READY"),
            ("Algorithm", "BFS"),
            ("Nodes Explored", "0"),
            ("Path Length", "0 steps"),
            ("Traversal Cost", "0.00"),
            ("Compute Time", "0.0000 ms"),
        ]

        for key, val in stat_rows:
            r = tk.Frame(stats_inner, bg=Theme.BG_BASE)
            r.pack(fill=tk.X, pady=1)
            tk.Label(r, text=key + ":", font=self.font_subtitle, fg=Theme.TEXT_SECONDARY, bg=Theme.BG_BASE).pack(side=tk.LEFT)
            lbl_val = tk.Label(r, text=val, font=self.font_stat_val if key == "Status" else self.font_subtitle, fg=Theme.TEXT_PRIMARY, bg=Theme.BG_BASE)
            lbl_val.pack(side=tk.RIGHT)
            self.stat_labels[key] = lbl_val

        lbl_footnote = tk.Label(
            stats_inner,
            text="*Execution time measured via time.perf_counter() excluding animation latency.",
            font=tkfont.Font(size=7),
            fg=Theme.TEXT_MUTED,
            bg=Theme.BG_BASE,
            wraplength=280,
            justify="left",
        )
        lbl_footnote.pack(anchor="w", pady=(4, 0))

        # 6. Visual Legend
        self._create_section_label(self.sidebar_frame, "LEGEND")

        legend_box = tk.Frame(self.sidebar_frame, bg=Theme.BG_CARD)
        legend_box.pack(fill=tk.X, pady=(2, 0))

        legend_items = [
            ("Start", Theme.CELL_START),
            ("Destination", Theme.CELL_DEST),
            ("Wall", Theme.CELL_WALL),
            ("Exploring", Theme.CELL_EXPLORING),
            ("Visited", Theme.CELL_VISITED),
            ("Final Path", Theme.CELL_PATH),
        ]

        col1 = tk.Frame(legend_box, bg=Theme.BG_CARD)
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        col2 = tk.Frame(legend_box, bg=Theme.BG_CARD)
        col2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        for i, (name, col) in enumerate(legend_items):
            parent = col1 if i % 2 == 0 else col2
            item_f = tk.Frame(parent, bg=Theme.BG_CARD)
            item_f.pack(anchor="w", pady=2)
            color_swatch = tk.Label(item_f, text="  ", bg=col, font=("Courier", 7))
            color_swatch.pack(side=tk.LEFT, padx=(0, 6))
            lbl = tk.Label(item_f, text=name, font=self.font_subtitle, fg=Theme.TEXT_SECONDARY, bg=Theme.BG_CARD)
            lbl.pack(side=tk.LEFT)

    def _build_canvas(self) -> None:
        self.canvas = tk.Canvas(
            self.canvas_container,
            bg=Theme.BG_BASE,
            highlightthickness=1,
            highlightbackground=Theme.BORDER,
            cursor="crosshair",
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def _create_status_bar(self) -> None:
        self.status_bar = tk.Frame(self.root, bg=Theme.BG_CARD, height=26, padx=16, pady=4)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.lbl_coord = tk.Label(
            self.status_bar,
            text="Hover over grid for coordinates",
            font=self.font_subtitle,
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_CARD,
        )
        self.lbl_coord.pack(side=tk.LEFT)

        self.lbl_hint = tk.Label(
            self.status_bar,
            text="Left-Click & Drag: Draw Walls | Right-Click / Shift+Click: Erase | Drag Start (S) or End (E) to relocate",
            font=self.font_subtitle,
            fg=Theme.TEXT_MUTED,
            bg=Theme.BG_CARD,
        )
        self.lbl_hint.pack(side=tk.RIGHT)

    def _create_section_label(self, parent: tk.Widget, text: str) -> None:
        lbl = tk.Label(
            parent,
            text=text,
            font=self.font_section,
            fg=Theme.TEXT_ACCENT,
            bg=Theme.BG_CARD,
        )
        lbl.pack(anchor="w", pady=(6, 2))

    def _create_button(
        self,
        parent: tk.Widget,
        text: str,
        bg_color: str,
        hover_color: str,
        command: Callable[[], None],
    ) -> tk.Button:
        btn = tk.Button(
            parent,
            text=text,
            font=self.font_btn,
            fg="#ffffff",
            bg=bg_color,
            activebackground=hover_color,
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=5,
            command=command,
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color) if btn["state"] != tk.DISABLED else None)
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color) if btn["state"] != tk.DISABLED else None)
        return btn

    def _select_tool(self, tool_id: str) -> None:
        self.current_tool = tool_id
        for tid, btn in self.tool_buttons.items():
            if tid == tool_id:
                btn.config(relief=tk.SUNKEN, bd=2)
            else:
                btn.config(relief=tk.FLAT, bd=0)

    # ==========================================================================
    # CANVAS GRID RENDERING
    # ==========================================================================

    def _on_canvas_resize(self, event: tk.Event) -> None:
        w = max(200, event.width - 20)
        h = max(200, event.height - 20)

        new_cell_w = max(8.0, w / self.grid.cols)
        new_cell_h = max(8.0, h / self.grid.rows)

        # Only rebuild if change is noticeable
        if abs(new_cell_w - self.cell_w) > 0.5 or abs(new_cell_h - self.cell_h) > 0.5:
            self.cell_w = new_cell_w
            self.cell_h = new_cell_h
            self.canvas_offset_x = (event.width - (self.cell_w * self.grid.cols)) / 2.0
            self.canvas_offset_y = (event.height - (self.cell_h * self.grid.rows)) / 2.0
            self._rebuild_canvas_grid()

    def _rebuild_canvas_grid(self) -> None:
        self.canvas.delete("all")
        self.canvas_rects = [[0 for _ in range(self.grid.cols)] for _ in range(self.grid.rows)]
        self.canvas_texts = [[0 for _ in range(self.grid.cols)] for _ in range(self.grid.rows)]

        ox = self.canvas_offset_x
        oy = self.canvas_offset_y
        cw = self.cell_w
        ch = self.cell_h

        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                x1 = ox + c * cw
                y1 = oy + r * ch
                x2 = x1 + cw
                y2 = y1 + ch

                fill_col = self._get_cell_color(r, c)
                rect_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill_col,
                    outline=Theme.GRID_LINE,
                    width=1,
                    tags=(f"cell_{r}_{c}", "grid_cell"),
                )
                self.canvas_rects[r][c] = rect_id

                # Text markers for Start (S) and Destination (E)
                text_id = 0
                if (r, c) == self.grid.start:
                    text_id = self.canvas.create_text(
                        (x1 + x2) / 2, (y1 + y2) / 2,
                        text="S",
                        fill="#ffffff",
                        font=self.font_cell,
                        tags="marker_text",
                    )
                elif (r, c) == self.grid.destination:
                    text_id = self.canvas.create_text(
                        (x1 + x2) / 2, (y1 + y2) / 2,
                        text="E",
                        fill="#ffffff",
                        font=self.font_cell,
                        tags="marker_text",
                    )
                self.canvas_texts[r][c] = text_id

    def _get_cell_color(self, r: int, c: int) -> str:
        pos = (r, c)
        if pos == self.grid.start:
            return Theme.CELL_START
        if pos == self.grid.destination:
            return Theme.CELL_DEST
        if pos in self.path_cells:
            return Theme.CELL_PATH
        if pos == self.last_explored_cell:
            return Theme.CELL_EXPLORING
        if pos in self.explored_cells:
            return Theme.CELL_VISITED
        if pos in self.grid.obstacles:
            return Theme.CELL_WALL
        return Theme.CELL_EMPTY

    def _update_single_cell_view(self, r: int, c: int) -> None:
        """Instant O(1) item update on the Canvas without full redraw."""
        if not (0 <= r < self.grid.rows and 0 <= c < self.grid.cols):
            return
        rect_id = self.canvas_rects[r][c]
        color = self._get_cell_color(r, c)
        self.canvas.itemconfig(rect_id, fill=color)

        # Update text markers
        old_text = self.canvas_texts[r][c]
        if old_text:
            self.canvas.delete(old_text)
            self.canvas_texts[r][c] = 0

        pos = (r, c)
        if pos == self.grid.start or pos == self.grid.destination:
            x1 = self.canvas_offset_x + c * self.cell_w
            y1 = self.canvas_offset_y + r * self.cell_h
            x2 = x1 + self.cell_w
            y2 = y1 + self.cell_h
            symbol = "S" if pos == self.grid.start else "E"
            tid = self.canvas.create_text(
                (x1 + x2) / 2, (y1 + y2) / 2,
                text=symbol,
                fill="#ffffff",
                font=self.font_cell,
                tags="marker_text",
            )
            self.canvas_texts[r][c] = tid

    # ==========================================================================
    # MOUSE EVENT HANDLERS
    # ==========================================================================

    def _bind_canvas_events(self) -> None:
        self.canvas.bind("<ButtonPress-1>", self._on_mouse_press_left)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag_left)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_release_left)

        self.canvas.bind("<ButtonPress-3>", self._on_mouse_press_right)
        self.canvas.bind("<B3-Motion>", self._on_mouse_drag_right)

        self.canvas.bind("<Motion>", self._on_mouse_motion)
        self.canvas.bind("<Leave>", lambda e: self.lbl_coord.config(text="Hover over grid for coordinates"))

    def _coords_to_cell(self, x: float, y: float) -> Optional[Tuple[int, int]]:
        ox = self.canvas_offset_x
        oy = self.canvas_offset_y
        c = int((x - ox) // self.cell_w)
        r = int((y - oy) // self.cell_h)
        if 0 <= r < self.grid.rows and 0 <= c < self.grid.cols:
            return (r, c)
        return None

    def _on_mouse_motion(self, event: tk.Event) -> None:
        cell = self._coords_to_cell(event.x, event.y)
        if cell:
            r, c = cell
            status = "EMPTY"
            if cell == self.grid.start:
                status = "START NODE"
            elif cell == self.grid.destination:
                status = "DESTINATION NODE"
            elif cell in self.grid.obstacles:
                status = "WALL OBSTACLE"
            elif cell in self.path_cells:
                status = "FINAL PATH"
            elif cell in self.explored_cells:
                status = "VISITED"
            self.lbl_coord.config(text=f"Cell ({r:2d}, {c:2d}) | State: {status}")

    def _on_mouse_press_left(self, event: tk.Event) -> None:
        if self.animator.is_active():
            return
        cell = self._coords_to_cell(event.x, event.y)
        if not cell:
            return

        self.is_mouse_down = True
        self.last_cell = cell

        # Check if Start or Destination was clicked for direct dragging
        if cell == self.grid.start:
            self.dragging_node = "start"
            return
        elif cell == self.grid.destination:
            self.dragging_node = "dest"
            return

        # Shift+Click behaves as an eraser
        if event.state & 0x0001:  # Shift mask
            self._apply_cell_action(cell, self.TOOL_ERASE)
        else:
            self._apply_cell_action(cell, self.current_tool)

    def _on_mouse_drag_left(self, event: tk.Event) -> None:
        if not self.is_mouse_down or self.animator.is_active():
            return
        cell = self._coords_to_cell(event.x, event.y)
        if not cell or cell == self.last_cell:
            return

        self.last_cell = cell

        if self.dragging_node == "start":
            if cell != self.grid.destination and cell not in self.grid.obstacles:
                old_start = self.grid.start
                self.grid.start = cell
                if old_start:
                    self._update_single_cell_view(*old_start)
                self._update_single_cell_view(*cell)
        elif self.dragging_node == "dest":
            if cell != self.grid.start and cell not in self.grid.obstacles:
                old_dest = self.grid.destination
                self.grid.destination = cell
                if old_dest:
                    self._update_single_cell_view(*old_dest)
                self._update_single_cell_view(*cell)
        else:
            if event.state & 0x0001:
                self._apply_cell_action(cell, self.TOOL_ERASE)
            else:
                self._apply_cell_action(cell, self.current_tool)

    def _on_mouse_release_left(self, event: tk.Event) -> None:
        self.is_mouse_down = False
        self.dragging_node = None
        self.last_cell = None

    def _on_mouse_press_right(self, event: tk.Event) -> None:
        if self.animator.is_active():
            return
        cell = self._coords_to_cell(event.x, event.y)
        if cell:
            self._apply_cell_action(cell, self.TOOL_ERASE)

    def _on_mouse_drag_right(self, event: tk.Event) -> None:
        if self.animator.is_active():
            return
        cell = self._coords_to_cell(event.x, event.y)
        if cell and cell != self.last_cell:
            self.last_cell = cell
            self._apply_cell_action(cell, self.TOOL_ERASE)

    def _apply_cell_action(self, cell: Tuple[int, int], tool: str) -> None:
        r, c = cell

        # Never overwrite start or destination with wall
        if tool == self.TOOL_WALL:
            if cell != self.grid.start and cell != self.grid.destination:
                self.grid.add_obstacle(r, c)
                self._update_single_cell_view(r, c)
        elif tool == self.TOOL_ERASE:
            if cell in self.grid.obstacles:
                self.grid.remove_obstacle(r, c)
                self._update_single_cell_view(r, c)
        elif tool == self.TOOL_START:
            if cell != self.grid.destination and cell not in self.grid.obstacles:
                old_s = self.grid.start
                self.grid.start = cell
                if old_s:
                    self._update_single_cell_view(*old_s)
                self._update_single_cell_view(r, c)
        elif tool == self.TOOL_DEST:
            if cell != self.grid.start and cell not in self.grid.obstacles:
                old_d = self.grid.destination
                self.grid.destination = cell
                if old_d:
                    self._update_single_cell_view(*old_d)
                self._update_single_cell_view(r, c)

    # ==========================================================================
    # CONTROLLER & BUTTON ACTIONS
    # ==========================================================================

    def on_click_start(self) -> None:
        if self.animator.is_active():
            return

        # Clear any prior visualization paths
        self._clear_visualization_layers()

        algo_name = self.selected_algo_var.get()
        self._update_stats_display(None, status_override="RUNNING...")

        # Run pure algorithmic calculation (high-resolution timer)
        if algo_name == "BFS":
            result = bfs(self.grid)
        elif algo_name == "DFS":
            result = dfs(self.grid)
        elif algo_name == "Dijkstra":
            result = dijkstra(self.grid)
        else:
            messagebox.showerror("Error", f"Unknown algorithm {algo_name}")
            return

        # Launch non-blocking animation via AnimationController
        self.animator.start(
            result=result,
            on_node_explored=self._on_animation_node_explored,
            on_path_step=self._on_animation_path_step,
            on_completed=self._on_animation_completed,
        )

    def on_click_pause(self) -> None:
        self.animator.pause()

    def on_click_resume(self) -> None:
        self.animator.resume()

    def on_click_reset_visualization(self) -> None:
        self.animator.reset()
        self._clear_visualization_layers()
        self._rebuild_canvas_grid()
        self._update_stats_display(None, status_override="READY")

    def on_click_clear_walls(self) -> None:
        if self.animator.is_active():
            return
        self.grid.clear_obstacles()
        self._clear_visualization_layers()
        self._rebuild_canvas_grid()
        self._update_stats_display(None, status_override="READY")

    def on_click_generate_maze(self) -> None:
        if self.animator.is_active():
            return
        self.animator.reset()
        self._clear_visualization_layers()
        self.grid.generate_maze(mode="braided")
        self._rebuild_canvas_grid()
        self._update_stats_display(None, status_override="MAZE READY")

    def _on_speed_slider_change(self, val_str: str) -> None:
        val = int(float(val_str))
        self.animator.set_speed(val)
        speed_label = "Instant" if val <= 1 else ("Fast" if val <= 25 else ("Normal" if val <= 60 else "Slow"))
        self.lbl_speed_val.config(text=f"Interval: {val} ms ({speed_label})")

    def _on_algorithm_selected(self) -> None:
        algo = self.selected_algo_var.get()
        self.stat_labels["Algorithm"].config(text=algo)

    # ==========================================================================
    # ANIMATION STEP CALLBACKS
    # ==========================================================================

    def _on_animation_node_explored(self, curr_node: Tuple[int, int], visited_count: int) -> None:
        # Re-color previous exploring node to Visited
        if self.last_explored_cell and self.last_explored_cell != self.grid.start and self.last_explored_cell != self.grid.destination:
            self.explored_cells.add(self.last_explored_cell)
            self._update_single_cell_view(*self.last_explored_cell)

        # Highlight current node
        self.last_explored_cell = curr_node
        if curr_node != self.grid.start and curr_node != self.grid.destination:
            self._update_single_cell_view(*curr_node)

        # Update live explored counter
        self.stat_labels["Nodes Explored"].config(text=str(visited_count))

    def _on_animation_path_step(self, path_node: Tuple[int, int], path_step_count: int) -> None:
        # Finalize any lingering exploring cell
        if self.last_explored_cell and self.last_explored_cell != self.grid.start and self.last_explored_cell != self.grid.destination:
            self.explored_cells.add(self.last_explored_cell)
            self._update_single_cell_view(*self.last_explored_cell)
            self.last_explored_cell = None

        if path_node != self.grid.start and path_node != self.grid.destination:
            self.path_cells.add(path_node)
            self._update_single_cell_view(*path_node)

        self.stat_labels["Path Length"].config(text=f"{path_step_count} steps")

    def _on_animation_completed(self, result: PathResult) -> None:
        if self.last_explored_cell and self.last_explored_cell != self.grid.start and self.last_explored_cell != self.grid.destination:
            self.explored_cells.add(self.last_explored_cell)
            self._update_single_cell_view(*self.last_explored_cell)
            self.last_explored_cell = None

        status_text = "PATH FOUND" if result.found else "NO PATH FOUND"
        status_color = Theme.CELL_START if result.found else Theme.CELL_DEST
        self.stat_labels["Status"].config(text=status_text, fg=status_color)
        self._update_stats_display(result)

    def _on_animator_state_changed(self, state: str) -> None:
        if state == AnimationController.STATE_RUNNING:
            self.btn_start.config(state=tk.DISABLED)
            self.btn_pause.config(state=tk.NORMAL)
            self.btn_resume.config(state=tk.DISABLED)
            self.btn_clear.config(state=tk.DISABLED)
            self.btn_maze.config(state=tk.DISABLED)
            for rb in self.algo_radios:
                rb.config(state=tk.DISABLED)
            self.stat_labels["Status"].config(text="EXPLORING...", fg=Theme.CELL_EXPLORING)
        elif state == AnimationController.STATE_PAUSED:
            self.btn_start.config(state=tk.DISABLED)
            self.btn_pause.config(state=tk.DISABLED)
            self.btn_resume.config(state=tk.NORMAL)
            self.stat_labels["Status"].config(text="PAUSED", fg=Theme.CELL_EXPLORING)
        else:  # IDLE or COMPLETED
            self.btn_start.config(state=tk.NORMAL)
            self.btn_pause.config(state=tk.NORMAL)
            self.btn_resume.config(state=tk.DISABLED)
            self.btn_clear.config(state=tk.NORMAL)
            self.btn_maze.config(state=tk.NORMAL)
            for rb in self.algo_radios:
                rb.config(state=tk.NORMAL)

    def _clear_visualization_layers(self) -> None:
        self.explored_cells.clear()
        self.path_cells.clear()
        self.last_explored_cell = None

    def _update_stats_display(self, result: Optional[PathResult], status_override: Optional[str] = None) -> None:
        algo = self.selected_algo_var.get()
        self.stat_labels["Algorithm"].config(text=algo)

        if status_override:
            col = Theme.TEXT_PRIMARY
            if status_override == "READY":
                col = Theme.TEXT_SECONDARY
            elif "RUNNING" in status_override or "EXPLORING" in status_override:
                col = Theme.CELL_EXPLORING
            self.stat_labels["Status"].config(text=status_override, fg=col)

        if result is not None:
            self.stat_labels["Nodes Explored"].config(text=str(result.visited_count))
            self.stat_labels["Path Length"].config(text=f"{result.path_length} steps" if result.found else "N/A")
            self.stat_labels["Traversal Cost"].config(text=f"{result.path_cost:.2f}" if result.found else "N/A")
            self.stat_labels["Compute Time"].config(text=f"{result.execution_time_ms:.4f} ms")


# ==============================================================================
# APPLICATION ENTRY POINT
# ==============================================================================

def launch_gui() -> None:
    """Instantiate and run the Tkinter desktop visualizer application."""
    root = tk.Tk()
    app = PathfindingVisualizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
