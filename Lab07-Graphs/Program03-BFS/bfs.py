#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 7: Graphs
Program 3: Breadth-First Search (BFS) Traversal and Shortest Path

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
Breadth-First Search (BFS) is a fundamental graph traversal algorithm that explores
vertices in order of increasing distance from a given source vertex.

LEVEL-BY-LEVEL EXPLORATION:
  - First, visit the source vertex s (Distance = 0).
  - Next, visit all immediate neighbors of s (Distance = 1).
  - Then, visit all unvisited neighbors of those neighbors (Distance = 2), and so on.

THE ROLE OF THE FIFO QUEUE:
A First-In, First-Out (FIFO) queue guarantees that vertices discovered earlier
are processed earlier. This ensures that the first time a vertex v is dequeued,
the path discovered from s to v is guaranteed to have the MINIMUM NUMBER OF EDGES
(shortest unweighted path).

HANDLING DISCONNECTED GRAPHS:
If a graph contains multiple disconnected components, starting BFS at a single
vertex only visits the component reachable from that vertex. To traverse the entire
graph, an outer loop iterates through all vertices, launching BFS on any vertex
that remains unvisited.

COMPLEXITIES:
  - Time Complexity: O(V + E) where V is vertices and E is edges.
    Each vertex is enqueued and dequeued at most once; every edge is inspected once
    (in directed graphs) or twice (in undirected graphs).
  - Space Complexity: O(V) for the visited set, predecessor map, and FIFO queue.
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
    """Custom manual dynamic FIFO queue (no queue.Queue or collections.deque)."""

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


class BFSGraph:
    """Graph structure with BFS traversal and unweighted shortest-path finder."""

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
    # BFS Traversal from a Single Source
    # -------------------------------------------------------------------------
    def bfs_traversal(self, start: Any) -> List[Any]:
        """
        Perform BFS traversal starting from vertex `start`.
        Returns: List of visited vertices in discovery order.
        """
        if start not in self._adj:
            raise KeyError(f"Start vertex '{start}' not found in graph.")

        visited: Set[Any] = set()
        traversal_order: List[Any] = []
        queue = ManualQueue()

        visited.add(start)
        queue.enqueue(start)

        while not queue.is_empty():
            curr = queue.dequeue()
            traversal_order.append(curr)

            # Sort neighbors for deterministic traversal ordering
            neighbors = sorted(self._adj.get(curr, []), key=str)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue(neighbor)

        return traversal_order

    # -------------------------------------------------------------------------
    # Full BFS (Handling Disconnected Components)
    # -------------------------------------------------------------------------
    def full_bfs_traversal(self) -> List[List[Any]]:
        """
        Traverse the entire graph, handling multiple disconnected components.
        Returns: List of components, each being a list of vertices in BFS order.
        """
        visited: Set[Any] = set()
        components: List[List[Any]] = []

        all_vertices = sorted(self._adj.keys(), key=str)
        for v in all_vertices:
            if v not in visited:
                comp_order: List[Any] = []
                queue = ManualQueue()

                visited.add(v)
                queue.enqueue(v)

                while not queue.is_empty():
                    curr = queue.dequeue()
                    comp_order.append(curr)

                    neighbors = sorted(self._adj.get(curr, []), key=str)
                    for nbr in neighbors:
                        if nbr not in visited:
                            visited.add(nbr)
                            queue.enqueue(nbr)

                components.append(comp_order)

        return components

    # -------------------------------------------------------------------------
    # Shortest Unweighted Path via BFS
    # -------------------------------------------------------------------------
    def shortest_path(self, start: Any, destination: Any) -> Optional[List[Any]]:
        """
        Find shortest unweighted path from start to destination using BFS.
        Returns list of vertices along the path, or None if destination is unreachable.
        """
        if start not in self._adj:
            raise KeyError(f"Start vertex '{start}' does not exist.")
        if destination not in self._adj:
            raise KeyError(f"Destination vertex '{destination}' does not exist.")

        if start == destination:
            return [start]

        visited: Set[Any] = {start}
        parent: Dict[Any, Any] = {}
        queue = ManualQueue()
        queue.enqueue(start)

        found = False
        while not queue.is_empty():
            curr = queue.dequeue()
            if curr == destination:
                found = True
                break

            neighbors = sorted(self._adj.get(curr, []), key=str)
            for nbr in neighbors:
                if nbr not in visited:
                    visited.add(nbr)
                    parent[nbr] = curr
                    queue.enqueue(nbr)

        if not found and destination not in parent:
            return None

        # Reconstruct path by following parent pointers backward
        path = []
        curr = destination
        while curr != start:
            path.append(curr)
            curr = parent[curr]
        path.append(start)
        path.reverse()
        return path


