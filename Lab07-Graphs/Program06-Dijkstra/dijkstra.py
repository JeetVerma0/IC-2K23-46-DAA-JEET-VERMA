#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 7: Graphs
Program 6: Weighted Graph and Dijkstra's Shortest Path Algorithm

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
Dijkstra's Algorithm (Edsger W. Dijkstra, 1959) solves the Single-Source Shortest
Path (SSSP) problem on weighted directed or undirected graphs with NON-NEGATIVE
edge weights.

GREEDY MIN-HEAP RELAXATION:
1. Initialize distances from source s: dist[s] = 0, and dist[v] = infinity for all v != s.
2. Insert (0, s) into a Min-Priority Queue.
3. While the priority queue is not empty:
   - Extract vertex u with minimum tentative distance.
   - If extracted distance > dist[u], ignore (stale entry).
   - For each neighbor v with edge weight w(u, v):
     * Relaxation Step: If dist[u] + w(u, v) < dist[v]:
         dist[v] = dist[u] + w(u, v)
         predecessor[v] = u
         Insert (dist[v], v) into priority queue.

WHY DIJKSTRA REQUIRES NON-NEGATIVE WEIGHTS:
Dijkstra operates greedily on the assumption that once a vertex is settled
(extracted from the min-priority queue), its shortest distance is finalized.
If negative edge weights exist, a longer path with a negative edge could later
reduce the distance, violating the greedy invariant and producing incorrect results.
For graphs with negative weights, the Bellman-Ford algorithm must be used instead.

COMPLEXITIES (WITH BINARY HEAP PQ):
  - Time Complexity : O((V + E) log V)
  - Space Complexity: O(V + E) for graph storage, O(V) for distances and heap.
