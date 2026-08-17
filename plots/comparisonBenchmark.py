"""Benchmark Fibonacci Heap against our own Binary Heap.

Both data structures are implemented in Python, so the comparison
focuses on the data structures rather than comparing our code against
Python's optimized heapq implementation.

Shared operations benchmarked:

    1. Insert
    2. Find-Min
    3. Extract-Min
"""

from __future__ import annotations

import statistics
import sys
import time
from pathlib import Path


# ============================================================
# Project root
# ============================================================

PROJECT_ROOT = Path(
    __file__
).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


from fibonacciHeap import FibonacciHeap


# ============================================================
# Binary Heap implementation
# ============================================================

class BinaryHeap:
    """A standard array-based binary min-heap.

    The heap is stored in a Python list.

    For an element at index i:

        parent = (i - 1) // 2
        leftChild = 2 * i + 1
        rightChild = 2 * i + 2
    """

    def __init__(self) -> None:
        """Create an empty Binary Heap."""
        self.heap = []

    def insert(self, key: int) -> None:
        """Insert a key.

        Complexity: O(log n)
        """
        self.heap.append(key)

        self._siftUp(
            len(self.heap) - 1
        )

    def findMin(self) -> int | None:
        """Return the minimum key without removing it.

        Complexity: O(1)
        """
        if not self.heap:
            return None

        return self.heap[0]

    def extractMin(self) -> int | None:
        """Remove and return the minimum key.

        Complexity: O(log n)
        """
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        minimumValue = self.heap[0]

        # Move the final element to the root.
        self.heap[0] = self.heap.pop()

        # Restore the heap-order property.
        self._siftDown(0)

        return minimumValue

    def isEmpty(self) -> bool:
        """Return whether the heap is empty."""
        return len(self.heap) == 0

    def getSize(self) -> int:
        """Return the number of elements."""
        return len(self.heap)

    def _siftUp(
        self,
        index: int,
    ) -> None:
        """Move a node upward until heap order is restored."""
        while index > 0:

            parentIndex = (
                index - 1
            ) // 2

            if (
                self.heap[index]
                >= self.heap[parentIndex]
            ):
                break

            (
                self.heap[index],
                self.heap[parentIndex],
            ) = (
                self.heap[parentIndex],
                self.heap[index],
            )

            index = parentIndex

    def _siftDown(
        self,
        index: int,
    ) -> None:
        """Move a node downward until heap order is restored."""
        heapSize = len(self.heap)

        while True:

            leftIndex = (
                2 * index + 1
            )

            rightIndex = (
                2 * index + 2
            )

            smallestIndex = index

            # Check left child.
            if (
                leftIndex < heapSize
                and self.heap[leftIndex]
                < self.heap[smallestIndex]
            ):
                smallestIndex = leftIndex

            # Check right child.
            if (
                rightIndex < heapSize
                and self.heap[rightIndex]
                < self.heap[smallestIndex]
            ):
                smallestIndex = rightIndex

            # Heap order is already correct.
            if smallestIndex == index:
                break

            (
                self.heap[index],
                self.heap[smallestIndex],
            ) = (
                self.heap[smallestIndex],
                self.heap[index],
            )

            index = smallestIndex


# ============================================================
# Benchmark configuration
# ============================================================

INPUT_SIZES = [
    1_000,
    5_000,
    10_000,
    50_000,
]

NUMBER_OF_TRIALS = 5

# Find-Min itself is O(1), so one call can be too fast to measure
# reliably. We perform the same fixed number of calls for both
# implementations.
FIND_MIN_REPETITIONS = 100_000


# ============================================================
# Timing helper
# ============================================================

def measureRuntime(
    benchmarkFunction,
) -> float:
    """Run a benchmark repeatedly and return median runtime."""
    runtimes = []

    for _ in range(
        NUMBER_OF_TRIALS
    ):
        startTime = time.perf_counter()

        benchmarkFunction()

        endTime = time.perf_counter()

        runtimes.append(
            endTime - startTime
        )

    return statistics.median(
        runtimes
    )


# ============================================================
# Fibonacci Heap benchmarks
# ============================================================

def benchmarkFibonacciInsert(
    inputSize: int,
) -> None:
    """Benchmark Fibonacci Heap insertion."""
    heap = FibonacciHeap()

    for value in range(inputSize):
        heap.insert(value)


def benchmarkFibonacciFindMin(
    inputSize: int,
) -> None:
    """Benchmark repeated Fibonacci Heap findMin calls."""
    heap = FibonacciHeap()

    for value in range(inputSize):
        heap.insert(value)

    for _ in range(
        FIND_MIN_REPETITIONS
    ):
        heap.findMin()


