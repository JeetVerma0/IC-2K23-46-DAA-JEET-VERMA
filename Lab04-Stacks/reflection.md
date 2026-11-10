# Student Reflection — Unit 4: Stacks

**Course:** IC-307D: Data Structures and Algorithms Lab  
**Student Name / Roll:** Student Lab Reflection  
**Topic:** Unit 4: Stacks (CO1)  

---

## 1. Understanding LIFO and the Mechanics of Stacks

Before completing this lab unit, I had used stacks primarily as an abstract concept—knowing the acronym LIFO (Last-In, First-Out) and that function calls in programming languages run on a "call stack." Implementing stacks from scratch across eight distinct programs gave me a concrete, visceral understanding of what LIFO truly means at the code level.

The defining characteristic of a stack is its strict single-point of access: the **top**. You cannot inspect the middle, modify the bottom, or insert an item into an arbitrary position. While this might initially sound restrictive compared to general lists or arrays, I realized that this very constraint is what makes stacks so powerful and mathematically predictable:
- **Reversal Property**: Reversing a sequence becomes trivial with a stack—pushing elements in order and popping them out yields the exact reverse sequence. We used this exact property in [Program 04: Infix to Prefix](file:///home/jeet/Desktop/Data_structures/Lab04-Stacks/Program04-InfixToPrefix/infix_to_prefix.py) to invert the token stream and reverse the Shunting-Yard output.
- **Nested Context Tracking**: Whenever a problem involves nested structures—such as parentheses `((A + B) * C)` or nested function calls—a stack naturally preserves the outer context while resolving the innermost sub-problem first.

---

## 2. Difference Between Static and Dynamic Stacks in Practice

Implementing both [Program 01: Static Stack](file:///home/jeet/Desktop/Data_structures/Lab04-Stacks/Program01-StaticStack/static_stack.py) and [Program 02: Dynamic Stack](file:///home/jeet/Desktop/Data_structures/Lab04-Stacks/Program02-DynamicStack/dynamic_stack.py) showed me the practical trade-offs between contiguous arrays and linked heap structures:

### 1. Static Stack (Fixed Capacity)
- **What I Observed**: In Program 01, we preallocate an array of size $C$ upfront (`[None] * capacity`). Pushing and popping simply increment or decrement an integer index `_top`.
- **The Trade-Off**: It is extremely fast because index math in contiguous memory has zero pointer overhead and great CPU cache locality. However, the fixed capacity limit is an immediate bottleneck. In my tests, pushing 4 items into a capacity-3 stack immediately triggered a `Stack Overflow` (`OverflowError`). In real embedded systems or operating system kernels, allocating too much static memory wastes precious RAM, while allocating too little causes fatal overflows.

### 2. Dynamic Stack (Linked List)
- **What I Observed**: In Program 02, we eliminated fixed arrays entirely. Each element is an independent [`StackNode`](file:///home/jeet/Desktop/Data_structures/Lab04-Stacks/Program02-DynamicStack/dynamic_stack.py#L27) linked to its predecessor.
- **The Trade-Off**: Pushing an element dynamically allocates a new node on the heap and points its `next` to `top`. `pop()` simply moves `top = top.next`. The stack never suffers from stack overflow (until physical RAM is exhausted). However, every node carries an extra pointer reference ($8$ bytes), and allocating nodes scattered across heap memory has poorer cache prefetching than a contiguous array.

---

## 3. How Stacks Power Expression Conversion and Evaluation

Before this lab, arithmetic expressions like `(10 + 20) * 3` felt trivial because we take operator precedence for granted. But computers cannot natively "glance" at an entire expression to decide which operator has higher priority. Implementing Programs 03 through 07 showed me how stacks solve this fundamental computer science problem:

1. **Infix Ambiguity vs. Postfix Clarity**:
   In Infix notation ($A + B * C$), the operator sits between operands, forcing compilers to scan back and forth and remember precedence rules or parentheses. In Postfix ($A\ B\ C\ *\ +$) and Prefix ($+\ A\ *\ B\ C$), **parentheses are completely unnecessary**, and evaluation requires only a single sequential pass.
2. **Postfix Evaluation Mechanics**:
   In [Program 05](file:///home/jeet/Desktop/Data_structures/Lab04-Stacks/Program05-PostfixEvaluation/postfix_evaluation.py), evaluating `10 20 + 3 *` was astonishingly simple with an operand stack:
   - When we see a number, push it.
   - When we see an operator `+`, pop the top two numbers ($20$ and $10$), add them ($30$), and push the result back.
   - When we see `*`, pop $3$ and $30$, multiply ($90$), and push back.
   - At the end, the only number remaining on the stack is the final answer ($90$).
3. **Prefix Evaluation (Right-to-Left)**:
   In [Program 06](file:///home/jeet/Desktop/Data_structures/Lab04-Stacks/Program06-PrefixEvaluation/prefix_evaluation.py), I learned that scanning prefix from right to left makes evaluation almost identical to postfix, with one critical subtlety: *the first popped element is the left operand, and the second popped element is the right operand*.

---

## 4. Handling Operator Precedence, Associativity, and Parentheses

Mastering Dijkstra's Shunting-Yard algorithm across Programs 03, 04, and 07 required careful attention to mathematical details:

### 1. Left-Associative vs. Right-Associative Operators
- Standard operators ($+$, $-$, $*$, $/$, $/ /$, $\%$) are left-associative ($A - B - C \implies (A - B) - C$). When an incoming operator arrives, it must pop any operator on the stack that has **greater or equal** precedence.
- Exponentiation (`^`) is right-associative ($A \text{ \textasciicircum } B \text{ \textasciicircum } C \implies A \text{ \textasciicircum } (B \text{ \textasciicircum } C)$). When an incoming `^` arrives, it must only pop operators with **strictly greater** precedence. Because no operator has higher precedence than `^`, an incoming `^` never pops another `^`—they accumulate on the stack and resolve from right to left!
- In our tests, `2 ^ 3 ^ 2` correctly evaluated to $2^{(3^2)} = 2^9 = 512$, not $(2^3)^2 = 64$.

### 2. Parentheses as Priority Shields
Parentheses completely override normal precedence. When `(` is pushed onto the stack, it acts as a boundary barrier: no operator can pop past `(`. When `)` appears, the algorithm pops and outputs everything until `(` is reached, effectively resolving the enclosed sub-expression before anything else.

### 3. Reversal Nuance in Infix to Prefix
In Program 04, converting Infix to Prefix by reversing the token stream required inverting the associativity comparison:
- In reverse order, left-associative operators must pop only when incoming precedence is strictly less than stack top (`prec1 < prec2`).
- Right-associative operators must pop when incoming precedence is less than or equal (`prec1 <= prec2`).
Getting this rule right was what allowed expressions like `A - B - C` to convert cleanly to `- - A B C`.

---

## 5. How Undo and Redo Work Using Dual Stacks

In [Program 08: Undo/Redo Text Editor](file:///home/jeet/Desktop/Data_structures/Lab04-Stacks/Program08-UndoRedo/undo_redo.py), I saw how two collaborating LIFO stacks implement the Command / Memento pattern:

1. **State Snapshots on `undo_stack`**:
   Every time the user types (`insert_text`) or deletes text, the editor takes a snapshot of `current_text` and pushes it onto `undo_stack`.
2. **Undo Action**:
   Pressing Undo pops the previous state from `undo_stack` and restores it, while simultaneously pushing the discarded state onto `redo_stack`.
3. **Redo Action**:
   Pressing Redo pops the undone state from `redo_stack` and restores it, pushing the active state back onto `undo_stack`.
4. **The Golden Invalidation Rule**:
   The most important architectural lesson was understanding what happens when a user presses Undo, and then immediately types something new. If the user undoes to `"Hello"` and types `"!"`, the old redo history (which contained `"Hello World"`) becomes completely invalid! The editor branches into a new timeline. Forgetting to call `self.redo_stack.clear()` would allow the user to redo into an impossible state. Writing Test 06 specifically verified that new edits wipe the redo stack cleanly.

---

## 6. Actual Difficulties Encountered and Possible Improvements

### 1. Difficulties Encountered
- **Tokenizing Multi-Digit Numbers and Unary Negation**:
  In [Program 07: Expression Evaluator](file:///home/jeet/Desktop/Data_structures/Lab04-Stacks/Program07-ExpressionEvaluator/expression_evaluator.py), single-character splitting fails completely for expressions like `100 + 25` or `-(4 + 2)`. Distinguishing a subtraction operator from a negative sign was tricky. I solved this by checking context: if a `-` occurs at index 0 or immediately after another operator or `(`, it is unary. If followed by a number, I bundled it into a negative literal (`"-5"`); if followed by `(`, I converted it to `(0 - ...)`.
- **Division by Zero in Complex Expressions**:
  In postfix and prefix evaluation, expressions like `(10 + 5) / (2 - 2)` cause floor division or modulo by zero. Catching `b == 0` for `/`, `//`, and `%` before applying Python arithmetic prevented ugly crashes and raised clean `ZeroDivisionError` exceptions.
- **Unbalanced Parentheses Validation**:
  Initially, expressions like `(A + B` left an unpopped `(` on the stack when the expression finished. Adding a final stack scan to verify that no `(` remained ensured mismatched parentheses were detected every time.

### 2. Improvements for Future Implementations
If expanding these programs in the future, I would:
1. **Support Scientific and Multi-Argument Functions**:
   Extend the Shunting-Yard parser to handle functions like `sin(x)`, `cos(x)`, `sqrt(x)`, and `max(a, b)` by treating function names as operators with high precedence and comma separators as argument delimiters.
2. **Memory-Efficient Delta Undo (Command Pattern)**:
   Currently, Program 08 snapshots the entire string state on each mutation ($O(n)$ space per edit). For a million-character document, storing full copies consumes excessive memory. Replacing state snapshots with reversible command objects (`InsertCommand(offset, text)`, `DeleteCommand(offset, text)`) would reduce memory consumption to $O(\text{change\_size})$.
3. **Array-Based Resizing Stack (Geometric Doubling)**:
   Implement a dynamic array stack that doubles its capacity when full and halves when one-quarter full (like Python's internal `list` implementation). This would combine the contiguous cache locality of static stacks with the unbounded growth of linked stacks in amortized $O(1)$ time.

