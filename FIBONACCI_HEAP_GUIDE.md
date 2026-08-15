# Fibonacci Heap: Complete Study Guide

## 1. What is a Fibonacci Heap?

A **Fibonacci Heap** is a collection of heap-ordered trees that together form a priority queue.

Unlike a binary heap, it does not maintain one rigid tree shape after every operation. Instead, it uses a **lazy** strategy:

- Insertions are performed immediately.
- New trees can remain in the root list.
- Expensive restructuring is postponed until `extractMin`.
- `decreaseKey` can cut nodes and move them to the root list.

This delayed restructuring is what gives Fibonacci Heaps their excellent **amortized** complexity.

---

## 2. Why is it called a Fibonacci Heap?

The name comes from the relationship between the **maximum possible degree of a node** and the Fibonacci sequence.

The analysis of Fibonacci Heaps shows that the size of a subtree rooted at a node grows at least like a Fibonacci number as the degree increases.

Because Fibonacci numbers grow exponentially, the maximum degree of any node is:

`O(log n)`

where `n` is the number of nodes in the heap.

So the name comes from the mathematical relationship used in its amortized analysis, not because the heap literally stores Fibonacci numbers.

---

## 3. Historical idea

Fibonacci Heaps were introduced by Michael L. Fredman and Robert E. Tarjan in their 1987 paper on Fibonacci Heaps and their uses in improved network optimization algorithms.

The central idea was to create a priority queue where operations such as `insert`, `merge`, and especially `decreaseKey` could be extremely cheap in an amortized sense.

This is useful in algorithms that perform many priority updates, such as:

- Dijkstra's shortest path algorithm
- Prim's minimum spanning tree algorithm
- Certain network optimization algorithms

---

## 4. Why do we need Fibonacci Heaps?

Binary Heaps are already excellent general-purpose priority queues.

However, some algorithms perform a very large number of `decreaseKey` operations.

For a binary heap:

- `insert`: O(log n)
- `extractMin`: O(log n)
- `decreaseKey`: O(log n)

For a Fibonacci Heap:

- `insert`: O(1) amortized
- `findMin`: O(1)
- `union`: O(1) amortized
- `decreaseKey`: O(1) amortized
- `extractMin`: O(log n) amortized

The trade-off is that Fibonacci Heaps are considerably more complicated to implement.

---

## 5. Core structure

A Fibonacci Heap contains:

1. A pointer to the minimum root.
2. A circular doubly linked list of roots.
3. Zero or more heap-ordered trees.
4. A node count.

Each node stores:

```text
key
degree
parent
child
left
right
mark
```

### Key

The priority value stored in the node.

### Degree

The number of direct children of the node.

### Parent

The node's parent, or `None` if the node is a root.

### Child

A pointer to any one child of the node.

### Left / Right

Pointers used to form circular doubly linked lists.

### Mark

A Boolean indicating whether the node has lost a child since it became a child of its current parent.

---

## 6. Heap-order property

The heap follows the min-heap property:

```text
parent.key <= child.key
```

Therefore the minimum key must always be at a root.

The heap keeps a direct pointer to that root:

```text
minNode
```

That makes `findMin()` O(1).

---

## 7. Circular doubly linked lists

The root list and every child list are circular doubly linked lists.

Example:

```text
       ┌─────────────────────────┐
       ↓                         │
     [3] <-> [7] <-> [10] <-> [15]
       ↑                         │
       └─────────────────────────┘
```

Circular means the final node links back to the first.

Doubly linked means every node has both:

```text
left
right
```

This allows insertion and removal from a list in O(1).

---

## 8. Insert

To insert a key:

1. Create a new node.
2. Put it into the root list.
3. Update `minNode` if necessary.

The inserted node is initially:

```text
degree = 0
parent = None
child = None
mark = False
```

### Complexity

**O(1) amortized**

No consolidation is required.

---

## 9. Find-Min

Return the node pointed to by `minNode`.

### Complexity

**O(1)**

---

## 10. Union