def benchmarkFibonacciExtractMin(
    inputSize: int,
) -> None:
    """Benchmark extracting every element."""
    heap = FibonacciHeap()

    for value in range(inputSize):
        heap.insert(value)

    while not heap.isEmpty():
        heap.extractMin()


# ============================================================
# Binary Heap benchmarks
# ============================================================

def benchmarkBinaryInsert(
    inputSize: int,
) -> None:
    """Benchmark Binary Heap insertion."""
    heap = BinaryHeap()

    for value in range(inputSize):
        heap.insert(value)


def benchmarkBinaryFindMin(
    inputSize: int,
) -> None:
    """Benchmark repeated Binary Heap findMin calls."""
    heap = BinaryHeap()

    for value in range(inputSize):
        heap.insert(value)

    for _ in range(
        FIND_MIN_REPETITIONS
    ):
        heap.findMin()


def benchmarkBinaryExtractMin(
    inputSize: int,
) -> None:
    """Benchmark extracting every element."""
    heap = BinaryHeap()

    for value in range(inputSize):
        heap.insert(value)

    while not heap.isEmpty():
        heap.extractMin()


# ============================================================
# Benchmark runner
# ============================================================

def runBenchmarks() -> dict:
    """Run all benchmarks and return the measured results."""

    results = {
        "insert": {
            "fibonacciHeap": [],
            "binaryHeap": [],
        },
        "findMin": {
            "fibonacciHeap": [],
            "binaryHeap": [],
        },
        "extractMin": {
            "fibonacciHeap": [],
            "binaryHeap": [],
        },
    }

    print()
    print("=" * 70)
    print("FIBONACCI HEAP vs BINARY HEAP")
    print("=" * 70)
    print(
        "Both implementations are written in Python."
    )
    print(
        f"Trials per measurement: {NUMBER_OF_TRIALS}"
    )

    # ========================================================
    # INSERT
    # ========================================================

    print()
    print("INSERT")
    print("-" * 70)

    for inputSize in INPUT_SIZES:

        fibonacciTime = measureRuntime(
            lambda: benchmarkFibonacciInsert(
                inputSize
            )
        )

        binaryTime = measureRuntime(
            lambda: benchmarkBinaryInsert(
                inputSize
            )
        )

        results["insert"][
            "fibonacciHeap"
        ].append(
            (
                inputSize,
                fibonacciTime,
            )
        )

        results["insert"][
            "binaryHeap"
        ].append(
            (
                inputSize,
                binaryTime,
            )
        )

        print(
            f"n={inputSize:<7} "
            f"Fibonacci={fibonacciTime:.8f}s   "
            f"Binary={binaryTime:.8f}s"
        )

    # ========================================================
    # FIND-MIN
    # ========================================================

    print()
    print("FIND-MIN")
    print("-" * 70)

    for inputSize in INPUT_SIZES:

        fibonacciTime = measureRuntime(
            lambda: benchmarkFibonacciFindMin(
                inputSize
            )
        )

        binaryTime = measureRuntime(
            lambda: benchmarkBinaryFindMin(
                inputSize
            )
        )

        results["findMin"][
            "fibonacciHeap"
        ].append(
            (
                inputSize,
                fibonacciTime,
            )
        )

        results["findMin"][
            "binaryHeap"
        ].append(
            (
                inputSize,
                binaryTime,
            )
        )

        print(
            f"n={inputSize:<7} "
            f"Fibonacci={fibonacciTime:.8f}s   "
            f"Binary={binaryTime:.8f}s"
        )

    # ========================================================
    # EXTRACT-MIN
    # ========================================================

    print()
    print("EXTRACT-MIN")
    print("-" * 70)

    for inputSize in INPUT_SIZES:

        fibonacciTime = measureRuntime(
            lambda: benchmarkFibonacciExtractMin(
                inputSize
            )
        )

        binaryTime = measureRuntime(
            lambda: benchmarkBinaryExtractMin(
                inputSize
            )
        )

        results["extractMin"][
            "fibonacciHeap"
        ].append(
            (
                inputSize,
                fibonacciTime,
            )
        )

        results["extractMin"][
            "binaryHeap"
        ].append(
            (
                inputSize,
                binaryTime,
            )
        )

        print(
            f"n={inputSize:<7} "
            f"Fibonacci={fibonacciTime:.8f}s   "
            f"Binary={binaryTime:.8f}s"
        )

    return results


if __name__ == "__main__":
    runBenchmarks()