================================================================================
"""

import sys
from typing import Any, Dict, List, Optional, Set, Tuple


class MinHeapPriorityQueue:
    """Manual binary min-heap priority queue storing (priority, data) tuples."""

    def __init__(self) -> None:
        self._heap: List[Tuple[float, Any]] = []

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def insert(self, priority: float, data: Any) -> None:
        """Insert (priority, data) and sift up in O(log n) time."""
        self._heap.append((priority, data))
        self._sift_up(len(self._heap) - 1)

    def extract_min(self) -> Tuple[float, Any]:
        """Extract and return minimum (priority, data) in O(log n) time."""
        if self.is_empty():
            raise IndexError("Cannot extract_min from an empty priority queue.")
        if len(self._heap) == 1:
            return self._heap.pop()

        min_item = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._sift_down(0)
        return min_item

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self._heap[idx][0] < self._heap[parent][0]:
                self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
                idx = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        n = len(self._heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < n and self._heap[left][0] < self._heap[smallest][0]:
                smallest = left
            if right < n and self._heap[right][0] < self._heap[smallest][0]:
                smallest = right

            if smallest != idx:
                self._heap[idx], self._heap[smallest] = self._heap[smallest], self._heap[idx]
                idx = smallest
            else:
                break


class WeightedGraph:
    """Weighted graph supporting directed and undirected configurations."""

    def __init__(self, is_directed: bool = False) -> None:
        self.is_directed: bool = is_directed
        # Maps u -> List of (v, weight)
        self._adj: Dict[Any, List[Tuple[Any, float]]] = {}

    def add_vertex(self, v: Any) -> None:
        if v not in self._adj:
            self._adj[v] = []

    def add_edge(self, u: Any, v: Any, weight: float) -> None:
        """
        Add a weighted edge. Rejects negative weights because Dijkstra
        requires non-negative weights.
        """
        if weight < 0:
            raise ValueError(
                f"Negative edge weight ({weight}) rejected! Dijkstra requires non-negative edge weights."
            )

        self.add_vertex(u)
        self.add_vertex(v)

        # Update if edge exists, else append
        updated = False
        for i, (target, _) in enumerate(self._adj[u]):
            if target == v:
                self._adj[u][i] = (v, weight)
                updated = True
                break
        if not updated:
            self._adj[u].append((v, weight))

        if not self.is_directed and u != v:
            updated_rev = False
            for i, (target, _) in enumerate(self._adj[v]):
                if target == u:
                    self._adj[v][i] = (u, weight)
                    updated_rev = True
                    break
            if not updated_rev:
                self._adj[v].append((u, weight))

    def get_vertices(self) -> List[Any]:
        return list(self._adj.keys())

    # -------------------------------------------------------------------------
    # Dijkstra's Algorithm
    # -------------------------------------------------------------------------
    def dijkstra(
        self, source: Any
    ) -> Tuple[Dict[Any, float], Dict[Any, Optional[Any]]]:
        """
        Compute shortest path distances and predecessor paths from source.

        Returns:
            distances: Dict mapping vertex -> shortest distance (float('inf') if unreachable).
            predecessors: Dict mapping vertex -> predecessor vertex on shortest path.
        """
        if source not in self._adj:
            raise KeyError(f"Source vertex '{source}' does not exist in graph.")

        distances: Dict[Any, float] = {v: float("inf") for v in self._adj}
        predecessors: Dict[Any, Optional[Any]] = {v: None for v in self._adj}

        distances[source] = 0.0
        pq = MinHeapPriorityQueue()
        pq.insert(0.0, source)

        visited: Set[Any] = set()

        while not pq.is_empty():
            curr_dist, u = pq.extract_min()

            if u in visited:
                continue
            visited.add(u)

            for neighbor, weight in self._adj[u]:
                if neighbor not in visited:
                    new_dist = curr_dist + weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        predecessors[neighbor] = u
                        pq.insert(new_dist, neighbor)

        return distances, predecessors

    def get_shortest_path(self, source: Any, destination: Any) -> Tuple[Optional[List[Any]], float]:
        """
        Reconstruct shortest path and total distance from source to destination.
        Returns: (path_list, total_distance). If unreachable, returns (None, inf).
        """
        distances, predecessors = self.dijkstra(source)
        if destination not in distances or distances[destination] == float("inf"):
            return None, float("inf")

        path = []
        curr: Optional[Any] = destination
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        path.reverse()
        return path, distances[destination]

    def display(self) -> None:
        """Display formatted weighted graph adjacency list."""
        g_type = "Directed" if self.is_directed else "Undirected"
        print(f"\nWeighted Graph ({g_type}, |V| = {len(self._adj)}):")
        for u in sorted(self._adj.keys(), key=str):
            edge_strs = [f"{v}(w={w})" for v, w in self._adj[u]]
            print(f"  {u} -> [ {', '.join(edge_strs)} ]")


def build_sample_graph() -> WeightedGraph:
    """
    Construct classic textbook weighted graph:
        A --- (4) ---> B --- (1) ---> C
        |              |              ^
       (2)            (1)             |
        v              v              |
        D --- (3) ---> E --- (2) -----+
    Plus disconnected vertex Z.
    """
    g = WeightedGraph(is_directed=True)
    g.add_edge("A", "B", 4.0)
    g.add_edge("A", "D", 2.0)
    g.add_edge("B", "C", 1.0)
    g.add_edge("B", "E", 1.0)
    g.add_edge("D", "E", 3.0)
    g.add_edge("E", "C", 2.0)
    g.add_vertex("Z")  # Unreachable component
    return g


def run_tests() -> None:
    """Automated unit verification test suite for Weighted Graph & Dijkstra."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Weighted Graph & Dijkstra")
    print("=" * 70)

    g = build_sample_graph()

    # Test 1: Distances from source "A"
    distances, predecessors = g.dijkstra("A")
    assert distances["A"] == 0.0
    assert distances["B"] == 4.0
    assert distances["D"] == 2.0
    assert distances["E"] == 5.0  # Min(A->D->E: 2+3=5, A->B->E: 4+1=5)
    assert distances["C"] == 5.0  # A -> B -> C: 4 + 1 = 5.0
    assert distances["Z"] == float("inf")  # Unreachable
    print(f"[PASS] Test 1: Shortest distances verified -> {distances}")

    # Test 2: Path reconstruction
    path_c, dist_c = g.get_shortest_path("A", "C")
    assert dist_c == 5.0
    assert path_c == ["A", "B", "C"]
    print(f"[PASS] Test 2: Shortest path A -> C verified -> {path_c} (dist: {dist_c})")

    # Test 3: Unreachable vertex handling
    path_z, dist_z = g.get_shortest_path("A", "Z")
    assert path_z is None
    assert dist_z == float("inf")
    print("[PASS] Test 3: Unreachable vertex 'Z' correctly reported as inf.")

    # Test 4: Negative edge weight rejection
    try:
        g.add_edge("A", "B", -5.0)
        assert False, "Should raise ValueError on negative edge weight"
    except ValueError:
        pass
    print("[PASS] Test 4: Negative edge weight rejection verified.")

    # Test 5: Undirected weighted graph with multiple paths
    undir_g = WeightedGraph(is_directed=False)
    undir_g.add_edge(1, 2, 7)
    undir_g.add_edge(1, 3, 9)
    undir_g.add_edge(1, 6, 14)
    undir_g.add_edge(2, 3, 10)
    undir_g.add_edge(2, 4, 15)
    undir_g.add_edge(3, 4, 11)
    undir_g.add_edge(3, 6, 2)
    undir_g.add_edge(4, 5, 6)
    undir_g.add_edge(6, 5, 9)

    # Shortest path 1 -> 5: 1 -> 3 (9) -> 6 (2) -> 5 (9) = 20
    p15, d15 = undir_g.get_shortest_path(1, 5)
    assert d15 == 20
    assert p15 == [1, 3, 6, 5]
    print(f"[PASS] Test 5: Undirected multi-path Dijkstra verified -> {p15} (dist: {d15})")

    print("\nALL 5 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 55)
    print("        WEIGHTED GRAPH & DIJKSTRA'S MENU")
    print("=" * 55)
    print(" 1. Add Weighted Edge (u, v, weight)")
    print(" 2. Compute Dijkstra from Source (All Distances)")
    print(" 3. Find Shortest Path to Specific Destination")
    print(" 4. Display Weighted Graph")
    print(" 5. Load Default Sample Graph (With Unreachable Node)")
    print(" 6. Run Automated Tests (--test)")
    print(" 7. Exit")
    print("=" * 55)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 7 — Dijkstra's Algorithm Demo")
    print("==========================================================")

    graph = build_sample_graph()
    print("Loaded default sample directed weighted graph.")

    while True:
        print_menu()
        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            u = input("Enter source vertex u: ").strip()
            v = input("Enter target vertex v: ").strip()
            w_str = input("Enter positive edge weight: ").strip()
            try:
                w = float(w_str)
                graph.add_edge(u, v, w)
                print(f"Weighted edge ({u} -> {v}, weight={w}) added.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == "2":
            s = input(f"Enter source vertex {graph.get_vertices()}: ").strip()
            try:
                distances, preds = graph.dijkstra(s)
                print(f"\nShortest Distances from Source '{s}':")
                print("+" + "-" * 15 + "+" + "-" * 15 + "+" + "-" * 15 + "+")
                print(f"| {'Vertex':^13} | {'Distance':^13} | {'Predecessor':^13} |")
                print("+" + "-" * 15 + "+" + "-" * 15 + "+" + "-" * 15 + "+")
                for v in sorted(distances.keys(), key=str):
                    d = distances[v]
                    d_str = "Unreachable" if d == float("inf") else f"{d:.2f}"
                    p_str = str(preds[v]) if preds[v] is not None else "-"
                    print(f"| {str(v):^13} | {d_str:^13} | {p_str:^13} |")
                print("+" + "-" * 15 + "+" + "-" * 15 + "+" + "-" * 15 + "+")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "3":
            s = input("Enter start vertex: ").strip()
            d = input("Enter destination vertex: ").strip()
            try:
                path, total_dist = graph.get_shortest_path(s, d)
                if path:
                    print(f"\nShortest Path: {' -> '.join(map(str, path))}")
                    print(f"Total Distance: {total_dist:.2f}")
                else:
                    print(f"\nDestination '{d}' is UNREACHABLE from '{s}'.")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "4":
            graph.display()

        elif choice == "5":
            graph = build_sample_graph()
            print("Reset to default sample graph.")

        elif choice == "6":
            run_tests()

        elif choice == "7":
            print("Exiting Dijkstra Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 7.")


if __name__ == "__main__":
    main()

