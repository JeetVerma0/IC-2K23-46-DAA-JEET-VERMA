#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 5: Queues
Program 7: Customer Service Queue Simulation

Author: Student Implementation
Course: IC-307D — DSA Lab (CO1)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
Queue data structures are the backbone of real-world service facilities such as
banks, hospitals, airport check-in counters, and customer service call centers.
These systems must manage customer arrival order, prevent unfair waiting, and
support differentiated service tiers (e.g., VIP vs Regular).

SIMULATION ARCHITECTURE:
In this simulation, a custom dynamic FIFO queue structure is implemented from
scratch without using Python's `queue.Queue` or `collections.deque`:
  - Customer Entity:
      * ticket_id: Unique formatted identifier (e.g., VIP-101, REG-102)
      * name: Customer's full name
      * service_type: Type of request (e.g., Account Opening, Cash Deposit, Inquiry)
      * is_vip: Boolean indicating priority tier
      * arrival_time: Timestamp or discrete simulation step of arrival
  - Service Desks & Dual Tiering:
      * VIP Queue: High-priority queue served first
      * Regular Queue: Standard FIFO queue
      * Service Logic: If VIP queue has waiting customers, they receive immediate
        precedence over the regular queue, ensuring SLA compliance for premium users.
      * History Log: Tracks served customers, wait durations, and summary statistics.

COMPLEXITY:
  - Enqueue customer : O(1) time
  - Serve (Dequeue)  : O(1) time
  - Peek next        : O(1) time
  - Auxiliary Space  : O(n) where n is total waiting customers
