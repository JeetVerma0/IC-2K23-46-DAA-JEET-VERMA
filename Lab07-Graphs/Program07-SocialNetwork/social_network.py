#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 7: Graphs
Program 7: Social Network / Friendship Graph Simulator

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
A Social Network is modeled naturally as an undirected, unweighted graph:
  - Vertices: Users / Profiles.
  - Edges: Mutual friendship connections.

KEY GRAPH OPERATIONS IN SOCIAL NETWORKS:
1. Immediate Friends (Degree 1 Neighbors):
   Directly inspect the adjacency list of user u.
2. Friends of Friends (FoF - Degree 2 Connections):
   Explore the 2-hop neighborhood of u. Exclude u itself and all immediate
   (1-hop) friends of u to produce friend recommendations!
3. Degrees of Separation (Shortest Connection Path):
   Using Breadth-First Search (BFS) guarantees discovering the shortest mutual
   friendship chain connecting any two individuals in the network.
4. Social Clusters (Connected Components):
   Identifies isolated or connected social circles/communities using full graph
   traversal.

GRAPH RESTRICTIONS:
Graph relationships are strictly stored in adjacency lists and traversed via
BFS queues without relying on built-in graph or queue libraries.

COMPLEXITIES:
  - Add User / Friendship : O(1)
  - Friends of Friends    : O(deg(u) * max_deg)
  - Degrees of Separation : O(V + E) via BFS
  - Connected Components  : O(V + E)
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
            raise IndexError("Queue is empty.")
        assert self._front is not None
        val = self._front.data
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return val


class UserProfile:
    """Metadata for a social network user."""

    def __init__(self, username: str, full_name: str) -> None:
        self.username: str = username
        self.full_name: str = full_name

    def __repr__(self) -> str:
        return f"{self.full_name} (@{self.username})"


class SocialNetworkGraph:
    """
    Social Network graph backed by an adjacency list representation.
    Friendships are strictly symmetric (undirected).
    """

    def __init__(self) -> None:
        self._users: Dict[str, UserProfile] = {}
        # Adjacency list: username -> List[str] of friend usernames
        self._adj: Dict[str, List[str]] = {}

    def add_user(self, username: str, full_name: str) -> None:
        """Register a new user in the network."""
        username = username.strip().lower()
        if not username:
            raise ValueError("Username cannot be empty.")
        if username in self._users:
            raise ValueError(f"User '@{username}' is already registered.")

        self._users[username] = UserProfile(username, full_name.strip())
        self._adj[username] = []

    def _validate_user(self, username: str) -> None:
        if username not in self._users:
            raise KeyError(f"User '@{username}' not found in the social network.")

    def add_friendship(self, u: str, v: str) -> None:
        """Form a mutual friendship connection between users u and v."""
        u, v = u.strip().lower(), v.strip().lower()
        self._validate_user(u)
        self._validate_user(v)

        if u == v:
            raise ValueError("Cannot form a friendship with oneself.")

        if v not in self._adj[u]:
            self._adj[u].append(v)
        if u not in self._adj[v]:
            self._adj[v].append(u)

    def remove_friendship(self, u: str, v: str) -> None:
        """Remove mutual friendship between u and v."""
        u, v = u.strip().lower(), v.strip().lower()
        self._validate_user(u)
        self._validate_user(v)

        if v in self._adj[u]:
            self._adj[u].remove(v)
        if u in self._adj[v]:
            self._adj[v].remove(u)

    def get_friends(self, username: str) -> List[UserProfile]:
        """Return list of immediate friends (Degree 1)."""
        username = username.strip().lower()
        self._validate_user(username)
        return [self._users[f] for f in sorted(self._adj[username])]

    def get_friends_of_friends(self, username: str) -> List[UserProfile]:
        """
        Find 2-hop connections (Friends of Friends), excluding the user
        and their direct friends. Perfect for friend suggestions!
        """
        username = username.strip().lower()
        self._validate_user(username)

        direct_friends = set(self._adj[username])
        fof_set: Set[str] = set()

        for friend in direct_friends:
            for candidate in self._adj[friend]:
                if candidate != username and candidate not in direct_friends:
                    fof_set.add(candidate)

        return [self._users[u] for u in sorted(fof_set)]

    def shortest_connection_path(self, start_user: str, target_user: str) -> Optional[List[UserProfile]]:
        """
        Find the shortest friendship chain connecting two users via BFS.
        Returns: List of UserProfiles along path, or None if disconnected.
        """
        start = start_user.strip().lower()
        target = target_user.strip().lower()
        self._validate_user(start)
        self._validate_user(target)

        if start == target:
            return [self._users[start]]

        visited: Set[str] = {start}
        parent: Dict[str, str] = {}
        queue = ManualQueue()
        queue.enqueue(start)

        found = False
        while not queue.is_empty():
            curr = queue.dequeue()
            if curr == target:
                found = True
                break

            for nbr in sorted(self._adj[curr]):
                if nbr not in visited:
                    visited.add(nbr)
                    parent[nbr] = curr
                    queue.enqueue(nbr)

        if not found and target not in parent:
            return None

        # Reconstruct path
        path = []
        curr = target
        while curr != start:
            path.append(self._users[curr])
            curr = parent[curr]
        path.append(self._users[start])
        path.reverse()
        return path

    def find_communities(self) -> List[List[UserProfile]]:
        """Find all connected social clusters/communities via full BFS."""
        visited: Set[str] = set()
        communities: List[List[UserProfile]] = []

        all_users = sorted(self._users.keys())
        for user in all_users:
            if user not in visited:
                community: List[UserProfile] = []
                queue = ManualQueue()
                visited.add(user)
                queue.enqueue(user)

                while not queue.is_empty():
                    curr = queue.dequeue()
                    community.append(self._users[curr])

                    for nbr in sorted(self._adj[curr]):
                        if nbr not in visited:
                            visited.add(nbr)
                            queue.enqueue(nbr)

                communities.append(community)

        return communities

    def display(self) -> None:
        """Display network directory and friendship lists."""
        print(f"\nSocial Network Directory (|Users| = {len(self._users)}):")
        for u in sorted(self._users.keys()):
            profile = self._users[u]
            friends = self._adj[u]
            friend_str = ", ".join(f"@{f}" for f in sorted(friends)) if friends else "(No friends)"
            print(f"  - {profile.full_name:<16} (@{u:<10}) -> Friends: [ {friend_str} ]")


