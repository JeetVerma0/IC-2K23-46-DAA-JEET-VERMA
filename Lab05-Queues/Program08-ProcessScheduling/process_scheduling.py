#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 5: Queues
Program 8: Operating System Process Scheduling Simulation (Round Robin)

Author: Student Implementation
Course: IC-307D — DSA Lab (CO1)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
In time-shared operating systems, the CPU scheduler allocates processing time
among competing processes. Round Robin (RR) is the foundational preemptive
scheduling algorithm designed specifically for time-sharing systems.

HOW THE READY QUEUE IS USED:
  1. The CPU Ready Queue is maintained strictly as a First-In, First-Out (FIFO) queue.
  2. The scheduler assigns the CPU to the process at the front of the ready queue
     for a predetermined duration called the Time Quantum (or time slice).
  3. Two outcomes can occur during a quantum:
     - The process completes execution within the quantum: it leaves the system,
       and its completion time is recorded.
     - The process needs more CPU time: an interrupt fires, the process is preempted,
       and it is appended to the REAR of the Ready Queue.
  4. Any processes newly arriving while the current process was executing are
     enqueued into the Ready Queue BEFORE the preempted process is re-enqueued.

KEY METRICS CALCULATED:
  - Completion Time (CT): Wall-clock time at which the process finishes execution.
  - Turnaround Time (TAT): Total elapsed time from arrival to completion.
      TAT = CT - AT
  - Waiting Time (WT): Total time spent sitting idle in the ready queue.
      WT = TAT - BT
  - Average Turnaround Time: Sum(TAT) / Number of Processes
  - Average Waiting Time:    Sum(WT)  / Number of Processes

COMPLEXITY:
  - Ready Queue Enqueue / Dequeue: O(1) time
  - Simulation Loop: O(total_burst / quantum + n) steps
  - Auxiliary Space: O(n) for process tracking and ready queue
