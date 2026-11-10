#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 7: Graphs
Program 1: Graph Representation using Adjacency Matrix

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
A Graph G = (V, E) is a non-linear data structure consisting of a set of vertices
(nodes) V and a set of edges (links) E connecting pairs of vertices.

ADJACENCY MATRIX REPRESENTATION:
An Adjacency Matrix is a 2D square matrix M of dimensions V x V, where:
  - M[u][v] = 1 (or edge weight w) if there is an edge from vertex u to vertex v.
  - M[u][v] = 0 if there is no edge between u and v.

CHARACTERISTICS:
1. Undirected Graph:
   - The matrix is symmetric: M[u][v] == M[v][u].
   - Adding an edge (u, v) sets both M[u][v] = 1 and M[v][u] = 1.
2. Directed Graph (Digraph):
   - The matrix is generally asymmetric.
   - Adding edge (u, v) sets only M[u][v] = 1.
3. Self-Loops:
   - An edge connecting a vertex to itself is represented by M[u][u] = 1.
   - Allowed and handled consistently.

COMPLEXITY:
  - Edge Lookup (u, v)     : O(1) time
  - Add / Remove Edge      : O(1) time
  - Find all neighbors of u: O(V) time
  - Space Complexity       : O(V^2) space (dense representation)
================================================================================
"""

import sys
from typing import List, Optional


class GraphAdjacencyMatrix:
    """Graph implementation backed by a 2D contiguous adjacency matrix."""

    def __init__(self, num_vertices: int, is_directed: bool = False) -> None:
        """
        Initialize an adjacency matrix graph.

        Args:
            num_vertices: Total number of vertices (must be > 0).
            is_directed: Boolean flag; True for directed, False for undirected.
        """
        if not isinstance(num_vertices, int) or num_vertices <= 0:
            raise ValueError("Number of vertices must be a positive integer greater than zero.")

        self.num_vertices: int = num_vertices
        self.is_directed: bool = is_directed
        # Preallocate V x V matrix with zeros
        self.matrix: List[List[int]] = [[0] * num_vertices for _ in range(num_vertices)]

    def _validate_vertex(self, v: int) -> None:
        """Ensure vertex index is within bounds [0, num_vertices - 1]."""
        if not isinstance(v, int) or v < 0 or v >= self.num_vertices:
            raise IndexError(
                f"Vertex index {v} out of bounds! Valid range is [0, {self.num_vertices - 1}]."
            )

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        """
        Add an edge from vertex u to vertex v with optional weight.
        """
        self._validate_vertex(u)
        self._validate_vertex(v)
        if weight <= 0:
            raise ValueError(f"Edge weight must be positive, got {weight}.")

        self.matrix[u][v] = weight
        if not self.is_directed:
            self.matrix[v][u] = weight

    def remove_edge(self, u: int, v: int) -> None:
        """
        Remove the edge between vertex u and vertex v.
        """
        self._validate_vertex(u)
        self._validate_vertex(v)
        self.matrix[u][v] = 0
        if not self.is_directed:
            self.matrix[v][u] = 0

    def has_edge(self, u: int, v: int) -> bool:
        """Return True if an edge exists from u to v, False otherwise."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self.matrix[u][v] != 0

    def get_edge_weight(self, u: int, v: int) -> int:
        """Return weight of edge (u, v) or 0 if no edge exists."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self.matrix[u][v]

    def get_neighbors(self, u: int) -> List[int]:
        """Return list of adjacent neighbor vertices reachable from u."""
        self._validate_vertex(u)
        neighbors = []
        for v in range(self.num_vertices):
            if self.matrix[u][v] != 0:
                neighbors.append(v)
        return neighbors

    def display(self) -> None:
        """Display formatted 2D adjacency matrix with row and column headers."""
        g_type = "Directed" if self.is_directed else "Undirected"
        print(f"\nAdjacency Matrix ({g_type} Graph, |V| = {self.num_vertices}):")

        # Header row
        header = "       " + " ".join(f"{c:4d}" for c in range(self.num_vertices))
        print(header)
        print("     +" + "----" * self.num_vertices)

        for r in range(self.num_vertices):
            row_str = " ".join(f"{self.matrix[r][c]:4d}" for c in range(self.num_vertices))
            print(f" {r:3d} | {row_str}")


def run_tests() -> None:
    """Automated unit verification test suite for Adjacency Matrix."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Graph Adjacency Matrix")
    print("=" * 70)

    # Test 1: Undirected graph construction & symmetry
    g_undir = GraphAdjacencyMatrix(4, is_directed=False)
    g_undir.add_edge(0, 1)
    g_undir.add_edge(1, 2)
    g_undir.add_edge(2, 3)

    assert g_undir.has_edge(0, 1) is True
    assert g_undir.has_edge(1, 0) is True  # Symmetric
    assert g_undir.has_edge(0, 2) is False
    assert g_undir.get_neighbors(1) == [0, 2]
    print("[PASS] Test 1: Undirected graph construction and symmetry verified.")

    # Test 2: Edge removal
    g_undir.remove_edge(1, 2)
    assert g_undir.has_edge(1, 2) is False
    assert g_undir.has_edge(2, 1) is False
    assert g_undir.get_neighbors(1) == [0]
    print("[PASS] Test 2: Edge removal verified.")

    # Test 3: Directed graph asymmetry
    g_dir = GraphAdjacencyMatrix(3, is_directed=True)
    g_dir.add_edge(0, 1)
    assert g_dir.has_edge(0, 1) is True
    assert g_dir.has_edge(1, 0) is False  # Asymmetric
    print("[PASS] Test 3: Directed graph asymmetry verified.")

    # Test 4: Self-loop handling
    g_dir.add_edge(2, 2)
    assert g_dir.has_edge(2, 2) is True
    assert g_dir.get_neighbors(2) == [2]
    print("[PASS] Test 4: Self-loop handling verified.")

    # Test 5: Out of bounds vertex validation
    try:
        g_dir.add_edge(0, 5)
        assert False, "Should raise IndexError on out-of-bounds vertex"
    except IndexError:
        pass
    print("[PASS] Test 5: Vertex boundary validation verified.")

    print("\nALL 5 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 50)
    print("       GRAPH ADJACENCY MATRIX MENU")
    print("=" * 50)
    print(" 1. Add Edge (u, v)")
    print(" 2. Remove Edge (u, v)")
    print(" 3. Check Edge Existence (has_edge)")
    print(" 4. Get Neighbors of Vertex")
    print(" 5. Display Adjacency Matrix")
    print(" 6. Run Automated Tests (--test)")
    print(" 7. Exit")
    print("=" * 50)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 7 — Graph Adjacency Matrix Demo")
    print("==========================================================")

    while True:
        try:
            v_input = input("Enter number of vertices (|V| > 0): ").strip()
            num_v = int(v_input)
            if num_v <= 0:
                print("Error: |V| must be > 0.")
                continue
            dir_input = input("Is graph directed? (y/n) [default: n]: ").strip().lower()
            is_directed = dir_input == "y"
            graph = GraphAdjacencyMatrix(num_v, is_directed=is_directed)
            print(f"Created {'Directed' if is_directed else 'Undirected'} Graph with {num_v} vertices [0 to {num_v-1}].")
            break
        except ValueError:
            print("Invalid input! Please enter a valid integer.")

    while True:
        print_menu()
        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            u_str = input("Enter source vertex u: ").strip()
            v_str = input("Enter target vertex v: ").strip()
            try:
                u, v = int(u_str), int(v_str)
                graph.add_edge(u, v)
                print(f"Edge ({u}, {v}) added successfully.")
            except (ValueError, IndexError) as err:
                print(f"Error: {err}")

        elif choice == "2":
            u_str = input("Enter source vertex u: ").strip()
            v_str = input("Enter target vertex v: ").strip()
            try:
                u, v = int(u_str), int(v_str)
                graph.remove_edge(u, v)
                print(f"Edge ({u}, {v}) removed successfully.")
            except (ValueError, IndexError) as err:
                print(f"Error: {err}")

        elif choice == "3":
            u_str = input("Enter source vertex u: ").strip()
            v_str = input("Enter target vertex v: ").strip()
            try:
                u, v = int(u_str), int(v_str)
                exists = graph.has_edge(u, v)
                print(f"Edge ({u}, {v}) {'EXISTS' if exists else 'DOES NOT EXIST'}.")
            except (ValueError, IndexError) as err:
                print(f"Error: {err}")

        elif choice == "4":
            u_str = input("Enter vertex u: ").strip()
            try:
                u = int(u_str)
                neighbors = graph.get_neighbors(u)
                print(f"Neighbors of {u}: {neighbors}")
            except (ValueError, IndexError) as err:
                print(f"Error: {err}")

        elif choice == "5":
            graph.display()

        elif choice == "6":
            run_tests()

        elif choice == "7":
            print("Exiting Adjacency Matrix Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 7.")


if __name__ == "__main__":
    main()