def build_sample_network() -> SocialNetworkGraph:
    """
    Construct realistic sample social network:
      Cluster 1: Alice -- Bob -- Charlie -- David
                   |       |
                 Eve ------+
      Cluster 2: Frank -- Grace
    """
    sn = SocialNetworkGraph()
    sn.add_user("alice", "Alice Walker")
    sn.add_user("bob", "Bob Smith")
    sn.add_user("charlie", "Charlie Brown")
    sn.add_user("david", "David Miller")
    sn.add_user("eve", "Eve Adams")
    sn.add_user("frank", "Frank Castle")
    sn.add_user("grace", "Grace Hopper")

    sn.add_friendship("alice", "bob")
    sn.add_friendship("bob", "charlie")
    sn.add_friendship("charlie", "david")
    sn.add_friendship("alice", "eve")
    sn.add_friendship("eve", "bob")
    sn.add_friendship("frank", "grace")  # Separate cluster

    return sn


def run_tests() -> None:
    """Automated unit verification test suite for Social Network Graph."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Social Network Graph")
    print("=" * 70)

    sn = build_sample_network()

    # Test 1: Immediate friends of Alice
    alice_friends = [u.username for u in sn.get_friends("alice")]
    assert alice_friends == ["bob", "eve"]
    print(f"[PASS] Test 1: Immediate friends of Alice verified -> {alice_friends}")

    # Test 2: Friends of Friends (FoF) for Alice
    # Alice's friends: Bob, Eve.
    # Bob's friends: Alice, Charlie, Eve.
    # Eve's friends: Alice, Bob.
    # FoF for Alice should be Charlie (David is 3 hops away)!
    alice_fof = [u.username for u in sn.get_friends_of_friends("alice")]
    assert alice_fof == ["charlie"]
    print(f"[PASS] Test 2: Friends of Friends recommendation verified -> {alice_fof}")

    # Test 3: Shortest connection path (Degrees of Separation)
    # Alice to David: Alice -> Bob -> Charlie -> David (3 degrees)
    path = sn.shortest_connection_path("alice", "david")
    assert path is not None
    path_names = [u.username for u in path]
    assert path_names == ["alice", "bob", "charlie", "david"]
    print(f"[PASS] Test 3: Degrees of separation path verified -> {path_names}")

    # Test 4: Disconnected clusters
    unconnected = sn.shortest_connection_path("alice", "frank")
    assert unconnected is None
    print("[PASS] Test 4: Disconnected users correctly identified (None).")

    # Test 5: Social communities / connected components
    comms = sn.find_communities()
    assert len(comms) == 2
    c1_names = [u.username for u in comms[0]]
    c2_names = [u.username for u in comms[1]]
    assert set(c1_names) == {"alice", "bob", "charlie", "david", "eve"}
    assert set(c2_names) == {"frank", "grace"}
    print(f"[PASS] Test 5: Social communities discovered -> {c1_names} and {c2_names}")

    # Test 6: Friendship removal
    sn.remove_friendship("alice", "bob")
    assert "bob" not in [u.username for u in sn.get_friends("alice")]
    assert "alice" not in [u.username for u in sn.get_friends("bob")]
    print("[PASS] Test 6: Friendship removal verified.")

    print("\nALL 6 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 55)
    print("        SOCIAL NETWORK SIMULATOR MENU")
    print("=" * 55)
    print(" 1. Add User Profile")
    print(" 2. Add Friendship Connection")
    print(" 3. Remove Friendship Connection")
    print(" 4. List Immediate Friends of a User")
    print(" 5. Find Friends of Friends (Suggestions)")
    print(" 6. Find Degrees of Separation (Shortest Path)")
    print(" 7. Find Social Clusters (Connected Components)")
    print(" 8. Display Full Network Directory")
    print(" 9. Run Automated Tests (--test)")
    print(" 10. Exit")
    print("=" * 55)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 7 — Social Network Graph Simulator")
    print("==========================================================")

    sn = build_sample_network()
    print("Loaded sample social network with 7 users across 2 clusters.")

    while True:
        print_menu()
        choice = input("Enter choice (1-10): ").strip()

        if choice == "1":
            uname = input("Enter unique username (e.g. john): ").strip()
            name = input("Enter full name: ").strip()
            try:
                sn.add_user(uname, name)
                print(f"User '@{uname}' created successfully.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == "2":
            u1 = input("Enter first username: ").strip()
            u2 = input("Enter second username: ").strip()
            try:
                sn.add_friendship(u1, u2)
                print(f"Friendship created between @{u1} and @{u2}.")
            except (KeyError, ValueError) as err:
                print(f"Error: {err}")

        elif choice == "3":
            u1 = input("Enter first username: ").strip()
            u2 = input("Enter second username: ").strip()
            try:
                sn.remove_friendship(u1, u2)
                print(f"Friendship severed between @{u1} and @{u2}.")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "4":
            u = input("Enter username: ").strip()
            try:
                friends = sn.get_friends(u)
                print(f"\nFriends of @{u} ({len(friends)}):")
                for f in friends:
                    print(f"  - {f}")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "5":
            u = input("Enter username: ").strip()
            try:
                fof = sn.get_friends_of_friends(u)
                print(f"\nFriends of Friends Recommendations for @{u} ({len(fof)}):")
                if fof:
                    for s in fof:
                        print(f"  * {s}")
                else:
                    print("  (No recommendations found)")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "6":
            u1 = input("Enter starting username: ").strip()
            u2 = input("Enter target username: ").strip()
            try:
                path = sn.shortest_connection_path(u1, u2)
                if path:
                    print(f"\nDegrees of Separation ({len(path)-1} hops):")
                    print("  " + " -> ".join(f"@{p.username}" for p in path))
                else:
                    print(f"\nNo social connection path exists between @{u1} and @{u2}.")
            except KeyError as err:
                print(f"Error: {err}")

        elif choice == "7":
            comms = sn.find_communities()
            print(f"\nDiscovered {len(comms)} Connected Social Communities:")
            for idx, c in enumerate(comms, start=1):
                users_str = ", ".join(f"@{u.username}" for u in c)
                print(f"  Community {idx} ({len(c)} members): [ {users_str} ]")

        elif choice == "8":
            sn.display()

        elif choice == "9":
            run_tests()

        elif choice == "10":
            print("Exiting Social Network Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 10.")


if __name__ == "__main__":
    main()