Two Fibonacci Heaps can be merged by joining their root lists.

There is no need to immediately combine equal-degree trees.

That is another example of lazy restructuring.

### Complexity

**O(1) amortized**

In this project, `union()` destructively merges the other heap into the current heap and empties the other heap object.

---

## 11. Extract-Min

This is the main expensive operation.

Suppose:

```text
       3
     / | \
    8  10 15
```

If 3 is the minimum:

1. Remove 3.
2. Move its children into the root list.
3. Consolidate roots.
4. Link roots of equal degree.
5. Find the new minimum.

### Why consolidate?

After many insertions and cuts, the root list may contain many unrelated trees, including trees with the same degree.

Consolidation combines equal-degree trees until no two roots have the same degree.

If two roots have the same degree:

```text
A       B
```

the one with the smaller key becomes the parent:

```text
      A
      |
      B
```

This continues until each degree appears at most once.

### Complexity

**O(log n) amortized**

The logarithmic bound follows from the fact that node degrees are logarithmically bounded.

---

## 12. Decrease-Key

Suppose a child has its key reduced below its parent's key:

```text
       20
       |
       30
```

After decreasing 30 to 5:

```text
       20
       |
        5
```

The heap property is violated.

The node is cut:

```text
20

5
```

The cut node becomes a root.

### Complexity

**O(1) amortized**

This is the major advantage of Fibonacci Heaps.

---

## 13. Cascading Cut

A single cut is not always enough.

A node can lose one child and remain attached to its parent by becoming marked.

If it later loses another child, it is cut as well.

This can continue upward.

Example idea:

```text
grandparent
    |
  parent   <- loses a second child
    |
  node
```

The parent may be cut and then the grandparent may also need to be reconsidered.

This process is called a **cascading cut**.

The marking rule prevents long chains of children from being lost without compensation.

---

## 14. Delete

Deleting a node can be reduced to:

```text
decreaseKey(node, -infinity)
extractMin()
```

After decreasing its value to negative infinity, it must become the minimum.

Then `extractMin()` removes it.

### Complexity

**O(log n) amortized**

This project uses numeric keys for `delete()` because it uses negative infinity as the sentinel.

---

## 15. Complexity table

| Operation | Fibonacci Heap |
|---|---:|
| Make-Heap | O(1) |
| Insert | O(1) amortized |
| Find-Min | O(1) |
| Union | O(1) amortized |
| Decrease-Key | O(1) amortized |
| Extract-Min | O(log n) amortized |
| Delete | O(log n) amortized |

The key phrase is **amortized**.

An individual operation can occasionally cost more than the listed value, but the average cost over a sequence of operations is bounded by the amortized complexity.

---

## 16. Why amortized analysis matters

Fibonacci Heaps intentionally allow some operations to be cheap immediately and postpone expensive restructuring.

Think of it as:

```text
cheap work now
      +
postponed cleanup later
```

This is why insertion does not immediately rebalance the heap.

The cost of future restructuring is paid by operations such as `extractMin`.

---

## 17. Potential function

A common amortized analysis uses the potential:

`Φ(H) = t(H) + 2m(H)`

where:

- `t(H)` = number of trees in the root list
- `m(H)` = number of marked nodes

The potential represents stored "future work".

Creating more root trees increases potential.

Cascading cuts can reduce potential.

This allows expensive future restructuring to be accounted for mathematically.

---

## 18. Comparison with Binary Heap

| Feature | Binary Heap | Fibonacci Heap |
|---|---:|---:|
| Insert | O(log n) | O(1) amortized |
| Find-Min | O(1) | O(1) |
| Extract-Min | O(log n) | O(log n) amortized |
| Decrease-Key | O(log n) | O(1) amortized |
| Union | O(n) typical implementation | O(1) amortized |
| Implementation | Simple | Complex |
| Practical overhead | Low | Higher |

Fibonacci Heap is not automatically faster in real programs.

For many normal priority-queue workloads, a binary heap is simpler and has lower constant factors.

