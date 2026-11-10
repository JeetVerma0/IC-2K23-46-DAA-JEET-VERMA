# Student Reflection — Unit 2: Sorting and Searching Algorithms

**Course:** IC-307D: Data Structures and Algorithms Lab  
**Student Name / Roll:** Student Lab Reflection  
**Topic:** Unit 2: Sorting and Searching Algorithms (CO2)  

---

## 1. What I Learned About Sorting and Searching

Before completing this laboratory unit, I viewed sorting algorithms primarily as abstract flowcharts and asymptotic formulas. Implementing all seven sorting algorithms, binary search, and dictionary data structures completely from first principles in Python—without using built-ins like `.sort()`, `sorted()`, `bisect`, or `heapq`—transformed my understanding of algorithm design.

I learned that sorting is not just about arranging numbers; it is an architectural decision that directly influences the performance of downstream systems:
1. **The Cost of Contiguity and Shifting**: In [Insertion Sort](file:///home/jeet/Desktop/Data_structures/Lab02-Sorting-Searching/Program03-InsertionSort/insertion_sort.py), I experienced the physical cost of preserving array contiguity. Inserting a single out-of-order element into a sorted array requires shifting elements one by one. Conversely, when data is already ordered, Insertion Sort skips shifting altogether, achieving an optimal linear scan $O(n)$.
2. **Divide-and-Conquer Partitioning**: Implementing [Merge Sort](file:///home/jeet/Desktop/Data_structures/Lab02-Sorting-Searching/Program04-MergeSort/merge_sort.py) and [Quick Sort](file:///home/jeet/Desktop/Data_structures/Lab02-Sorting-Searching/Program05-QuickSort/quick_sort.py) highlighted the distinction between *dividing* work versus *combining* work. In Merge Sort, the division is trivial (halving at the midpoint), but all the real work happens during the linear two-pointer merge. In Quick Sort, the division (partitioning around a pivot) does all the heavy lifting, while combining the sub-arrays requires no additional work.
3. **Implicit Tree Representation**: In [Heap Sort](file:///home/jeet/Desktop/Data_structures/Lab02-Sorting-Searching/Program06-HeapSort/heap_sort.py), I learned how a complete binary tree can be mapped directly onto a flat array using index arithmetic ($2i + 1$ and $2i + 2$). This avoids pointer overhead completely, allowing us to build an in-place priority queue and sort with zero auxiliary allocations.
4. **Binary Search Invariants**: For [Binary Search](file:///home/jeet/Desktop/Data_structures/Lab02-Sorting-Searching/Program08-BinarySearch/binary_search.py), I realized that logarithmic search is only possible because the data structure guarantees random index access and monotonic ordering. Verifying sortedness before searching reinforced why maintaining a sorted collection is worth the upfront sorting cost when frequent queries occur.

---

## 2. Differences Between Comparison-Based and Non-Comparison Sorting

Working with both types of sorting algorithms helped me understand the theoretical and practical boundaries that separate them:

### Theoretical Boundary: The $\Omega(n \log n)$ Barrier
Comparison-based sorts (Bubble, Selection, Insertion, Merge, Quick, Heap) operate under the assumption that we know nothing about the keys except whether $A[i] \le A[j]$. Any algorithm relying strictly on pairwise comparisons can be modeled as a binary decision tree. Because there are $n!$ possible permutations of an input list, the decision tree must have at least $n!$ leaves. The minimum height of such a tree is:
$$h \ge \log_2(n!) \approx n \log_2 n - n \log_2 e = \Omega(n \log n)$$
Thus, no comparison sort can ever run faster than $O(n \log n)$ in the worst case.

### Non-Comparison Sorting: Breaking the Lower Bound
In [Radix Sort](file:///home/jeet/Desktop/Data_structures/Lab02-Sorting-Searching/Program07-RadixSort/radix_sort.py), we completely discarded pairwise comparisons. Instead, the algorithm inspects the numerical representation of keys digit by digit.
- By using an intermediate stable **Counting Sort** for each digit place ($1\text{s}, 10\text{s}, 100\text{s}$), the algorithm distributes elements into 10 buckets ($0$ to $9$) and reassembles them using prefix sum indices.
- Because the number of digits $d = \lfloor \log_{10}(\text{max\_val}) \rfloor + 1$ is bounded (for our numbers up to $10000$, $d \le 5$), Radix Sort achieves total time:
  $$O(d \cdot (n + b)) = O(n)$$
- In our empirical tests at $N = 1000$, Radix Sort took only $0.4297\text{ ms}$, scaling strictly linearly.

### Trade-Offs Observed
However, non-comparison sorting is not universally superior:
1. **Domain Constraints**: Radix Sort requires keys to have a well-defined digit or byte structure and strictly non-negative integer representation. Passing negative numbers like `-5` causes invalid array index calculations, which required me to implement explicit input validation to raise a `ValueError`.
2. **Auxiliary Memory**: While Quick Sort and Heap Sort operate in-place or with $O(\log n)$ stack frames, Radix Sort allocates $O(n + b)$ auxiliary buffers for intermediate digit counts and output reassembly.
3. **Generality**: Comparison sorts can sort arbitrary objects (strings, tuples, custom classes) as long as a less-than operator is defined, whereas Radix Sort requires specialized digit-extraction logic for each data type.

---

## 3. The Importance of Input Characteristics

One of the most striking lessons from this lab was how significantly input characteristics (initial ordering, duplicates, and list size) dictate algorithm performance.

### 1. The Pre-Sorted Dataset ($N = 1000$)
- In theoretical analysis, Bubble Sort and Insertion Sort are classified as slow $O(n^2)$ algorithms. Yet, when tested on an already-sorted list of $1000$ elements:
  - **Bubble Sort (with `swapped` flag)** took only **$0.0266\text{ ms}$**.
  - **Insertion Sort** took only **$0.0421\text{ ms}$**.
  - Meanwhile, **Merge Sort** took **$0.5364\text{ ms}$** and **Heap Sort** took **$1.0171\text{ ms}$**.
- This taught me that on nearly-sorted data, an algorithm with an $O(n)$ best-case and small constant factors runs **over 20 to 38 times faster** than divide-and-conquer algorithms that blindly recurse and rebuild trees.

### 2. The Invariance of Selection Sort
Unlike Bubble and Insertion Sort, [Selection Sort](file:///home/jeet/Desktop/Data_structures/Lab02-Sorting-Searching/Program02-SelectionSort/selection_sort.py) showed virtually zero change across data distributions:
- Random data ($N = 1000$): $9.1236\text{ ms}$
- Sorted data ($N = 1000$): $8.9668\text{ ms}$
- Reverse data ($N = 1000$): $9.4397\text{ ms}$
Because Selection Sort's inner loop scans the entire unsorted suffix for the minimum element regardless of whether the list is already sorted, it executes all $n(n-1)/2$ comparisons unconditionally.

### 3. The Reverse-Sorted Trap
On the reverse-sorted dataset:
- Insertion Sort degraded from $0.0421\text{ ms}$ (sorted) to $15.9960\text{ ms}$ (reverse)—a massive **$380\times$ slowdown**—because every single key had to shift across the entire prefix.
- Merge Sort and Heap Sort, by contrast, showed rock-solid stability ($0.5422\text{ ms}$ and $0.8798\text{ ms}$), proving their resilience in systems where worst-case performance guarantees are essential.

---

## 4. What I Learned from Empirical Performance Testing

Running [Program 09: Sorting Performance Analysis](file:///home/jeet/Desktop/Data_structures/Lab02-Sorting-Searching/Program09-PerformanceAnalysis/sorting_comparison.py) and generating the Matplotlib comparison graphs bridged the gap between asymptotic notation and physical execution time:

### 1. Verifying Theoretical Scaling Factors
When increasing input size by $10\times$ ($N = 100 \to 1000$):
- **Quadratic Sorts ($O(n^2)$)**:
  - Bubble Sort on random data jumped from $0.2193\text{ ms}$ to $22.2761\text{ ms}$ ($\approx 101.6\times$ increase).
  - Selection Sort jumped from $0.1072\text{ ms}$ to $9.1236\text{ ms}$ ($\approx 85.1\times$ increase).
  - Insertion Sort jumped from $0.0976\text{ ms}$ to $8.3944\text{ ms}$ ($\approx 86.0\times$ increase).
  - This perfectly matches the theoretical $10^2 = 100\times$ scaling.
- **Log-Linear Sorts ($O(n \log n)$)**:
  - Merge Sort increased from $0.0580\text{ ms}$ to $0.6795\text{ ms}$ ($11.7\times$).
  - Quick Sort increased from $0.0330\text{ ms}$ to $0.4582\text{ ms}$ ($13.9\times$).
  - Heap Sort increased from $0.0779\text{ ms}$ to $0.9785\text{ ms}$ ($12.6\times$).
  - This matches $10 \times \frac{\log_2(1000)}{\log_2(100)} \approx 10 \times 1.5 = 15\times$.
- **Linear Sort ($O(n)$)**:
  - Radix Sort scaled from $0.0477\text{ ms}$ to $0.4297\text{ ms}$ ($9.0\times$), demonstrating linear behavior.

### 2. The Power of Pivot Selection in Quick Sort
In theoretical textbooks, standard Quick Sort degrades to $O(n^2)$ on already-sorted or reverse-sorted lists if the pivot is chosen as the first or last element. In our implementation, I used **median-of-three pivot selection** (`_median_of_three`). The empirical data proved its effectiveness:
- Quick Sort on sorted data ($N = 1000$) took only **$0.3437\text{ ms}$**.
- Quick Sort on reverse data ($N = 1000$) took only **$0.5280\text{ ms}$**.
This completely eliminated the $O(n^2)$ degradation, making Quick Sort the fastest comparison sort across all random and ordered tests.

---

## 5. Hash Collisions and Collision Resolution

Implementing [Program 11: Search Engine Simulator](file:///home/jeet/Desktop/Data_structures/Lab02-Sorting-Searching/Program11-SearchEngineSimulator/search_engine.py) provided deep practical insight into hashing, hash collisions, and collision resolution architectures:

### 1. Custom Polynomial Rolling Hash
Rather than relying on Python's built-in `hash()`, which includes random salting between process restarts, I implemented a deterministic polynomial rolling hash:
$$\text{hash}(s) = \left( \sum_{i=0}^{L-1} \text{ord}(s[i]) \times 31^i \right) \pmod{\text{capacity}}$$
Using prime base $31$ distributes English strings evenly across the modulo table capacity.

### 2. Separate Chaining (Open Hashing)
- **Mechanism**: The table is an array of buckets, where each bucket holds a linked chain (list) of key-value pairs.
- **Collision Behavior**: When words like `"cat"`, `"dog"`, `"bat"`, and `"rat"` hash to the same bucket index in a table of capacity 5, the new item is simply appended to that bucket's chain.
- **Load Factor ($\alpha = N/M$)**: I observed that Separate Chaining handles $\alpha > 1.0$ without failing. When we inserted 6 items into 5 buckets ($\alpha = 1.2$), all items were retrieved correctly. The search time degrades smoothly to $O(1 + \alpha)$.

### 3. Linear Probing (Open Addressing / Closed Hashing)
- **Mechanism**: The table consists of a flat array of slots. When a collision occurs at slot $h$, the algorithm checks $(h + 1) \pmod M$, $(h + 2) \pmod M$, and so on.
- **Collision Behavior**: In our self-test with capacity 7 and 4 items, collisions forced entries into neighboring free slots.
- **Primary Clustering**: As consecutive slots fill up, contiguous occupied blocks form. Any key hashing into or near this block must traverse the entire cluster, causing search and insertion times to spike.
- **Hard Capacity Bound**: Linear probing strictly requires $\alpha < 1.0$. When the table reaches $100\%$ capacity, inserting an additional key raises an `OverflowError`.

### 4. Direct Architectural Comparison
| Metric | Binary Search Dictionary | Separate Chaining Hash Table | Linear Probing Hash Table |
| :--- | :--- | :--- | :--- |
| **Search Time** | Guaranteed $O(\log n)$ | Expected $O(1)$, Worst $O(n)$ | Expected $O(1)$, Worst $O(n)$ |
| **Insertion Time**| $O(n)$ (element shifting) | Expected $O(1)$ | Expected $O(1)$ (degrades with clustering) |
| **Memory Layout** | Packed contiguous list | Array of bucket pointers | Single flat array of fixed size |
| **Load Capacity** | Unbounded | Tolerates $\alpha > 1.0$ | Strictly requires $\alpha < 1.0$ |
| **Cache Locality**| High | Low (pointer chasing) | High (sequential scans) |

---

## 6. Difficulties Encountered and Improvements

### 1. Difficulties Encountered
1. **Off-by-One Errors in Lomuto Partitioning**:
   In Quick Sort, ensuring that the median-of-three pivot was swapped correctly to index `high` before scanning and that index pointer $i$ incremented properly required careful tracing. Initially, duplicate pivot elements caused infinite recursion until I ensured $A[j] \le \text{pivot}$ correctly managed identical keys.
2. **Reverse Output Traversal in Radix Counting Sort**:
   When implementing `_counting_sort_by_digit` in Radix Sort, iterating forward through the input array when placing elements into `output` broke algorithm stability. This caused higher-order passes to scramble earlier sorted digit orders. Reversing the placement loop (from $n-1$ down to $0$) restored strict stability.
3. **Implicit Max-Heap Indexing**:
   In Heap Sort's `heapify`, boundary checks like `left < n` and `right < n` had to precede array lookups to prevent `IndexError`. Furthermore, distinguishing the heap-building phase (which iterates downward from $\lfloor n/2 \rfloor - 1$ to $0$) from the extraction phase (which reduces the active heap boundary $n-1$ down to $1$) was crucial to avoid overwriting extracted maximum values.
4. **Defensive Validation in Binary Search**:
   Ensuring Binary Search fails gracefully when fed an unsorted array required writing a dedicated $O(n)$ `is_sorted()` check that raises an informative `ValueError` rather than producing silent incorrect search results.

### 2. Improvements for Future Implementations
If extending this codebase in the future, I would implement:
1. **Hybrid Introsort / Timsort**: Combine Quick Sort with Heap Sort and Insertion Sort: start with Quick Sort, switch to Heap Sort if recursion depth exceeds $2 \log_2 n$ to guarantee $O(n \log n)$ worst-case time, and switch to Insertion Sort for partitions of size $n \le 16$.
2. **Quadratic Probing or Double Hashing**: Replace Linear Probing in the search engine with Double Hashing ($h(k, i) = (h_1(k) + i \cdot h_2(k)) \pmod M$) to eliminate primary clustering.
3. **Dynamic Table Resizing (Rehashing)**: Implement automatic table resizing in the hash tables whenever load factor $\alpha$ exceeds $0.75$, doubling the capacity to the next prime number to preserve expected $O(1)$ operations under continuous insertions.
4. **Signed and Floating-Point Radix Sort**: Extend Radix Sort to handle negative integers by partitioning into negative and non-negative sub-arrays, and support floating-point keys via IEEE 754 bit-twiddling.