================================================================================
"""

import sys
import time
from typing import Any, List, Optional, Tuple


class Customer:
    """Represents a customer with ticketing and service metadata."""

    def __init__(
        self,
        ticket_id: str,
        name: str,
        service_type: str,
        is_vip: bool = False,
        arrival_step: int = 0,
    ) -> None:
        self.ticket_id: str = ticket_id
        self.name: str = name
        self.service_type: str = service_type
        self.is_vip: bool = is_vip
        self.arrival_step: int = arrival_step

    def __str__(self) -> str:
        tier = "VIP" if self.is_vip else "REGULAR"
        return f"[{self.ticket_id}] {self.name} ({tier} - {self.service_type})"


class Node:
    """Linked list node holding a Customer object."""

    def __init__(self, customer: Customer) -> None:
        self.customer: Customer = customer
        self.next: Optional["Node"] = None


class CustomerQueue:
    """Custom dynamic singly-linked FIFO queue for customer management."""

    def __init__(self, queue_name: str) -> None:
        self.queue_name: str = queue_name
        self._front: Optional[Node] = None
        self._rear: Optional[Node] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """Check if queue has no customers."""
        return self._front is None

    def size(self) -> int:
        """Return number of waiting customers."""
        return self._size

    def enqueue(self, customer: Customer) -> None:
        """Add customer to the rear of the queue in O(1) time."""
        new_node = Node(customer)
        if self.is_empty():
            self._front = new_node
            self._rear = new_node
        else:
            assert self._rear is not None
            self._rear.next = new_node
            self._rear = new_node
        self._size += 1

    def dequeue(self) -> Customer:
        """Remove and return customer from the front of the queue in O(1) time."""
        if self.is_empty():
            raise IndexError(f"Queue '{self.queue_name}' is empty.")
        assert self._front is not None
        customer = self._front.customer
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return customer

    def peek(self) -> Customer:
        """View next customer at the front without dequeuing."""
        if self.is_empty():
            raise IndexError(f"Queue '{self.queue_name}' is empty.")
        assert self._front is not None
        return self._front.customer

    def to_list(self) -> List[Customer]:
        """Convert queue elements to a list ordered front to rear."""
        items: List[Customer] = []
        curr = self._front
        while curr:
            items.append(curr.customer)
            curr = curr.next
        return items


class CustomerServiceSimulator:
    """
    Simulation coordinator managing VIP and Regular service queues,
    desk processing, and operational statistics.
    """

    def __init__(self) -> None:
        self.vip_queue = CustomerQueue("VIP Queue")
        self.regular_queue = CustomerQueue("Regular Queue")
        self.current_simulation_step: int = 1
        self.vip_counter: int = 100
        self.reg_counter: int = 200
        self.served_history: List[Tuple[Customer, int, int]] = []  # (customer, service_step, wait_steps)

    def register_customer(self, name: str, service_type: str, is_vip: bool = False) -> Customer:
        """
        Create and enqueue a new customer ticket.
        """
        if is_vip:
            self.vip_counter += 1
            ticket_id = f"VIP-{self.vip_counter}"
            customer = Customer(ticket_id, name, service_type, is_vip=True, arrival_step=self.current_simulation_step)
            self.vip_queue.enqueue(customer)
        else:
            self.reg_counter += 1
            ticket_id = f"REG-{self.reg_counter}"
            customer = Customer(ticket_id, name, service_type, is_vip=False, arrival_step=self.current_simulation_step)
            self.regular_queue.enqueue(customer)

        self.current_simulation_step += 1
        return customer

    def peek_next_customer(self) -> Optional[Customer]:
        """
        Check which customer is next in line across both priority tiers.
        VIP queue has strict precedence.
        """
        if not self.vip_queue.is_empty():
            return self.vip_queue.peek()
        if not self.regular_queue.is_empty():
            return self.regular_queue.peek()
        return None

    def serve_customer(self) -> Optional[Customer]:
        """
        Serve the next eligible customer.
        VIP queue customers are served before Regular queue customers.
        """
        customer: Optional[Customer] = None
        if not self.vip_queue.is_empty():
            customer = self.vip_queue.dequeue()
        elif not self.regular_queue.is_empty():
            customer = self.regular_queue.dequeue()
        else:
            return None

        wait_time = self.current_simulation_step - customer.arrival_step
        self.served_history.append((customer, self.current_simulation_step, wait_time))
        self.current_simulation_step += 1
        return customer

    def total_waiting(self) -> int:
        """Return total waiting customers across all tiers."""
        return self.vip_queue.size() + self.regular_queue.size()

    def display_status(self) -> None:
        """Display a comprehensive overview of the service center."""
        print("\n" + "=" * 65)
        print("          CUSTOMER SERVICE CENTER DASHBOARD")
        print(f"  Current Time Step: {self.current_simulation_step} | Total Waiting: {self.total_waiting()}")
        print("=" * 65)

        next_cust = self.peek_next_customer()
        if next_cust:
            print(f"  --> NOW CALLING / NEXT IN LINE: {next_cust}")
        else:
            print("  --> NOW CALLING: No customers waiting.")

        print("\n  [VIP WAITING QUEUE] (Count: " + str(self.vip_queue.size()) + ")")
        vip_list = self.vip_queue.to_list()
        if vip_list:
            for idx, c in enumerate(vip_list, start=1):
                print(f"    {idx}. [{c.ticket_id}] {c.name} | Service: {c.service_type} (Wait: {self.current_simulation_step - c.arrival_step} steps)")
        else:
            print("    (No VIP customers waiting)")

        print("\n  [REGULAR WAITING QUEUE] (Count: " + str(self.regular_queue.size()) + ")")
        reg_list = self.regular_queue.to_list()
        if reg_list:
            for idx, c in enumerate(reg_list, start=1):
                print(f"    {idx}. [{c.ticket_id}] {c.name} | Service: {c.service_type} (Wait: {self.current_simulation_step - c.arrival_step} steps)")
        else:
            print("    (No regular customers waiting)")

        print("\n  [SERVED METRICS]")
        print(f"    Total Customers Served: {len(self.served_history)}")
        if self.served_history:
            total_wait = sum(w for _, _, w in self.served_history)
            avg_wait = total_wait / len(self.served_history)
            print(f"    Average Waiting Time:   {avg_wait:.2f} time steps")
            print("    Recent Served (Last 3):")
            for c, s_step, w in self.served_history[-3:]:
                print(f"      - {c.ticket_id} ({c.name}) served at step {s_step} (waited {w} steps)")
        print("=" * 65)


def run_tests() -> None:
    """Automated unit verification test suite for Customer Service Simulator."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Customer Service Queue Simulation")
    print("=" * 70)

    sim = CustomerServiceSimulator()
    assert sim.total_waiting() == 0
    assert sim.peek_next_customer() is None
    print("[PASS] Test 1: Initial state verified.")

    # Test 2: Regular customer enqueuing
    c1 = sim.register_customer("Alice Johnson", "Account Opening", is_vip=False)
    c2 = sim.register_customer("Bob Smith", "Cheque Deposit", is_vip=False)
    assert sim.regular_queue.size() == 2
    assert sim.vip_queue.size() == 0
    assert sim.peek_next_customer().ticket_id == c1.ticket_id
    print("[PASS] Test 2: Regular customer arrival and FIFO order verified.")

    # Test 3: VIP priority over regular customers
    c_vip = sim.register_customer("Charles Xavier", "Loan Consultation", is_vip=True)
    assert sim.vip_queue.size() == 1
    # Despite arriving after Alice and Bob, VIP is called first
    assert sim.peek_next_customer().ticket_id == c_vip.ticket_id
    print("[PASS] Test 3: VIP priority precedence verified.")

    # Test 4: Service execution order
    served_1 = sim.serve_customer()
    assert served_1.ticket_id == c_vip.ticket_id  # VIP served first
    served_2 = sim.serve_customer()
    assert served_2.ticket_id == c1.ticket_id     # Alice served next
    served_3 = sim.serve_customer()
    assert served_3.ticket_id == c2.ticket_id     # Bob served next
    assert sim.total_waiting() == 0
    assert sim.serve_customer() is None           # Underflow handled safely
    print("[PASS] Test 4: Strict service priority order and empty queue handling verified.")

    # Test 5: Metrics and served history
    assert len(sim.served_history) == 3
    print("[PASS] Test 5: Historical reporting and metrics verified.")

    print("\nALL 5 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu options."""
    print("\n" + "=" * 50)
    print("      CUSTOMER SERVICE DESK SIMULATOR")
    print("=" * 50)
    print(" 1. Issue Ticket: Regular Customer")
    print(" 2. Issue Ticket: VIP Customer")
    print(" 3. Serve Next Customer")
    print(" 4. View Next Customer in Line (Peek)")
    print(" 5. Display Live Service Dashboard")
    print(" 6. Exit")
    print("=" * 50)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 5 — Customer Service Queue Simulation")
    print("==========================================================")

    sim = CustomerServiceSimulator()

    while True:
        print_menu()
        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            name = input("Enter customer name: ").strip()
            service = input("Enter service needed (e.g. Deposit, Inquiry): ").strip()
            if not name:
                name = "Customer"
            if not service:
                service = "General Service"
            cust = sim.register_customer(name, service, is_vip=False)
            print(f"Ticket Issued: {cust.ticket_id} for {cust.name} (Regular Queue)")

        elif choice == "2":
            name = input("Enter VIP customer name: ").strip()
            service = input("Enter VIP service needed: ").strip()
            if not name:
                name = "VIP Customer"
            if not service:
                service = "Priority Advisory"
            cust = sim.register_customer(name, service, is_vip=True)
            print(f"VIP Ticket Issued: {cust.ticket_id} for {cust.name} (Priority Queue)")

        elif choice == "3":
            served = sim.serve_customer()
            if served:
                tier = "VIP" if served.is_vip else "Regular"
                print(f"\n[NOW SERVING] Ticket: {served.ticket_id} | Name: {served.name} ({tier}) | Service: {served.service_type}")
            else:
                print("No customers currently waiting to be served.")

        elif choice == "4":
            nxt = sim.peek_next_customer()
            if nxt:
                tier = "VIP" if nxt.is_vip else "Regular"
                print(f"Next in Line: [{nxt.ticket_id}] {nxt.name} ({tier} - {nxt.service_type})")
            else:
                print("Waiting line is completely empty.")

        elif choice == "5":
            sim.display_status()

        elif choice == "6":
            print("Exiting Customer Service Simulation. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 6.")


if __name__ == "__main__":
    main()

