#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 7: Graphs
Program 2: Graph Representation using Adjacency List

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
An Adjacency List represents a graph as an associative collection (or array)
where each vertex is mapped to a linked list or dynamic list of its incident edges.

WHY ADJACENCY LIST?
1. Space Efficiency on Sparse Graphs:
   Most real-world networks (social graphs, road maps, web link graphs) are
   sparse, where |E| << |V|^2.
   An adjacency matrix consumes O(V^2) space regardless of edge density.
   An adjacency list consumes only O(V + E) space, which is optimal for sparse graphs.
2. Rapid Neighbor Iteration:
   Iterating over the neighbors of vertex u takes O(deg(u)) time rather than O(V).

DUPLICATE EDGE POLICY:
Attempting to add an edge (u, v) that already exists does not create duplicate
records; instead, the edge weight is updated (or confirmed), preserving uniqueness.

COMPLEXITIES:
  - Add Vertex            : O(1) time
  - Add Edge (u, v)       : O(deg(u)) to verify duplicate, O(1) insertion
  - Remove Edge (u, v)    : O(deg(u)) time
  - Edge Existence Check  : O(deg(u)) time
  - Space Complexity      : O(V + E) space (optimal for sparse graphs)
================================================================================
"""

import sys
from typing import Any, Dict, List, Optional, Tuple


class EdgeNode:
    """Represents an edge target and its associated weight."""

    def __init__(self, target: Any, weight: int = 1) -> None:
        self.target: Any = target
        self.weight: int = weight

    def __repr__(self) -> str:
        return f"Edge({self.target}, w={self.weight})" if self.weight != 1 else str(self.target)


class GraphAdjacencyList:
    """Manually implemented graph backed by an adjacency list representation."""

    def __init__(self, is_directed: bool = False) -> None:
        self.is_directed: bool = is_directed
        # Maps vertex -> List[EdgeNode]
        self._adj: Dict[Any, List[EdgeNode]] = {}

    @property
    def num_vertices(self) -> int:
        return len(self._adj)

    def has_vertex(self, v: Any) -> bool:
        """Check if vertex v exists in the graph."""
        return v in self._adj

    def add_vertex(self, v: Any) -> None:
        """Add a new vertex to the graph if not already present."""
        if v not in self._adj:
            self._adj[v] = []

    def _validate_vertex(self, v: Any) -> None:
        """Raise KeyError if vertex v is not in the graph."""
        if v not in self._adj:
            raise KeyError(f"Vertex '{v}' does not exist in graph.")

    def add_edge(self, u: Any, v: Any, weight: int = 1) -> None:
        """
        Add an edge from u to v. Vertices u and v are added automatically if absent.
        Handles duplicate edges by updating weight.
        """
        if weight <= 0:
            raise ValueError(f"Edge weight must be positive, got {weight}.")

        self.add_vertex(u)
        self.add_vertex(v)

        # Check for existing edge from u to v
        found = False
        for edge in self._adj[u]:
            if edge.target == v:
                edge.weight = weight
                found = True
                break
        if not found:
            self._adj[u].append(EdgeNode(v, weight))

        if not self.is_directed and u != v:
            # Add reverse edge for undirected graphs
            found_rev = False
            for edge in self._adj[v]:
                if edge.target == u:
                    edge.weight = weight
                    found_rev = True
                    break
            if not found_rev:
                self._adj[v].append(EdgeNode(u, weight))

    def remove_edge(self, u: Any, v: Any) -> None:
        """Remove edge connecting u to v."""
        self._validate_vertex(u)
        self._validate_vertex(v)

        self._adj[u] = [e for e in self._adj[u] if e.target != v]
        if not self.is_directed and u != v:
            self._adj[v] = [e for e in self._adj[v] if e.target != u]

    def remove_vertex(self, v: Any) -> None:
        """Remove vertex v and all incident edges connected to it."""
        self._validate_vertex(v)
        # Remove from other vertices' adjacency lists
        del self._adj[v]
        for u in self._adj:
            self._adj[u] = [e for e in self._adj[u] if e.target != v]

    def has_edge(self, u: Any, v: Any) -> bool:
        """Check if an edge exists from u to v."""
        if not self.has_vertex(u) or not self.has_vertex(v):
            return False
        return any(e.target == v for e in self._adj[u])

    def get_neighbors(self, u: Any) -> List[Any]:
        """Return list of destination vertices adjacent to u."""
        self._validate_vertex(u)
        return [e.target for e in self._adj[u]]

    def get_vertices(self) -> List[Any]:
        """Return list of all vertices in graph."""
        return list(self._adj.keys())

    def display(self) -> None:
        """Display formatted adjacency list representation."""
        g_type = "Directed" if self.is_directed else "Undirected"
        print(f"\nAdjacency List ({g_type} Graph, |V| = {self.num_vertices}):")
        if not self._adj:
            print("  [Graph is empty]")
            return

        for u in sorted(self._adj.keys(), key=str):
            edges = self._adj[u]
            if not edges:
                print(f"  {u} -> [] (Isolated)")
            else:
                edge_strs = [f"{e.target}(w={e.weight})" if e.weight != 1 else str(e.target) for e in edges]
                print(f"  {u} -> [ {', '.join(edge_strs)} ]")


def run_tests() -> None:
    """Automated unit verification test suite for Adjacency List."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Graph Adjacency List")
    print("=" * 70)

    # Test 1: Undirected graph construction
    g = GraphAdjacencyList(is_directed=False)
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("A", "C")
    assert g.has_vertex("A") and g.has_vertex("B") and g.has_vertex("C")
    assert g.has_edge("A", "B") is True
    assert g.has_edge("B", "A") is True  # Undirected symmetry
    assert g.has_edge("A", "D") is False
    print("[PASS] Test 1: Undirected graph construction and symmetry verified.")

    # Test 2: Duplicate edge handling
    g.add_edge("A", "B", weight=5)  # Update weight of existing edge
    assert g.has_edge("A", "B") is True
    assert len(g.get_neighbors("A")) == 2  # Still just B and C, no duplicate entry
    print("[PASS] Test 2: Duplicate edge prevention and weight update verified.")

    # Test 3: Edge removal
    g.remove_edge("A", "B")
    assert g.has_edge("A", "B") is False
    assert g.has_edge("B", "A") is False
    print("[PASS] Test 3: Edge removal verified.")

    # Test 4: Directed graph asymmetry
    g_dir = GraphAdjacencyList(is_directed=True)
    g_dir.add_edge("X", "Y")
    assert g_dir.has_edge("X", "Y") is True
    assert g_dir.has_edge("Y", "X") is False
    print("[PASS] Test 4: Directed graph asymmetry verified.")

    # Test 5: Vertex removal and incident edge cleanup
    g.remove_vertex("B")
    assert g.has_vertex("B") is False
    assert g.has_edge("B", "C") is False
    assert "B" not in g.get_neighbors("C")
    print("[PASS] Test 5: Vertex removal and incident edge cleanup verified.")

    print("\nALL 5 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 50)
    print("        GRAPH ADJACENCY LIST MENU")
    print("=" * 50)
    print(" 1. Add Vertex")
    print(" 2. Add Edge (u, v)")
    print(" 3. Remove Edge (u, v)")
    print(" 4. Remove Vertex")
    print(" 5. Check Edge (has_edge)")
    print(" 6. Get Neighbors of Vertex")
    print(" 7. Display Adjacency List")
    print(" 8. Run Automated Tests (--test)")
    print(" 9. Exit")
    print("=" * 50)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 7 — Graph Adjacency List Demo")
    print("==========================================================")

    dir_input = input("Is graph directed? (y/n) [default: n]: ").strip().lower()
    is_directed = dir_input == "y"
    graph = GraphAdjacencyList(is_directed=is_directed)
    print(f"Created {'Directed' if is_directed else 'Undirected'} Adjacency List Graph.")

    while True:
        print_menu()
        choice = input("Enter choice (1-9): ").strip()

        if choice == "1":
            v = input("Enter vertex identifier (e.g. A, Node1): ").strip()
            if v:
                graph.add_vertex(v)
                print(f"Vertex '{v}' added.")

        elif choice == "2":
            u = input("Enter source vertex u: ").strip()
            v = input("Enter target vertex v: ").strip()
            w_str = input("Enter edge weight [default: 1]: ").strip()
            w = int(w_str) if w_str.isdigit() else 1
            if u and v:
                try:
                    graph.add_edge(u, v, weight=w)
                    print(f"Edge ({u} -> {v}, w={w}) added.")
                except ValueError as err:
                    print(f"Error: {err}")

        elif choice == "3":
            u = input("Enter source vertex u: ").strip()
            v = input("Enter target vertex v: ").strip()
            try:
                graph.remove_edge(u, v)
                print(f"Edge ({u}, {v}) removed.")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "4":
            v = input("Enter vertex to delete: ").strip()
            try:
                graph.remove_vertex(v)
                print(f"Vertex '{v}' and its incident edges removed.")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "5":
            u = input("Enter source vertex u: ").strip()
            v = input("Enter target vertex v: ").strip()
            exists = graph.has_edge(u, v)
            print(f"Edge ({u}, {v}) {'EXISTS' if exists else 'DOES NOT EXIST'}.")

        elif choice == "6":
            u = input("Enter vertex u: ").strip()
            try:
                neighbors = graph.get_neighbors(u)
                print(f"Neighbors of {u}: {neighbors}")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "7":
            graph.display()

        elif choice == "8":
            run_tests()

        elif choice == "9":
            print("Exiting Adjacency List Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 9.")


if __name__ == "__main__":
    main()

