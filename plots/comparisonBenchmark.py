from __future__ import annotations

import heapq
import statistics
import sys
import time
from pathlib import Path


# ------------------------------------------------------------
# Project root
# ------------------------------------------------------------

PROJECT_ROOT = Path(
    __file__
).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from fibonacciHeap import FibonacciHeap


# ------------------------------------------------------------
# Benchmark settings
# ------------------------------------------------------------

INPUT_SIZES = [
    1_000,
    5_000,
    10_000,
    50_000,
]

NUMBER_OF_TRIALS = 5


# ============================================================
# Helper
# ============================================================

def measureRuntime(
    benchmarkFunction,
) -> float:
    """Run a benchmark several times and return the median runtime."""

    runtimes = []

    for _ in range(NUMBER_OF_TRIALS):
        startTime = time.perf_counter()

        benchmarkFunction()

        endTime = time.perf_counter()

        runtimes.append(
            endTime - startTime
        )

    return statistics.median(runtimes)


# ============================================================
# Fibonacci Heap
# ============================================================

def fibonacciInsert(
    inputSize: int,
) -> None:
    """Insert inputSize elements into a Fibonacci Heap."""

    heap = FibonacciHeap()

    for value in range(inputSize):
        heap.insert(value)


def fibonacciFindMin(
    inputSize: int,
) -> None:
    """Perform findMin on a populated Fibonacci Heap."""

    heap = FibonacciHeap()

    for value in range(inputSize):
        heap.insert(value)

    # Perform the operation repeatedly so the timing is measurable.
    for _ in range(inputSize):
        heap.findMin()


def fibonacciExtractMin(
    inputSize: int,
) -> None:
    """Extract all elements from a Fibonacci Heap."""

    heap = FibonacciHeap()

    for value in range(inputSize):
        heap.insert(value)

    while not heap.isEmpty():
        heap.extractMin()


# ============================================================
# Python Binary Heap
# ============================================================

def binaryInsert(
    inputSize: int,
) -> None:
    """Insert inputSize elements using Python's heapq."""

    heap = []

    for value in range(inputSize):
        heapq.heappush(
            heap,
            value,
        )


def binaryFindMin(
    inputSize: int,
) -> None:
    """Perform find-min using heapq[0]."""

    heap = list(
        range(inputSize)
    )

    heapq.heapify(heap)

    for _ in range(inputSize):
        # heap[0] is the minimum element.
        _ = heap[0]


def binaryExtractMin(
    inputSize: int,
) -> None:
    """Extract all elements using heapq.heappop."""

    heap = list(
        range(inputSize)
    )

    heapq.heapify(heap)

    while heap:
        heapq.heappop(heap)


# ============================================================
# Main benchmark
# ============================================================

def runBenchmarks() -> dict:
    """Benchmark all shared operations."""

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
    print("FIBONACCI HEAP vs PYTHON BINARY HEAP")
    print("=" * 70)
    print(
        f"Trials per measurement: {NUMBER_OF_TRIALS}"
    )

    # --------------------------------------------------------
    # INSERT
    # --------------------------------------------------------

    print()
    print("INSERT")
    print("-" * 70)

    for inputSize in INPUT_SIZES:

        fibonacciTime = measureRuntime(
            lambda: fibonacciInsert(
                inputSize
            )
        )

        binaryTime = measureRuntime(
            lambda: binaryInsert(
                inputSize
            )
        )

        results["insert"]["fibonacciHeap"].append(
            (
                inputSize,
                fibonacciTime,
            )
        )

        results["insert"]["binaryHeap"].append(
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

    # --------------------------------------------------------
    # FIND-MIN
    # --------------------------------------------------------

    print()
    print("FIND-MIN")
    print("-" * 70)

    for inputSize in INPUT_SIZES:

        fibonacciTime = measureRuntime(
            lambda: fibonacciFindMin(
                inputSize
            )
        )

        binaryTime = measureRuntime(
            lambda: binaryFindMin(
                inputSize
            )
        )

        results["findMin"]["fibonacciHeap"].append(
            (
                inputSize,
                fibonacciTime,
            )
        )

        results["findMin"]["binaryHeap"].append(
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

    # --------------------------------------------------------
    # EXTRACT-MIN
    # --------------------------------------------------------

    print()
    print("EXTRACT-MIN")
    print("-" * 70)

    for inputSize in INPUT_SIZES:

        fibonacciTime = measureRuntime(
            lambda: fibonacciExtractMin(
                inputSize
            )
        )

        binaryTime = measureRuntime(
            lambda: binaryExtractMin(
                inputSize
            )
        )

        results["extractMin"]["fibonacciHeap"].append(
            (
                inputSize,
                fibonacciTime,
            )
        )

        results["extractMin"]["binaryHeap"].append(
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
