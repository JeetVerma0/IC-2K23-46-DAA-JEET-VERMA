#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 7: Graphs
Program 4: Recursive Depth-First Search (DFS) Traversal

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
Depth-First Search (DFS) is a recursive graph traversal strategy that plunges as
deeply as possible along each branch before backtracking.

HOW RECURSION USES THE IMPLICIT CALL STACK:
  1. Starting at vertex u, mark u as visited.
  2. For each unvisited neighbor v of u:
     - Invoke dfs_recursive(v).
     - The runtime pushes the activation frame of u onto the hidden Call Stack
       and transfers control to v.
  3. When a vertex has no unvisited neighbors, the function call returns (pops from
     the call stack), backtracking to the previous vertex to explore its remaining
     unvisited branches.

DISCONNECTED GRAPHS:
To ensure all vertices in a disconnected graph are visited, an outer wrapper loops
through every vertex in V; whenever an unvisited vertex is encountered, a new DFS
recursion is initiated.

APPLICATIONS:
  - Cycle detection in directed and undirected graphs.
  - Topological sorting.
  - Finding connected components and strongly connected components (Tarjan/Kosaraju).
  - Pathfinding and maze solving.

COMPLEXITIES:
  - Time Complexity : O(V + E)
  - Space Complexity: O(V) for the visited set and recursive call stack depth.
================================================================================
"""

import sys
from typing import Any, Dict, List, Optional, Set


class RecursiveDFSGraph:
    """Graph structure supporting recursive Depth-First Search."""

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
    # Single-Source Recursive DFS
    # -------------------------------------------------------------------------
    def dfs_traversal(self, start: Any) -> List[Any]:
        """
        Perform recursive DFS from a starting vertex.
        Returns: List of vertices visited in DFS discovery order.
        """
        if start not in self._adj:
            raise KeyError(f"Start vertex '{start}' not found in graph.")

        visited: Set[Any] = set()
        traversal_order: List[Any] = []
        self._dfs_helper(start, visited, traversal_order)
        return traversal_order

    def _dfs_helper(self, u: Any, visited: Set[Any], traversal_order: List[Any]) -> None:
        """Recursive helper executing on the implicit call stack."""
        visited.add(u)
        traversal_order.append(u)

        # Sort neighbors for deterministic, reproducible traversal order
        neighbors = sorted(self._adj.get(u, []), key=str)
        for v in neighbors:
            if v not in visited:
                self._dfs_helper(v, visited, traversal_order)

    # -------------------------------------------------------------------------
    # Full Recursive DFS (All Components)
    # -------------------------------------------------------------------------
    def full_dfs_traversal(self) -> List[List[Any]]:
        """
        Perform recursive DFS traversing all connected components.
        Returns: List of components, each containing vertices in DFS order.
        """
        visited: Set[Any] = set()
        components: List[List[Any]] = []

        all_vertices = sorted(self._adj.keys(), key=str)
        for v in all_vertices:
            if v not in visited:
                comp_order: List[Any] = []
                self._dfs_helper(v, visited, comp_order)
                components.append(comp_order)

        return components


def build_sample_graph() -> RecursiveDFSGraph:
    """
    Construct reference graph with two components:
      Component 1:
         0 --- 1 --- 3
         |     |
         2 ----+
      Component 2 (Disconnected):
         4 --- 5
    """
    g = RecursiveDFSGraph(is_directed=False)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(4, 5)
    return g


def run_tests() -> None:
    """Automated unit verification test suite for Recursive DFS."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Recursive Depth-First Search (DFS)")
    print("=" * 70)

    g = build_sample_graph()

    # Test 1: Single-source DFS
    # From 0 -> neighbor 1 (visits 1, then 1's neighbor 2, then 2's neighbor 0 is visited,
    # then 1's neighbor 3). Order: [0, 1, 2, 3]
    order = g.dfs_traversal(0)
    assert order == [0, 1, 2, 3]
    print(f"[PASS] Test 1: Single-source recursive DFS verified -> {order}")

    # Test 2: Start at vertex 3
    order_3 = g.dfs_traversal(3)
    # 3 -> 1 -> 0 -> 2
    assert order_3 == [3, 1, 0, 2]
    print(f"[PASS] Test 2: Recursive DFS from leaf vertex 3 verified -> {order_3}")

    # Test 3: Full graph traversal across disconnected components
    comps = g.full_dfs_traversal()
    assert len(comps) == 2
    assert comps[0] == [0, 1, 2, 3]
    assert comps[1] == [4, 5]
    print(f"[PASS] Test 3: Disconnected components discovered -> {comps}")

    # Test 4: Single vertex graph
    g_single = RecursiveDFSGraph()
    g_single.add_vertex("X")
    assert g_single.dfs_traversal("X") == ["X"]
    print("[PASS] Test 4: Single isolated vertex traversal verified.")

    # Test 5: Missing vertex handling
    try:
        g.dfs_traversal(999)
        assert False, "Should raise KeyError on non-existent start vertex"
    except KeyError:
        pass
    print("[PASS] Test 5: Missing vertex exception handling verified.")

    print("\nALL 5 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 50)
    print("     RECURSIVE DEPTH-FIRST SEARCH (DFS) MENU")
    print("=" * 50)
    print(" 1. Add Edge (u, v)")
    print(" 2. Perform Single-Source Recursive DFS")
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
    print("  IC-307D: Unit 7 — Recursive DFS Traversal Demo")
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
                order = graph.dfs_traversal(val)
                print(f"\nRecursive DFS Traversal Order starting at {val}:")
                print(f"  {' -> '.join(map(str, order))}")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "3":
            comps = graph.full_dfs_traversal()
            print(f"\nFull DFS Traversal ({len(comps)} Connected Components):")
            for idx, comp in enumerate(comps, start=1):
                print(f"  Component {idx}: {' -> '.join(map(str, comp))}")

        elif choice == "4":
            graph = build_sample_graph()
            print("Reset to default sample graph.")

        elif choice == "5":
            run_tests()

        elif choice == "6":
            print("Exiting Recursive DFS Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 6.")


if __name__ == "__main__":
    main()

