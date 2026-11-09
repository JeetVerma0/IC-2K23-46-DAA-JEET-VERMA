"""
Program 11: Search Engine Simulator (Dictionary & Collision Resolution)
Course: IC-307D Data Structures and Algorithms Lab
Unit 2: Sorting and Searching Algorithms (CO2)

This program implements a search engine dictionary storing word-definition pairs:
1. Binary Search over a sorted word list.
2. Manual Hash Table using Separate Chaining (linked buckets).
3. Manual Hash Table using Linear Probing (open addressing).
4. Custom polynomial rolling hash function without relying on Python's built-in hash.
5. Collision handling demonstration and architectural comparison.
6. Menu-driven interface and automated self-tests.
"""

import sys
from typing import Any, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Custom Polynomial Rolling Hash Function
# ---------------------------------------------------------------------------

def custom_hash(key: str, table_size: int) -> int:
    """
    Computes a deterministic hash index using polynomial rolling hash:
        hash = (sum(ord(char) * (PRIME ** i))) % table_size
    where PRIME = 31.

    Args:
        key: The string word to hash.
        table_size: Number of slots in the hash table.

    Returns:
        Integer index in range [0, table_size - 1].
    """
    prime = 31
    hash_val = 0
    p_pow = 1

    for char in key.lower():
        hash_val = (hash_val + ord(char) * p_pow) % table_size
        p_pow = (p_pow * prime) % table_size

    return hash_val


# ---------------------------------------------------------------------------
# 1. Sorted List with Binary Search
# ---------------------------------------------------------------------------

class BinarySearchDictionary:
    """Stores word-definition pairs in a sorted array and searches via Binary Search."""

    def __init__(self) -> None:
        # List of tuples: [(word, definition), ...]
        self.entries: List[Tuple[str, str]] = []

    def insert(self, word: str, definition: str) -> None:
        """Inserts or updates an entry while maintaining alphabetical sorted order."""
        clean_word = word.strip().lower()
        clean_def = definition.strip()

        # Check if word already exists (update definition)
        for i, (w, _) in enumerate(self.entries):
            if w == clean_word:
                self.entries[i] = (clean_word, clean_def)
                return

        # Find position to insert maintaining sorted order
        idx = 0
        while idx < len(self.entries) and self.entries[idx][0] < clean_word:
            idx += 1

        self.entries.insert(idx, (clean_word, clean_def))

    def search(self, word: str) -> Optional[Tuple[str, int]]:
        """
        Binary search for word.

        Returns:
            Tuple of (definition, comparisons_count) if found; None otherwise.
        """
        target = word.strip().lower()
        low = 0
        high = len(self.entries) - 1
        comparisons = 0

        while low <= high:
            comparisons += 1
            mid = low + (high - low) // 2
            current_word = self.entries[mid][0]

            if current_word == target:
                return self.entries[mid][1], comparisons
            elif current_word < target:
                low = mid + 1
            else:
                high = mid - 1

        return None

    def display(self) -> None:
        """Displays sorted dictionary entries."""
        if not self.entries:
            print("  Dictionary is currently empty.")
            return
        print(f"  Sorted Dictionary ({len(self.entries)} entries):")
        for idx, (w, d) in enumerate(self.entries):
            print(f"    [{idx}] {w:<15} : {d}")


# ---------------------------------------------------------------------------
# 2. Hash Table with Separate Chaining
# ---------------------------------------------------------------------------

