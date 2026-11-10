#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 7: Graphs
Program 5: Iterative Depth-First Search (DFS) Traversal using Explicit Stack

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
While recursive DFS relies on the language runtime's hidden call stack,
Iterative DFS manages an explicit LIFO Stack data structure in heap memory.

HOW EXPLICIT STACKS REPLACE RECURSIVE ACTIVATION FRAMES:
  1. Initialize an empty stack and push the start vertex: stack = [start].
  2. While the stack is not empty:
     - Pop the top vertex u from the stack.
     - If u has not yet been visited:
       * Mark u as visited and append to traversal result.
       * For each neighbor v of u:
         If v is unvisited, push v onto the stack.
  3. Ordering Nuance:
     Because a stack is Last-In, First-Out (LIFO), pushing neighbors in reverse
     order (e.g., reversed sorted order) ensures the first neighbor in alphabetical/
     numerical order is popped and explored first, closely matching the
     canonical recursive DFS traversal!

BENEFITS OF ITERATIVE DFS:
  - Immune to call stack overflow (bypasses Python's default recursion limit of 1000).
  - Fine-grained control over execution state, checkpointing, and resource allocation.

COMPLEXITIES:
  - Time Complexity : O(V + E)
  - Space Complexity: O(V) for visited set and explicit stack.
================================================================================
"""

import sys
from typing import Any, Dict, List, Optional, Set


class IterativeDFSGraph:
    """Graph structure supporting non-recursive, stack-based Depth-First Search."""

    def __init__(self, is_directed: bool = False) -> None:
        self.is_directed: bool = is_directed
        self._adj: Dict[Any, List[Any]] = {}

    def add_vertex(self, v: Any) -> None:
        if v not in self._adj:
            self._adj[v] = []

    def add_edge(self, u: Any, v: Any) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        if v not in self._adj[u]:
            self._adj[u].append(v)
        if not self.is_directed and u != v:
            if u not in self._adj[v]:
                self._adj[v].append(u)

    def get_vertices(self) -> List[Any]:
        return list(self._adj.keys())

    # -------------------------------------------------------------------------
    # Single-Source Iterative DFS
    # -------------------------------------------------------------------------
    def dfs_iterative(self, start: Any) -> List[Any]:
        """
        Perform iterative DFS using an explicit LIFO stack (NO recursion).
        Returns: List of visited vertices in discovery order.
        """
        if start not in self._adj:
            raise KeyError(f"Start vertex '{start}' not found in graph.")

        visited: Set[Any] = set()
        traversal_order: List[Any] = []
        stack: List[Any] = [start]

        while len(stack) > 0:
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr)
                traversal_order.append(curr)

                # Push neighbors in reverse sorted order so smallest is popped first
                neighbors = sorted(self._adj.get(curr, []), key=str, reverse=True)
                for nbr in neighbors:
                    if nbr not in visited:
                        stack.append(nbr)

        return traversal_order

    # -------------------------------------------------------------------------
    # Full Iterative DFS (All Connected Components)
    # -------------------------------------------------------------------------
    def full_dfs_iterative(self) -> List[List[Any]]:
        """
        Perform iterative DFS across all disconnected components.
        Returns: List of components with vertices in DFS order.
        """
        visited: Set[Any] = set()
        components: List[List[Any]] = []

        all_vertices = sorted(self._adj.keys(), key=str)
        for v in all_vertices:
            if v not in visited:
                comp_order: List[Any] = []
                stack: List[Any] = [v]

                while len(stack) > 0:
                    curr = stack.pop()
                    if curr not in visited:
                        visited.add(curr)
                        comp_order.append(curr)

                        neighbors = sorted(self._adj.get(curr, []), key=str, reverse=True)
                        for nbr in neighbors:
                            if nbr not in visited:
                                stack.append(nbr)

                components.append(comp_order)

        return components


def build_sample_graph() -> IterativeDFSGraph:
    """
    Construct reference graph with two components:
      Component 1:
         0 --- 1 --- 3
         |     |
         2 ----+
      Component 2 (Disconnected):
         4 --- 5
    """
    g = IterativeDFSGraph(is_directed=False)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(4, 5)
    return g


def run_tests() -> None:
    """Automated unit verification test suite for Iterative DFS."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Iterative Depth-First Search (DFS)")
    print("=" * 70)

    g = build_sample_graph()

    # Test 1: Single-source iterative DFS from 0
    # From 0, neighbors 2 and 1 pushed; 1 popped first -> visits 1; 3 and 2 pushed;
    # 2 popped next -> visits 2; then 3 popped -> visits 3.
    order = g.dfs_iterative(0)
    assert order == [0, 1, 2, 3], f"Unexpected order: {order}"
    print(f"[PASS] Test 1: Iterative DFS verified -> {order}")

    # Test 2: Iterative DFS from vertex 3
    order_3 = g.dfs_iterative(3)
    # 3 -> 1 -> 0 -> 2
    assert order_3 == [3, 1, 0, 2], f"Unexpected order: {order_3}"
    print(f"[PASS] Test 2: Iterative DFS from vertex 3 verified -> {order_3}")

    # Test 3: Disconnected components handled
    comps = g.full_dfs_iterative()
    assert len(comps) == 2
    assert comps[0] == [0, 1, 2, 3]
    assert comps[1] == [4, 5]
    print(f"[PASS] Test 3: Full iterative DFS across disconnected components verified -> {comps}")

    # Test 4: Missing vertex exception handling
    try:
        g.dfs_iterative("NonExistent")
        assert False, "Should raise KeyError on non-existent vertex"
    except KeyError:
        pass
    print("[PASS] Test 4: Missing vertex exception handling verified.")

    print("\nALL 4 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 50)
    print("     ITERATIVE DEPTH-FIRST SEARCH (DFS) MENU")
    print("=" * 50)
    print(" 1. Add Edge (u, v)")
    print(" 2. Perform Single-Source Iterative DFS")
    print(" 3. Perform Full Graph DFS (All Components)")
    print(" 4. Load Default Sample Graph (Disconnected)")
    print(" 5. Run Automated Tests (--test)")
    print(" 6. Exit")
    print("=" * 50)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 7 — Iterative DFS Traversal Demo")
    print("==========================================================")

    graph = build_sample_graph()
    print("Loaded default sample graph with disconnected components.")

    while True:
        print_menu()
        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            u = input("Enter vertex u: ").strip()
            v = input("Enter vertex v: ").strip()
            if u and v:
                graph.add_edge(u, v)
                print(f"Edge ({u}, {v}) added.")

        elif choice == "2":
            s = input(f"Enter start vertex {graph.get_vertices()}: ").strip()
            val = int(s) if s.isdigit() else s
            try:
                order = graph.dfs_iterative(val)
                print(f"\nIterative DFS Traversal Order starting at {val}:")
                print(f"  {' -> '.join(map(str, order))}")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "3":
            comps = graph.full_dfs_iterative()
            print(f"\nFull Iterative DFS ({len(comps)} Connected Components):")
            for idx, comp in enumerate(comps, start=1):
                print(f"  Component {idx}: {' -> '.join(map(str, comp))}")

        elif choice == "4":
            graph = build_sample_graph()
            print("Reset to default sample graph.")

        elif choice == "5":
            run_tests()

        elif choice == "6":
            print("Exiting Iterative DFS Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 6.")


if __name__ == "__main__":
    main()