Fibonacci Heap becomes theoretically attractive when an algorithm performs many `decreaseKey` and `union` operations.

---

## 19. Comparison with Binomial Heap

A Binomial Heap explicitly maintains a structured collection of binomial trees.

A Fibonacci Heap relaxes the structure and postpones more of the work.

The high-level evolution can be presented as:

```text
Binary Heap
    |
    v
Binomial Heap
    |
    v
Fibonacci Heap
```

This is useful for explaining why Fibonacci Heaps trade structural simplicity for better amortized update complexity.

---

## 20. Real-world and algorithmic applications

### Dijkstra's algorithm

Dijkstra repeatedly selects the closest vertex and may update many other vertices with `decreaseKey`.

Fibonacci Heap improves the theoretical bound of Dijkstra when the graph is sufficiently dense and `decreaseKey` dominates the workload.

### Prim's algorithm

Prim's algorithm for minimum spanning trees also uses a priority queue and can perform many priority updates.

### Network optimization

Fibonacci Heap theory was motivated in part by improved network optimization algorithms.

---

## 21. Advantages

- O(1) amortized insertion.
- O(1) find-min.
- O(1) amortized merge.
- O(1) amortized decrease-key.
- Excellent theoretical performance for priority-update-heavy algorithms.
- Strong connection to amortized analysis.

---

## 22. Limitations

- Much harder to implement than a binary heap.
- More pointers per node.
- Higher memory overhead.
- More pointer manipulation.
- Worse constant factors can make it slower in practical workloads.
- Correctness is harder to verify.
- The benefits depend strongly on workload.

---

## 23. Implementation design used in this project

```text
FibonacciHeap
│
├── minNode
├── nodeCount
│
└── root list
      │
      ├── FibonacciNode
      ├── FibonacciNode
      └── FibonacciNode
             │
             └── child list
```

A `FibonacciNode` contains:

```text
key
degree
parent
child
left
right
mark
```

Public operations:

```text
insert()
findMin()
union()
extractMin()
decreaseKey()
delete()
```

Educational helpers:

```text
isEmpty()
getSize()
validate()
```

Internal algorithmic helpers include:

```text
_addToRootList()
_removeFromRootList()
_removeFromCircularList()
_link()
_consolidate()
_cut()
_cascadingCut()
```

---

## 24. Correctness testing

The project contains:

1. Basic insertion and minimum tests.
2. Sorted extraction tests.
3. Union tests.
4. Decrease-key tests.
5. Delete tests.
6. Randomized tests.
7. Internal invariant validation.

The randomized tests compare the extracted result with Python's `sorted()` result.

The `validate()` function checks:

- root nodes have no parent,
- child-parent pointers agree,
- left/right pointers are consistent,
- heap order is maintained,
- degree matches the number of children,
- every node is visited exactly once,
- total visited nodes equals `nodeCount`.

---

## 25. Experimental analysis

The benchmark stage measures runtime at increasing input sizes.

Typical input sizes:

```text
1,000
5,000
10,000
50,000
100,000
```

The benchmark records:

- input size,
- operation,
- runtime in seconds.

The plotting script converts these measurements into runtime-vs-input-size graphs.

Important:

**Experimental runtime does not prove asymptotic complexity.**

The graphs are used to observe practical behavior and compare it with the theoretically expected trend.

---

## 26. What to say during the presentation

The strongest story for this project is:

> Binary heaps are simple and practical, but some algorithms perform huge numbers of priority updates. Fibonacci Heaps deliberately postpone structural work so that operations such as `decreaseKey` become O(1) amortized. The price is a much more complicated data structure.

That is the central idea to keep coming back to.

---

## 27. Key terms to know before the viva

Be able to explain these without memorizing definitions:

- Heap-order property
- Root list
- Circular doubly linked list
- Node degree
- Minimum pointer
- Lazy consolidation
- Amortized analysis
- Potential function
- Cut
- Cascading cut
- Marked node
- Consolidation
- Decrease-key
- Node handle
- O(1) amortized
- O(log n) amortized
