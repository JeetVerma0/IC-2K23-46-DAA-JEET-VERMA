# Student Reflection — Unit 6: Trees

**Course:** IC-307D: Data Structures and Algorithms Lab  
**Student Name / Roll:** Student Lab Reflection  
**Topic:** Unit 6: Trees (CO3)  

---

## 1. What I Learned About Tree Structures and Traversals

Coming into Unit 6, all the data structures we had built—arrays, linked lists, stacks, and queues—were strictly linear. Every element had an unambiguous single predecessor and single successor. Transitioning from linear chains to hierarchical trees required a fundamental shift in how I think about data organization.

In a tree, a single parent branches out into multiple children, forming subtrees that mirror the recursive structure of the whole tree. This self-similarity is why trees are so naturally manipulated using recursion:
- **Preorder ($\text{Root} \to \text{Left} \to \text{Right}$)**: Processing the parent before its subtrees felt natural when the parent establishes the context—such as serializing a tree or copying directory paths.
- **Inorder ($\text{Left} \to \text{Root} \to \text{Right}$)**: Seeing Inorder traversal extract keys from a Binary Search Tree in perfectly sorted ascending order was a defining moment for me. It transformed the tree from an abstract drawing into an efficient sorting and searching engine.
- **Postorder ($\text{Left} \to \text{Right} \to \text{Root}$)**: Processing both children before the parent is essential whenever dependencies must be resolved bottom-up, such as evaluating operands before applying an operator in an expression tree or deleting child nodes before freeing the parent directory.

---

## 2. Differences Between Recursive and Iterative Traversals