class SeparateChainingHashTable:
    """
    Hash Table resolving collisions via Separate Chaining:
    - Each bucket is a list of (word, definition) pairs.
    """

    def __init__(self, capacity: int = 11) -> None:
        self.capacity = capacity
        # Array of buckets (chains)
        self.buckets: List[List[Tuple[str, str]]] = [[] for _ in range(capacity)]
        self.count = 0

    def insert(self, word: str, definition: str) -> None:
        """Inserts or updates a key-value pair in the appropriate chain."""
        clean_word = word.strip().lower()
        clean_def = definition.strip()
        idx = custom_hash(clean_word, self.capacity)

        chain = self.buckets[idx]
        for i, (w, _) in enumerate(chain):
            if w == clean_word:
                chain[i] = (clean_word, clean_def)
                return

        chain.append((clean_word, clean_def))
        self.count += 1

    def search(self, word: str) -> Optional[Tuple[str, int, int]]:
        """
        Searches for word.

        Returns:
            (definition, bucket_index, probes_in_chain) if found; None otherwise.
        """
        clean_word = word.strip().lower()
        idx = custom_hash(clean_word, self.capacity)
        chain = self.buckets[idx]

        for probe_num, (w, d) in enumerate(chain, start=1):
            if w == clean_word:
                return d, idx, probe_num

        return None

    def display(self) -> None:
        """Prints the full bucket array and active chains."""
        print(f"\n--- Separate Chaining Hash Table (Capacity: {self.capacity}, Items: {self.count}) ---")
        for i in range(self.capacity):
            chain = self.buckets[i]
            if chain:
                chain_str = " -> ".join(f"[{w}: '{d}']" for w, d in chain)
                print(f"  Bucket {i:2d} ({len(chain)} item{'s' if len(chain) > 1 else ''}): {chain_str}")
            else:
                print(f"  Bucket {i:2d}: [EMPTY]")


# ---------------------------------------------------------------------------
# 3. Hash Table with Linear Probing
# ---------------------------------------------------------------------------

class LinearProbingHashTable:
    """
    Hash Table resolving collisions via Linear Probing (Open Addressing):
    - When slot h = hash(key) is occupied, inspects (h + 1)%N, (h + 2)%N, ...
    """

    def __init__(self, capacity: int = 11) -> None:
        self.capacity = capacity
        # Array of slots: None if empty, or (word, definition)
        self.slots: List[Optional[Tuple[str, str]]] = [None] * capacity
        self.count = 0

    def insert(self, word: str, definition: str) -> None:
        """
        Inserts or updates using linear probing.

        Raises:
            OverflowError: If table is full.
        """
        clean_word = word.strip().lower()
        clean_def = definition.strip()

        if self.count >= self.capacity:
            raise OverflowError("Hash Table is full (Linear Probing capacity reached).")

        start_idx = custom_hash(clean_word, self.capacity)
        idx = start_idx

        while True:
            entry = self.slots[idx]

            # Empty slot found -> insert
            if entry is None:
                self.slots[idx] = (clean_word, clean_def)
                self.count += 1
                return

            # Key already exists -> update
            if entry[0] == clean_word:
                self.slots[idx] = (clean_word, clean_def)
                return

            # Linear probe to next slot
            idx = (idx + 1) % self.capacity

            if idx == start_idx:
                raise OverflowError("Hash Table is completely full.")

    def search(self, word: str) -> Optional[Tuple[str, int, int]]:
        """
        Searches for word using linear probing.

        Returns:
            (definition, slot_index, probe_count) if found; None otherwise.
        """
        clean_word = word.strip().lower()
        start_idx = custom_hash(clean_word, self.capacity)
        idx = start_idx
        probes = 0

        while True:
            probes += 1
            entry = self.slots[idx]

            # If empty slot reached, key is not in table
            if entry is None:
                return None

            if entry[0] == clean_word:
                return entry[1], idx, probes

            idx = (idx + 1) % self.capacity

            if idx == start_idx or probes >= self.capacity:
                return None

    def display(self) -> None:
        """Prints all slots in linear array."""
        print(f"\n--- Linear Probing Hash Table (Capacity: {self.capacity}, Items: {self.count}) ---")
        for i in range(self.capacity):
            entry = self.slots[i]
            if entry is not None:
                print(f"  Slot {i:2d}: [{entry[0]}: '{entry[1]}']")
            else:
                print(f"  Slot {i:2d}: [EMPTY]")


