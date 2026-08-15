from __future__ import annotations
import csv
import random
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fibonacciHeap import FibonacciHeap

INPUT_SIZES = [1_000, 5_000, 10_000, 50_000, 100_000]
OUTPUT_FILE = Path(__file__).resolve().parent / "benchmarkResults.csv"


def benchmarkInsert(inputSize: int) -> float:
    heap = FibonacciHeap()
    startTime = time.perf_counter()
    for value in range(inputSize):
        heap.insert(value)
    return time.perf_counter() - startTime


def benchmarkExtractMin(inputSize: int) -> float:
    heap = FibonacciHeap()
    for value in range(inputSize):
        heap.insert(value)
    startTime = time.perf_counter()
    while not heap.isEmpty():
        heap.extractMin()
    return time.perf_counter() - startTime


def benchmarkDecreaseKey(inputSize: int) -> float:
    generator = random.Random(42)
    heap = FibonacciHeap()
    nodes = [heap.insert(generator.randint(1, 1_000_000_000)) for _ in range(inputSize)]
    startTime = time.perf_counter()
    for index, node in enumerate(nodes):
        heap.decreaseKey(node, node.key - index - 1)
    return time.perf_counter() - startTime


def main() -> None:
    rows = []
    print("Running Fibonacci Heap benchmarks...\n")

    for inputSize in INPUT_SIZES:
        runtime = benchmarkInsert(inputSize)
        rows.append({"inputSize": inputSize, "operation": "insert", "runtimeSeconds": runtime})
        print(f"insert       n={inputSize:<7} {runtime:.6f}s")

    for inputSize in INPUT_SIZES:
        runtime = benchmarkExtractMin(inputSize)
        rows.append({"inputSize": inputSize, "operation": "extractMin", "runtimeSeconds": runtime})
        print(f"extractMin   n={inputSize:<7} {runtime:.6f}s")

    for inputSize in [1_000, 5_000, 10_000, 50_000]:
        runtime = benchmarkDecreaseKey(inputSize)
        rows.append({"inputSize": inputSize, "operation": "decreaseKey", "runtimeSeconds": runtime})
        print(f"decreaseKey  n={inputSize:<7} {runtime:.6f}s")

    with OUTPUT_FILE.open("w", newline="") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=["inputSize", "operation", "runtimeSeconds"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