def build_sample_graph() -> BFSGraph:
    """
    Construct a sample graph with 2 components:
      Component 1:
        0 --- 1 --- 3
        |     |
        2 ----+
      Component 2 (Disconnected):
        4 --- 5
    """
    g = BFSGraph(is_directed=False)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(4, 5)  # Disconnected component
    return g


def run_tests() -> None:
    """Automated unit verification test suite for BFS."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Breadth-First Search (BFS)")
    print("=" * 70)

    g = build_sample_graph()

    # Test 1: Single-source BFS
    order = g.bfs_traversal(0)
    # Distance 0: [0], Distance 1: [1, 2], Distance 2: [3]
    assert order == [0, 1, 2, 3]
    print(f"[PASS] Test 1: Single-source BFS traversal verified -> {order}")

    # Test 2: Full BFS across disconnected components
    comps = g.full_bfs_traversal()
    assert len(comps) == 2
    assert comps[0] == [0, 1, 2, 3]
    assert comps[1] == [4, 5]
    print(f"[PASS] Test 2: Disconnected components discovered -> {comps}")

    # Test 3: Shortest unweighted path (reachable)
    path = g.shortest_path(0, 3)
    assert path == [0, 1, 3]
    print(f"[PASS] Test 3: Shortest path 0 -> 3 verified -> {path}")

    # Test 4: Unreachable path detection
    unreachable = g.shortest_path(0, 4)
    assert unreachable is None
    print("[PASS] Test 4: Unreachable destination correctly returned None.")

    # Test 5: Self-path
    self_path = g.shortest_path(2, 2)
    assert self_path == [2]
    print("[PASS] Test 5: Same source and destination handled -> [2].")

    print("\nALL 5 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 50)
    print("        BREADTH-FIRST SEARCH (BFS) MENU")
    print("=" * 50)
    print(" 1. Add Edge (u, v)")
    print(" 2. Perform Single-Source BFS Traversal")
    print(" 3. Perform Full Graph BFS (All Components)")
    print(" 4. Find Shortest Unweighted Path (Source -> Dest)")
    print(" 5. Load Default Sample Graph (Disconnected)")
    print(" 6. Run Automated Tests (--test)")
    print(" 7. Exit")
    print("=" * 50)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 7 — Breadth-First Search (BFS) Demo")
    print("==========================================================")

    graph = build_sample_graph()
    print("Loaded default sample graph with disconnected components.")

    while True:
        print_menu()
        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            u = input("Enter vertex u: ").strip()
            v = input("Enter vertex v: ").strip()
            if u and v:
                graph.add_edge(u, v)
                print(f"Edge ({u}, {v}) added.")

        elif choice == "2":
            s = input(f"Enter start vertex {graph.get_vertices()}: ").strip()
            try:
                # Try integer parsing first if keys are ints
                val = int(s) if s.isdigit() else s
                order = graph.bfs_traversal(val)
                print(f"\nBFS Traversal Order starting at {val}:")
                print(f"  {' -> '.join(map(str, order))}")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "3":
            comps = graph.full_bfs_traversal()
            print(f"\nFull Graph Traversal ({len(comps)} Connected Components):")
            for idx, comp in enumerate(comps, start=1):
                print(f"  Component {idx}: {' -> '.join(map(str, comp))}")

        elif choice == "4":
            s = input("Enter start vertex: ").strip()
            d = input("Enter destination vertex: ").strip()
            val_s = int(s) if s.isdigit() else s
            val_d = int(d) if d.isdigit() else d
            try:
                path = graph.shortest_path(val_s, val_d)
                if path:
                    print(f"\nShortest Path ({len(path)-1} edges): {' -> '.join(map(str, path))}")
                else:
                    print(f"\nNo path exists between '{val_s}' and '{val_d}' (Disconnected!).")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "5":
            graph = build_sample_graph()
            print("Reset to default sample graph.")

        elif choice == "6":
            run_tests()

        elif choice == "7":
            print("Exiting BFS Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 7.")


if __name__ == "__main__":
    main()