Implementing both [Program 01 (Recursive)](file:///home/jeet/Desktop/Data_structures/Lab06-Trees/Program01-RecursiveTraversals/recursive_traversals.py) and [Program 02 (Iterative)](file:///home/jeet/Desktop/Data_structures/Lab06-Trees/Program02-IterativeTraversals/iterative_traversals.py) demystified how function calls actually work behind the scenes:

### 1. Recursion: Elegance with Hidden Memory Costs
In Program 01, recursive traversals took only four lines of Python code per method. The elegance is undeniable. However, recursion relies entirely on the system's runtime call stack. For a balanced tree of $10^6$ nodes, height is only $\approx 20$, which easily fits in memory. But if the tree degrades into a skewed linked list of height $1000$, Python immediately crashes with a `RecursionError: maximum recursion depth exceeded`.

### 2. Iteration: Explicit Stacks and Total Control
In Program 02, we eliminated recursion by managing an explicit LIFO stack in our own heap memory:
- **Preorder**: Pushing the right child first so the left child is popped and visited next mirrored the call stack cleanly.
- **Inorder**: Descending down the left spine with a while loop, pushing ancestor nodes, and then backtracking upon hitting `None` showed me the exact mechanical steps that recursion hides.
- **Postorder**: Postorder was by far the trickiest to do iteratively without recursion. Implementing the **Two-Stack algorithm** was an elegant breakthrough: `Stack 1` visits nodes in modified order ($\text{Root} \to \text{Right} \to \text{Left}$), pushing them into `Stack 2`. When `Stack 1` empties, popping `Stack 2` inverts the sequence into exact ($\text{Left} \to \text{Right} \to \text{Root}$) postorder!

---

## 3. Mastering BST Insertion, Search, and Deletion

In [Program 03: Binary Search Tree](file:///home/jeet/Desktop/Data_structures/Lab06-Trees/Program03-BinarySearchTree/binary_search_tree.py), I implemented standard binary search tree mechanics:
- **Insertion & Search**: Navigating left when $k < \text{node.key}$ and right when $k > \text{node.key}$ cuts the remaining search space in half at each step (on a balanced tree), giving $O(\log n)$ efficiency.
- **Handling Deletions**: Deletion was the most complex operation I had implemented so far in DSA because of its three distinct cases:
  1. *Leaf Node*: Trivial to delete; simply return `None`.
  2. *Single Child*: Bypass the deleted node by returning its child directly to the parent pointer.
  3. *Two Children*: You cannot simply remove a node with two children without fracturing the tree into disconnected components. Replacing the node's key with its **inorder successor** (the minimum key in the right subtree) and then deleting that successor from the right subtree preserved the BST invariant cleanly without re-linking the entire subtree.

---

## 4. Why AVL Balancing is Essential

While building the BST in Program 03, I realized its fatal vulnerability: **input order dictates tree shape**. If you insert sorted keys `[10, 20, 30, 40, 50]`, the BST completely degenerates into a linear right-skewed linked list! Search and insertion degrade from $O(\log n)$ to $O(n)$, destroying all benefits of using a tree.

Implementing [Program 04: AVL Tree](file:///home/jeet/Desktop/Data_structures/Lab06-Trees/Program04-AVLTree/avl_tree.py) solved this problem completely:
- Tracking node height and computing the Balance Factor ($\text{BF} = h_{\text{left}} - h_{\text{right}}$) allowed the tree to detect unbalance the instant $|\text{BF}| > 1$.
- Implementing the four rotations gave me a concrete geometric appreciation of how pointer rotations rebalance subtrees:
  - **LL & RR Cases**: A single rotation (Right for LL, Left for RR) brings the middle node to the root and pushes the heavy outer node down.
  - **LR & RL Cases**: A double rotation is required because the imbalance is on an "inner" child. Rotating the child first converts the problem into an outer LL or RR case, which is then resolved by the second rotation.
- In our test suite, inserting `[30, 20, 10]` immediately triggered a right rotation on `30`, promoting `20` to the root with children `10` and `30` at height 2. No matter what order keys were inserted, the AVL tree height remained strictly logarithmic ($O(\log n)$).

---

## 5. Expression Trees: Connecting Trees to Language Compilers

In [Program 05: Expression Tree](file:///home/jeet/Desktop/Data_structures/Lab06-Trees/Program05-ExpressionTree/expression_tree.py), we built a bridge between Unit 4 (Stacks) and Unit 6 (Trees).
- Parsing a postfix string like `"5 3 + 2 ^ 4 /"` using a stack of tree nodes felt like watching a compiler frontend in miniature:
  - Operands become leaf nodes.
  - Operators pop two subtrees and become internal parent nodes.
- Once the tree was constructed, generating notations became effortless:
  - Infix is just an Inorder traversal with parentheses: `(((5 + 3) ^ 2) / 4)`.
  - Prefix is a Preorder traversal: `/ ^ + 5 3 2 4`.
  - Postfix is a Postorder traversal: `5 3 + 2 ^ 4 /`.
- Evaluating the expression recursively without using Python's `eval()` proved how calculators and compiler optimization engines (like constant folding) evaluate syntax trees from the bottom up.

---

## 6. Real-World Applications: File Systems and Compiler Symbol Tables

The final two programs applied trees to solve real software engineering problems:

### 1. File System Simulator (Program 06)
- Modeling a file system as an $N$-ary tree in memory showed me why operating systems use trees for file namespaces.
- Each directory is a tree node containing an arbitrary list of child files and subdirectories.
- Reconstructing absolute paths (`/home/student/projects/dsa_tree.py`) by walking up parent pointers until reaching the root was fast and elegant.
- Adding safety rules—preventing duplicate sibling names, blocking root deletion, and requiring recursive flags to remove non-empty folders—mirrored the behavior of the real Linux `rm` and `mkdir` utilities.

### 2. Compiler Symbol Table (Program 07)
- In Program 07, we built a compiler symbol table backed strictly by a Binary Search Tree instead of a Python dictionary.
- Using identifier names as BST search keys gave us $O(\log n)$ lookup and update speeds.
- More importantly, performing an Inorder traversal on the BST automatically produced all declared program variables in alphabetical order without any sorting overhead!
- Catching duplicate variable declarations on the same line and throwing compile errors for undeclared identifiers connected data structures directly to compiler design.

---

## 7. Implementation Difficulties and Future Improvements

### Difficulties Encountered:
1. **AVL Height Updates During Rotations**:
   When performing a right rotation on node $y$ with left child $x$, $y$ becomes the right child of $x$. In my first attempt, I updated $x$'s height before $y$'s height. Because $x$'s height depends on the newly updated height of $y$, this produced incorrect heights and corrupted balance factors. Updating $y$ first and then $x$ resolved the issue.
2. **Double Rotation Rebalancing on Deletion**:
   During AVL deletion, rebalancing can propagate all the way up to the root, requiring multiple rotations. I had to ensure that every ancestor node along the deletion path recalculated its height and checked its balance factor.
3. **Empty Postfix and Leftover Stack Tokens**:
   In Program 05, expressions like `"10 20 + 30"` left two nodes on the stack. I added strict validation to ensure that exactly one root node remains on the stack after consuming all tokens.
4. **Path Reconstruction in File System**:
   Handling the root directory's name properly so that root displays as `"/"` while child paths display as `"/docs"` without trailing double slashes (`"//docs"`) required careful path joining logic.

### Possible Future Improvements:
1. **Red-Black Trees**: Implement Red-Black tree balancing to compare its rotation frequency against AVL trees (AVL is more strictly balanced, making it faster for lookup-heavy workloads, whereas Red-Black trees require fewer rotations during frequent insertions).
2. **$B$-Trees for Disk-Based Storage**: Extend the file system simulator to use $B$-Trees or $B+$ Trees, simulating how databases read multi-way tree blocks from persistent secondary storage.
3. **Scope Stack for Nested Lexical Scopes**: Enhance the Symbol Table into a scoped symbol table by maintaining a stack of BSTs, enabling local variables in functions to shadow global variables.

