# Fibonacci Heap Project

A complete, educational Python implementation of a Fibonacci Heap with:

- Core Fibonacci Heap operations
- Circular doubly linked lists
- Consolidation after `extractMin`
- `decreaseKey` with cuts and cascading cuts
- Node handles for `decreaseKey` and `delete`
- Unit tests and randomized correctness tests
- Runtime benchmarking
- Experimental runtime plots

All project identifiers use camelCase.

## Project structure

```text
fibonacciHeapProject/
├── fibonacciHeap/
│   ├── __init__.py
│   └── fibonacciHeap.py
├── tests/
│   ├── testBasic.py
│   ├── testDecreaseKey.py
│   ├── testDelete.py
│   └── testRandomized.py
├── benchmarks/
│   └── benchmarkHeap.py
├── plots/
│   └── generatePlots.py
├── demo.py
├── requirements.txt
└── FIBONACCI_HEAP_GUIDE.md
```

## Quick start

From the project root:

```bash
python -m unittest discover -s tests -p "test*.py"
python demo.py
```

Install plotting support:

```bash
pip install -r requirements.txt
```

Benchmark:

```bash
python benchmarks/benchmarkHeap.py
```

Generate plots:

```bash
python plots/generatePlots.py
```

## Basic API

```python
from fibonacciHeap import FibonacciHeap

heap = FibonacciHeap()

node = heap.insert(10)
heap.insert(4)
heap.insert(7)

print(heap.findMin().key)

heap.decreaseKey(node, 2)
print(heap.findMin().key)

print(heap.extractMin())
```

## Important API behavior

`union(otherHeap)` is destructive. It moves all nodes from `otherHeap` into the current heap and empties `otherHeap`.

`decreaseKey(node, newKey)` requires a node handle returned by `insert()`.

`delete(node)` is implemented through the standard Fibonacci Heap reduction:

```text
decreaseKey(node, -infinity)
extractMin()
```

Therefore `delete()` is intended for numeric keys.