================================================================================
"""

import sys
from typing import Any, List, Optional, Tuple


class Process:
    """Represents an operating system process with scheduling parameters."""

    def __init__(self, pid: str, arrival_time: int, burst_time: int) -> None:
        self.pid: str = pid
        self.arrival_time: int = arrival_time
        self.burst_time: int = burst_time
        self.remaining_time: int = burst_time

        # Metrics calculated post-execution
        self.completion_time: int = 0
        self.turnaround_time: int = 0
        self.waiting_time: int = 0
        self.first_response_time: Optional[int] = None

    def __repr__(self) -> str:
        return f"Process({self.pid}, AT={self.arrival_time}, BT={self.burst_time}, Rem={self.remaining_time})"


class QueueNode:
    """Singly-linked queue node."""

    def __init__(self, process: Process) -> None:
        self.process: Process = process
        self.next: Optional["QueueNode"] = None


class FIFOReadyQueue:
    """Custom dynamic singly-linked FIFO Ready Queue for Process Scheduling."""

    def __init__(self) -> None:
        self._front: Optional[QueueNode] = None
        self._rear: Optional[QueueNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        return self._front is None

    def size(self) -> int:
        return self._size

    def enqueue(self, process: Process) -> None:
        """Add process to rear of ready queue."""
        new_node = QueueNode(process)
        if self.is_empty():
            self._front = new_node
            self._rear = new_node
        else:
            assert self._rear is not None
            self._rear.next = new_node
            self._rear = new_node
        self._size += 1

    def dequeue(self) -> Process:
        """Remove and return process from front of ready queue."""
        if self.is_empty():
            raise IndexError("Ready Queue Underflow: Queue is empty.")
        assert self._front is not None
        proc = self._front.process
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return proc

    def to_pids(self) -> List[str]:
        """Return list of process IDs in the ready queue."""
        pids = []
        curr = self._front
        while curr:
            pids.append(curr.process.pid)
            curr = curr.next
        return pids


class RoundRobinScheduler:
    """
    Simulates Round Robin CPU scheduling over an arbitrary list of processes.
    """

    def __init__(self, time_quantum: int) -> None:
        if not isinstance(time_quantum, int) or time_quantum <= 0:
            raise ValueError("Time Quantum must be a positive integer.")
        self.time_quantum: int = time_quantum
        self.processes: List[Process] = []
        self.timeline: List[Tuple[int, int, str]] = []  # (start_time, end_time, pid)

    def add_process(self, pid: str, arrival_time: int, burst_time: int) -> None:
        """Add a process specification."""
        if arrival_time < 0:
            raise ValueError(f"Arrival time cannot be negative: {arrival_time}")
        if burst_time <= 0:
            raise ValueError(f"Burst time must be > 0: {burst_time}")
        self.processes.append(Process(pid, arrival_time, burst_time))

    def run_simulation(self) -> Tuple[List[Process], float, float]:
        """
        Execute the Round Robin simulation.

        Returns:
            (finished_processes, avg_turnaround_time, avg_waiting_time)
        """
        if not self.processes:
            return [], 0.0, 0.0

        # Sort input processes by arrival time, tie-broken by PID
        sorted_procs = sorted(self.processes, key=lambda p: (p.arrival_time, p.pid))
        ready_queue = FIFOReadyQueue()
        self.timeline.clear()

        n = len(sorted_procs)
        arrival_idx = 0
        completed_count = 0
        current_time = 0
        finished_list: List[Process] = []

        # If the earliest arrival is > 0, advance time to first arrival
        if sorted_procs[0].arrival_time > current_time:
            self.timeline.append((current_time, sorted_procs[0].arrival_time, "[IDLE]"))
            current_time = sorted_procs[0].arrival_time

        # Initial arrival enqueue
        while arrival_idx < n and sorted_procs[arrival_idx].arrival_time <= current_time:
            ready_queue.enqueue(sorted_procs[arrival_idx])
            arrival_idx += 1

        while completed_count < n:
            if ready_queue.is_empty():
                # CPU is idle waiting for next arrival
                if arrival_idx < n:
                    next_arrival = sorted_procs[arrival_idx].arrival_time
                    self.timeline.append((current_time, next_arrival, "[IDLE]"))
                    current_time = next_arrival
                    while arrival_idx < n and sorted_procs[arrival_idx].arrival_time <= current_time:
                        ready_queue.enqueue(sorted_procs[arrival_idx])
                        arrival_idx += 1
                continue

            # Dispatch process at front of ready queue
            current_proc = ready_queue.dequeue()

            if current_proc.first_response_time is None:
                current_proc.first_response_time = current_time

            # Calculate slice to run
            exec_time = min(self.time_quantum, current_proc.remaining_time)
            start_t = current_time
            end_t = current_time + exec_time
            self.timeline.append((start_t, end_t, current_proc.pid))
            current_time = end_t
            current_proc.remaining_time -= exec_time

            # Enqueue any new processes arriving during this execution slice
            while arrival_idx < n and sorted_procs[arrival_idx].arrival_time <= current_time:
                ready_queue.enqueue(sorted_procs[arrival_idx])
                arrival_idx += 1

            # Check if current process has finished or needs to re-enter ready queue
            if current_proc.remaining_time == 0:
                current_proc.completion_time = current_time
                current_proc.turnaround_time = current_proc.completion_time - current_proc.arrival_time
                current_proc.waiting_time = current_proc.turnaround_time - current_proc.burst_time
                finished_list.append(current_proc)
                completed_count += 1
            else:
                # Re-enqueue preempted process to rear of queue
                ready_queue.enqueue(current_proc)

        # Calculate averages
        total_tat = sum(p.turnaround_time for p in finished_list)
        total_wt = sum(p.waiting_time for p in finished_list)
        avg_tat = total_tat / n
        avg_wt = total_wt / n

        return finished_list, avg_tat, avg_wt

    def display_results(self, finished_list: List[Process], avg_tat: float, avg_wt: float) -> None:
        """Display formatted Gantt timeline and scheduling metrics table."""
        print("\n" + "=" * 75)
        print(f"      ROUND ROBIN SCHEDULING RESULTS (Time Quantum = {self.time_quantum})")
        print("=" * 75)

        # 1. Timeline / Gantt Chart
        print("\nExecution Timeline (Gantt Chart Blocks):")
        timeline_str = " | ".join(f"[{s:2d}-{e:2d}: {pid}]" for s, e, pid in self.timeline)
        print(f"  {timeline_str}")

        # 2. Detailed Process Metrics Table
        print("\nProcess Performance Metrics:")
        print("+" + "-" * 8 + "+" + "-" * 14 + "+" + "-" * 12 + "+" + "-" * 17 + "+" + "-" * 17 + "+" + "-" * 14 + "+")
        print(f"| {'PID':^6} | {'Arrival (AT)':^12} | {'Burst (BT)':^10} | {'Completion (CT)':^15} | {'Turnaround(TAT)':^15} | {'Waiting (WT)':^12} |")
        print("+" + "-" * 8 + "+" + "-" * 14 + "+" + "-" * 12 + "+" + "-" * 17 + "+" + "-" * 17 + "+" + "-" * 14 + "+")

        for p in sorted(finished_list, key=lambda x: x.pid):
            print(f"| {p.pid:^6} | {p.arrival_time:^12} | {p.burst_time:^10} | {p.completion_time:^15} | {p.turnaround_time:^15} | {p.waiting_time:^12} |")
        print("+" + "-" * 8 + "+" + "-" * 14 + "+" + "-" * 12 + "+" + "-" * 17 + "+" + "-" * 17 + "+" + "-" * 14 + "+")

        print(f"\nSummary Averages:")
        print(f"  Total Processes:         {len(finished_list)}")
        print(f"  Average Turnaround Time: {avg_tat:.2f} time units")
        print(f"  Average Waiting Time:    {avg_wt:.2f} time units")
        print("=" * 75)


def run_tests() -> None:
    """Automated unit verification test suite for Round Robin Process Scheduling."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Round Robin Process Scheduler")
    print("=" * 70)

    # Standard textbook test case:
    # P1: AT=0, BT=5
    # P2: AT=1, BT=3
    # P3: AT=2, BT=1
    # P4: AT=3, BT=2
    # Quantum = 2
    scheduler = RoundRobinScheduler(time_quantum=2)
    scheduler.add_process("P1", 0, 5)
    scheduler.add_process("P2", 1, 3)
    scheduler.add_process("P3", 2, 1)
    scheduler.add_process("P4", 3, 2)

    finished, avg_tat, avg_wt = scheduler.run_simulation()
    p_map = {p.pid: p for p in finished}

    # Trace:
    # t=0: P1 arrives. P1 runs (0-2), remaining=3. At t=2, P2(AT=1) and P3(AT=2) arrived.
    # Queue: [P2, P3, P1]
    # t=2: P2 runs (2-4), remaining=1. At t=3, P4 arrived.
    # Queue: [P3, P1, P4, P2]
    # t=4: P3 runs (4-5), remaining=0. P3 completes at t=5. CT(P3)=5.
    # Queue: [P1, P4, P2]
    # t=5: P1 runs (5-7), remaining=1.
    # Queue: [P4, P2, P1]
    # t=7: P4 runs (7-9), remaining=0. P4 completes at t=9. CT(P4)=9.
    # Queue: [P2, P1]
    # t=9: P2 runs (9-10), remaining=0. P2 completes at t=10. CT(P2)=10.
    # Queue: [P1]
    # t=10: P1 runs (10-11), remaining=0. P1 completes at t=11. CT(P1)=11.

    assert p_map["P3"].completion_time == 5
    assert p_map["P4"].completion_time == 9
    assert p_map["P2"].completion_time == 10
    assert p_map["P1"].completion_time == 11

    # TAT = CT - AT
    assert p_map["P1"].turnaround_time == 11 - 0  # 11
    assert p_map["P2"].turnaround_time == 10 - 1  # 9
    assert p_map["P3"].turnaround_time == 5 - 2   # 3
    assert p_map["P4"].turnaround_time == 9 - 3   # 6

    # WT = TAT - BT
    assert p_map["P1"].waiting_time == 11 - 5  # 6
    assert p_map["P2"].waiting_time == 9 - 3   # 6
    assert p_map["P3"].waiting_time == 3 - 1   # 2
    assert p_map["P4"].waiting_time == 6 - 2   # 4

    assert avg_tat == (11 + 9 + 3 + 6) / 4     # 7.25
    assert avg_wt == (6 + 6 + 2 + 4) / 4       # 4.5
    print("[PASS] Test 1: Textbook multi-process Round Robin scheduling verified.")

    # Test 2: Idle period handling
    s2 = RoundRobinScheduler(time_quantum=3)
    s2.add_process("PA", 2, 3)
    s2.add_process("PB", 8, 2)
    fin2, avg_tat2, avg_wt2 = s2.run_simulation()
    p2_map = {p.pid: p for p in fin2}
    # PA starts at 2, finishes at 5. CT=5, TAT=3, WT=0.
    # Idle from 0 to 2, and 5 to 8.
    # PB starts at 8, finishes at 10. CT=10, TAT=2, WT=0.
    assert p2_map["PA"].completion_time == 5
    assert p2_map["PB"].completion_time == 10
    assert avg_wt2 == 0.0
    print("[PASS] Test 2: CPU idle period and delayed arrival verified.")

    # Test 3: Quantum larger than burst times
    s3 = RoundRobinScheduler(time_quantum=10)
    s3.add_process("P1", 0, 4)
    s3.add_process("P2", 0, 2)
    fin3, avg_tat3, avg_wt3 = s3.run_simulation()
    p3_map = {p.pid: p for p in fin3}
    assert p3_map["P1"].completion_time == 4
    assert p3_map["P2"].completion_time == 6
    print("[PASS] Test 3: Large quantum (degenerates to FCFS) verified.")

    print("\nALL 3 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 5 — OS Process Scheduling (Round Robin)")
    print("==========================================================")

    while True:
        try:
            q_str = input("Enter Time Quantum (positive integer): ").strip()
            quantum = int(q_str)
            if quantum <= 0:
                print("Error: Time Quantum must be greater than zero.")
                continue
            scheduler = RoundRobinScheduler(time_quantum=quantum)
            break
        except ValueError:
            print("Invalid input! Please enter a positive integer.")

    print("\nAdd processes to scheduler. Enter 'run' when finished.")
    count = 1
    while True:
        prompt = input(f"\nEnter Process {count} PID (or 'run' to execute, 'demo' for sample set): ").strip()
        if prompt.lower() == "run":
            if not scheduler.processes:
                print("No processes added yet. Please add at least one process.")
                continue
            break
        elif prompt.lower() == "demo":
            scheduler = RoundRobinScheduler(time_quantum=quantum)
            scheduler.add_process("P1", 0, 5)
            scheduler.add_process("P2", 1, 3)
            scheduler.add_process("P3", 2, 1)
            scheduler.add_process("P4", 3, 2)
            print("Loaded standard 4-process demonstration workload.")
            break

        pid = prompt if prompt else f"P{count}"
        try:
            at_str = input(f"  Arrival Time for {pid} (integer >= 0): ").strip()
            bt_str = input(f"  Burst Time for {pid} (integer > 0): ").strip()
            at = int(at_str)
            bt = int(bt_str)
            scheduler.add_process(pid, at, bt)
            print(f"Added Process {pid}: Arrival={at}, Burst={bt}")
            count += 1
        except ValueError as err:
            print(f"Input Error: {err}. Process not added.")

    finished, avg_tat, avg_wt = scheduler.run_simulation()
    scheduler.display_results(finished, avg_tat, avg_wt)


if __name__ == "__main__":
    main()