# ---------------------------------------------------------------------------
# Collision Handling Comparison and Discussion
# ---------------------------------------------------------------------------

def explain_collision_handling() -> None:
    """Prints a comparative conceptual analysis of collision handling techniques."""
    comparison = """
==============================================================================
      COLLISION RESOLUTION COMPARISON: SEPARATE CHAINING vs LINEAR PROBING
==============================================================================
Feature                  Separate Chaining               Linear Probing
------------------------------------------------------------------------------
Data Structure           Array of linked lists/chains    Single flat array of slots
Load Factor (alpha)      Can exceed 1.0 (alpha > 1)      Must strictly stay < 1.0
Clustering Effect        No clustering                   Primary Clustering occurs
Cache Locality           Poorer (pointer traversing)     Superior (contiguous array)
Deletion Complexity      Simple node removal             Requires tombstone markers
Memory Overhead          Extra pointer/reference space  Requires larger preallocated array
Worst-Case Performance   O(n) if all keys hash to 1 chain O(n) when clusters merge
Best Suited For          Unknown item count; high load   Known fixed capacity; cache speed
==============================================================================
"""
    print(comparison)


# ---------------------------------------------------------------------------
# Built-in Self-Tests
# ---------------------------------------------------------------------------

def run_self_tests() -> None:
    """Verifies all components: binary search dictionary, chaining, and linear probing."""
    print("=" * 60)
    print("RUNNING SELF-TESTS: Search Engine Simulator (Program 11)")
    print("=" * 60)

    # 1. Binary Search Dictionary Tests
    bs_dict = BinarySearchDictionary()
    bs_dict.insert("banana", "A yellow tropical fruit")
    bs_dict.insert("apple", "A round edible fruit")
    bs_dict.insert("cherry", "A small red stone fruit")

    # Order must be: apple, banana, cherry
    words = [w for w, _ in bs_dict.entries]
    assert words == ["apple", "banana", "cherry"], f"Unexpected sort: {words}"
    print("  [Test 1 Passed] Binary Search Dictionary preserves alphabetical sort.")

    res_bs = bs_dict.search("banana")
    assert res_bs is not None and res_bs[0] == "A yellow tropical fruit"
    assert bs_dict.search("missing") is None
    print("  [Test 2 Passed] Binary Search locates target and handles missing keys.")

    # 2. Separate Chaining Tests & Deliberate Collision Handling
    chain_table = SeparateChainingHashTable(capacity=5)
    # Insert multiple items into capacity=5 to guarantee collisions
    chain_table.insert("cat", "Feline domestic animal")
    chain_table.insert("dog", "Canine loyal pet")
    chain_table.insert("bat", "Nocturnal flying mammal")
    chain_table.insert("rat", "Rodent species")
    chain_table.insert("cow", "Bovine domestic animal")
    chain_table.insert("pig", "Swine farm animal")

    assert chain_table.count == 6
    # Verify retrieval of all elements despite collisions
    for w in ["cat", "dog", "bat", "rat", "cow", "pig"]:
        found = chain_table.search(w)
        assert found is not None, f"Failed to retrieve {w} in separate chaining"
    print("  [Test 3 Passed] Separate Chaining correctly resolved collisions and retrieved all keys.")

    # 3. Linear Probing Tests & Deliberate Collision Handling
    probe_table = LinearProbingHashTable(capacity=7)
    probe_table.insert("cat", "Feline domestic animal")
    probe_table.insert("dog", "Canine loyal pet")
    probe_table.insert("bat", "Nocturnal flying mammal")
    probe_table.insert("rat", "Rodent species")

    assert probe_table.count == 4
    for w in ["cat", "dog", "bat", "rat"]:
        found = probe_table.search(w)
        assert found is not None, f"Failed to retrieve {w} in linear probing"
    print("  [Test 4 Passed] Linear Probing successfully resolved collisions and retrieved all keys.")

    # Missing search in linear probing
    assert probe_table.search("unicorn") is None
    print("  [Test 5 Passed] Linear Probing handles missing search correctly.")

    print("\nAll Program 11 self-tests PASSED successfully!")


