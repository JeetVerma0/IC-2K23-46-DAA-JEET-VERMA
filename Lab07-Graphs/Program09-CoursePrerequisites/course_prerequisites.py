#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 7: Graphs
Program 9: Course Prerequisite Tracker and Topological Sorter (Kahn's Algorithm)

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
A university course curriculum with prerequisites can be modeled as a Directed
Graph G = (V, E):
  - Vertices (V): Courses (e.g., CS101, CS201, CS301).
  - Directed Edges (E): A directed edge u -> v signifies that course u is a
    mandatory prerequisite that MUST be completed before enrolling in course v.

DIRECTED ACYCLIC GRAPHS (DAGs) & TOPOLOGICAL SORTING:
A Topological Sort of a directed graph is a linear ordering of its vertices
such that for every directed edge u -> v, vertex u appears before vertex v
in the ordering.
  - Fundamental Theorem: A directed graph possesses a topological ordering
    IF AND ONLY IF it is a Directed Acyclic Graph (DAG) — i.e., it contains NO CYCLES!
  - Circular Prerequisite Deadlock: If course A requires B, B requires C, and C
    requires A (a cycle A -> B -> C -> A), no student can ever graduate because
    none of the three courses can be taken first. Topological sorting detects this!

KAHN'S ALGORITHM (IN-DEGREE BFS METHOD):
  1. Calculate the in-degree (number of incoming prerequisite edges) for every vertex.
  2. Enqueue all vertices with in_degree == 0 into a manual FIFO queue (courses with
     zero prerequisites that can be taken immediately in Semester 1).
  3. While queue is not empty:
     - Dequeue course u and append to the topological ordering.
     - For each course v dependent on u (edge u -> v):
       * Decrement in_degree[v] by 1.
       * If in_degree[v] becomes 0, enqueue v.
  4. Cycle Detection:
     If the count of scheduled courses in the topological ordering is LESS than
     the total number of courses (|V|), A PREREQUISITE CYCLE EXISTS!
     The courses with in_degree > 0 are identified as participating in the cycle deadlock.

COMPLEXITIES:
  - Time Complexity : O(V + E)
  - Space Complexity: O(V + E) for graph storage, O(V) for in-degree and queue.
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


class CoursePrerequisiteTracker:
    """Directed graph representing courses and prerequisite dependencies."""

    def __init__(self) -> None:
        # Maps course_code -> List of dependent course_codes (u -> v means u is prereq for v)
        self._adj: Dict[str, List[str]] = {}
        # Maps course_code -> Course Title
        self._titles: Dict[str, str] = {}

    def add_course(self, code: str, title: str = "") -> None:
        """Register a course in the tracker."""
        code = code.strip().upper()
        if not code:
            raise ValueError("Course code cannot be empty.")
        if code not in self._adj:
            self._adj[code] = []
            self._titles[code] = title.strip() if title else code

    def add_prerequisite(self, prereq_code: str, course_code: str) -> None:
        """
        Add a prerequisite relationship: prereq_code MUST be taken before course_code.
        Directed edge: prereq_code -> course_code.
        """
        prereq = prereq_code.strip().upper()
        course = course_code.strip().upper()
        if prereq == course:
            raise ValueError(f"Self-prerequisite cycle! Course '{course}' cannot require itself.")

        self.add_course(prereq)
        self.add_course(course)

        if course not in self._adj[prereq]:
            self._adj[prereq].append(course)

    def get_courses(self) -> List[str]:
        return list(self._adj.keys())

    # -------------------------------------------------------------------------
    # Kahn's Algorithm for Topological Sort & Cycle Detection
    # -------------------------------------------------------------------------
    def find_schedule(self) -> Tuple[bool, List[str], List[str]]:
        """
        Execute Kahn's algorithm to compute a valid course ordering.

        Returns:
            (is_valid_dag, schedule, cyclic_courses)
            - is_valid_dag: True if valid linear schedule exists, False if cycle detected.
            - schedule: List of course codes in valid prerequisite order.
            - cyclic_courses: List of courses trapped in deadlocks if cycle detected.
        """
        if not self._adj:
            return True, [], []

        # Step 1: Calculate in-degrees for all registered courses
        in_degree: Dict[str, int] = {c: 0 for c in self._adj}
        for u in self._adj:
            for v in self._adj[u]:
                in_degree[v] += 1

        # Step 2: Enqueue all courses with in_degree == 0 (no prerequisites)
        queue = ManualQueue()
        # Sort courses with zero in-degree alphabetically for deterministic schedule
        zero_in = sorted([c for c, deg in in_degree.items() if deg == 0])
        for c in zero_in:
            queue.enqueue(c)

        schedule: List[str] = []

        # Step 3: Process courses
        while not queue.is_empty():
            u = queue.dequeue()
            schedule.append(u)

            # For each course that depends on u, decrement its in-degree
            for v in sorted(self._adj[u]):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.enqueue(v)

        # Step 4: Verify if all courses were successfully scheduled
        total_courses = len(self._adj)
        if len(schedule) == total_courses:
            return True, schedule, []
        else:
            # Cycle detected! Courses remaining with in_degree > 0 are locked in cycle
            locked_courses = sorted([c for c, deg in in_degree.items() if deg > 0])
            return False, schedule, locked_courses

    def display(self) -> None:
        """Display the directed prerequisite graph."""
        print(f"\nCourse Prerequisite Graph (|Courses| = {len(self._adj)}):")
        for u in sorted(self._adj.keys()):
            title = self._titles.get(u, u)
            dependents = self._adj[u]
            if dependents:
                dep_str = ", ".join(dependents)
                print(f"  {u:<8} ({title}) -> Enables: [ {dep_str} ]")
            else:
                print(f"  {u:<8} ({title}) -> (Terminal course, no further dependents)")


def build_sample_curriculum() -> CoursePrerequisiteTracker:
    """
    Standard Computer Science curriculum (Valid DAG):
      CS101 (Intro to CS) ----> CS102 (Data Structures) ----> CS201 (Algorithms) ----> CS301 (AI)
      MATH101 (Calculus) -----> MATH201 (Discrete Math) -+
                                 |
                                 +----------------------------> CS202 (Computer Architecture)
    """
    cpt = CoursePrerequisiteTracker()
    cpt.add_prerequisite("CS101", "CS102")
    cpt.add_prerequisite("CS102", "CS201")
    cpt.add_prerequisite("CS201", "CS301")
    cpt.add_prerequisite("MATH101", "MATH201")
    cpt.add_prerequisite("MATH201", "CS201")
    cpt.add_prerequisite("MATH201", "CS202")
    return cpt


def build_cyclic_curriculum() -> CoursePrerequisiteTracker:
    """Curriculum with circular prerequisite deadlock: A -> B -> C -> A."""
    cpt = CoursePrerequisiteTracker()
    cpt.add_prerequisite("CS101", "CS102")
    cpt.add_prerequisite("CS102", "CS103")
    cpt.add_prerequisite("CS103", "CS101")  # Circular deadlock!
    cpt.add_prerequisite("HIST101", "HIST102")  # Independent valid component
    return cpt


def run_tests() -> None:
    """Automated unit verification test suite for Course Prerequisite Tracker."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Course Prerequisite Tracker")
    print("=" * 70)

    # Test 1: Valid DAG scheduling
    valid_cpt = build_sample_curriculum()
    is_valid, schedule, cyclic = valid_cpt.find_schedule()
    assert is_valid is True
    assert len(cyclic) == 0
    assert len(schedule) == 7

    # Validate that prerequisites appear before dependents
    idx_map = {c: i for i, c in enumerate(schedule)}
    assert idx_map["CS101"] < idx_map["CS102"]
    assert idx_map["CS102"] < idx_map["CS201"]
    assert idx_map["MATH101"] < idx_map["MATH201"]
    assert idx_map["MATH201"] < idx_map["CS201"]
    assert idx_map["CS201"] < idx_map["CS301"]
    print(f"[PASS] Test 1: Valid topological schedule verified -> {schedule}")

    # Test 2: Cycle detection and deadlock reporting
    cyclic_cpt = build_cyclic_curriculum()
    c_valid, c_schedule, c_locked = cyclic_cpt.find_schedule()
    assert c_valid is False
    assert set(c_locked) == {"CS101", "CS102", "CS103"}
    # Valid independent components (HIST101, HIST102) can still be scheduled
    assert "HIST101" in c_schedule and "HIST102" in c_schedule
    print(f"[PASS] Test 2: Prerequisite cycle detected cleanly -> Locked courses: {c_locked}")

    # Test 3: Self-loop prerequisite rejection
    try:
        valid_cpt.add_prerequisite("CS101", "CS101")
        assert False, "Should raise ValueError on self-prerequisite"
    except ValueError:
        pass
    print("[PASS] Test 3: Self-prerequisite rejection verified.")

    print("\nALL 3 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 55)
    print("      COURSE PREREQUISITE TRACKER MENU")
    print("=" * 55)
    print(" 1. Add Course")
    print(" 2. Add Prerequisite Relationship (Prereq -> Course)")
    print(" 3. Compute Valid Study Schedule (Topological Sort)")
    print(" 4. Display Prerequisite Dependency Graph")
    print(" 5. Load Standard Computer Science Curriculum (Valid DAG)")
    print(" 6. Load Circular Deadlock Example (Cycle Detection)")
    print(" 7. Run Automated Tests (--test)")
    print(" 8. Exit")
    print("=" * 55)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 7 — Course Prerequisite Tracker (DAG)")
    print("==========================================================")

    tracker = build_sample_curriculum()
    print("Loaded default sample Computer Science curriculum.")

    while True:
        print_menu()
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            code = input("Enter course code (e.g. CS101): ").strip()
            title = input("Enter course title (e.g. Intro to CS): ").strip()
            try:
                tracker.add_course(code, title)
                print(f"Course '{code}' added.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == "2":
            p = input("Enter prerequisite course code: ").strip()
            c = input("Enter target course code: ").strip()
            try:
                tracker.add_prerequisite(p, c)
                print(f"Prerequisite set: '{p}' must be taken before '{c}'.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == "3":
            is_valid, schedule, locked = tracker.find_schedule()
            if is_valid:
                print("\nValid Study Plan (Topological Ordering):")
                for sem, course in enumerate(schedule, start=1):
                    title = tracker._titles.get(course, course)
                    print(f"  Step {sem:2d}: {course:<8} ({title})")
                print("Status: 100% Valid DAG — All prerequisites satisfied!")
            else:
                print("\nDEADLOCK DETECTED! No valid course schedule exists.")
                print(f"Circular prerequisite cycle prevents completion of {len(locked)} courses:")
                for c in locked:
                    title = tracker._titles.get(c, c)
                    print(f"  * {c:<8} ({title})")

        elif choice == "4":
            tracker.display()

        elif choice == "5":
            tracker = build_sample_curriculum()
            print("Loaded standard Computer Science curriculum.")

        elif choice == "6":
            tracker = build_cyclic_curriculum()
            print("Loaded cyclic curriculum demonstration.")

        elif choice == "7":
            run_tests()

        elif choice == "8":
            print("Exiting Course Prerequisite Tracker. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 8.")


if __name__ == "__main__":
    main()