# ---------------------------------------------------------------------------
# Interactive Menu
# ---------------------------------------------------------------------------

def main() -> None:
    """Interactive command-line driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_self_tests()
        sys.exit(0)

    bs_dict = BinarySearchDictionary()
    chain_table = SeparateChainingHashTable(capacity=7)
    probe_table = LinearProbingHashTable(capacity=7)

    # Initial knowledge base
    initial_pairs = [
        ("algorithm", "A finite set of unambiguous instructions to solve a problem"),
        ("array", "A contiguous linear data structure with indexed element access"),
        ("hashing", "Mapping variable-length keys to fixed-size table indices"),
        ("recursion", "A problem-solving method where a function calls itself"),
        ("stack", "A LIFO linear collection supporting push and pop"),
        ("queue", "A FIFO linear collection supporting enqueue and dequeue")
    ]

    for w, d in initial_pairs:
        bs_dict.insert(w, d)
        chain_table.insert(w, d)
        probe_table.insert(w, d)

    menu = """
========================================
     SEARCH ENGINE SIMULATOR (CO2)
========================================
1. Add Word-Definition Pair (All Stores)
2. Search Word using Binary Search
3. Search Word using Separate Chaining
4. Search Word using Linear Probing
5. Display Binary Search Dictionary
6. Display Separate Chaining Hash Table
7. Display Linear Probing Hash Table
8. View Collision Handling Architecture Comparison
9. Run Automated Self-Tests
10. Exit
========================================
"""

    while True:
        print(menu)
        choice = input("Enter choice (1-10): ").strip()

        if choice == "1":
            w = input("Enter word: ").strip()
            d = input("Enter definition: ").strip()
            if not w or not d:
                print("Error: Word and definition cannot be empty.")
                continue
            bs_dict.insert(w, d)
            chain_table.insert(w, d)
            try:
                probe_table.insert(w, d)
                print(f"Added '{w}' to all search stores successfully.")
            except OverflowError as err:
                print(f"Added to Binary Search & Chaining. Linear Probing Error: {err}")

        elif choice == "2":
            target = input("Enter word to search (Binary Search): ").strip()
            res = bs_dict.search(target)
            if res:
                definition, comps = res
                print(f"\n[Found via Binary Search] '{target}': {definition}")
                print(f"  Comparisons required: {comps}")
            else:
                print(f"\n[Not Found] '{target}' does not exist in Binary Search Dictionary.")

        elif choice == "3":
            target = input("Enter word to search (Separate Chaining): ").strip()
            res = chain_table.search(target)
            if res:
                definition, bucket, probes = res
                print(f"\n[Found via Separate Chaining] '{target}': {definition}")
                print(f"  Located in Bucket: {bucket} | Probes in Chain: {probes}")
            else:
                print(f"\n[Not Found] '{target}' does not exist in Separate Chaining Table.")

        elif choice == "4":
            target = input("Enter word to search (Linear Probing): ").strip()
            res = probe_table.search(target)
            if res:
                definition, slot, probes = res
                print(f"\n[Found via Linear Probing] '{target}': {definition}")
                print(f"  Located at Slot: {slot} | Linear Probes: {probes}")
            else:
                print(f"\n[Not Found] '{target}' does not exist in Linear Probing Table.")

        elif choice == "5":
            bs_dict.display()

        elif choice == "6":
            chain_table.display()

        elif choice == "7":
            probe_table.display()

        elif choice == "8":
            explain_collision_handling()

        elif choice == "9":
            run_self_tests()

        elif choice == "10":
            print("Exiting Search Engine Simulator. Goodbye!")
            break

        else:
            print("Invalid choice! Please select 1-10.")


if __name__ == "__main__":
    main()

