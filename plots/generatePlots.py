"""Generate nine Fibonacci Heap vs Binary Heap plots.

For each operation:

    1. Fibonacci Heap only
    2. Binary Heap only
    3. Both implementations together

Operations:

    Insert
    Find-Min
    Extract-Min
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt


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


from plots.comparisonBenchmark import runBenchmarks


# ============================================================
# Output directory
# ============================================================

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "plots"
    / "generated"
)


# ============================================================
# Helper functions
# ============================================================

def getInputSizes(
    values: list[tuple[int, float]],
) -> list[int]:
    """Extract input sizes from benchmark results."""
    return [
        item[0]
        for item in values
    ]


def getRuntimes(
    values: list[tuple[int, float]],
) -> list[float]:
    """Extract runtime values."""
    return [
        item[1]
        for item in values
    ]


def saveSinglePlot(
    inputSizes: list[int],
    runtimes: list[float],
    title: str,
    filename: str,
    label: str,
) -> None:
    """Create and save a plot for one implementation."""

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        inputSizes,
        runtimes,
        marker="o",
        label=label,
    )

    plt.xlabel(
        "Input Size (n)"
    )

    plt.ylabel(
        "Median Runtime (seconds)"
    )

    plt.title(title)

    plt.grid(
        True,
        alpha=0.3,
    )

    plt.legend()

    plt.tight_layout()

    outputFile = (
        OUTPUT_FOLDER
        / filename
    )

    plt.savefig(
        outputFile,
        dpi=200,
    )

    plt.close()

    print(
        f"Created: {filename}"
    )


def saveComparisonPlot(
    inputSizes: list[int],
    fibonacciRuntimes: list[float],
    binaryRuntimes: list[float],
    title: str,
    filename: str,
) -> None:
    """Create and save a comparison plot."""

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        inputSizes,
        fibonacciRuntimes,
        marker="o",
        label="Fibonacci Heap",
    )

    plt.plot(
        inputSizes,
        binaryRuntimes,
        marker="o",
        label="Binary Heap",
    )

    plt.xlabel(
        "Input Size (n)"
    )

    plt.ylabel(
        "Median Runtime (seconds)"
    )

    plt.title(title)

    plt.grid(
        True,
        alpha=0.3,
    )

    plt.legend()

    plt.tight_layout()

    outputFile = (
        OUTPUT_FOLDER
        / filename
    )

    plt.savefig(
        outputFile,
        dpi=200,
    )

    plt.close()

    print(
        f"Created: {filename}"
    )


# ============================================================
# Plot generation
# ============================================================

def generatePlots() -> None:
    """Run benchmarks and generate all nine plots."""

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    results = runBenchmarks()

    # ========================================================
    # INSERT
    # ========================================================

    fibonacciInsert = (
        results["insert"][
            "fibonacciHeap"
        ]
    )

    binaryInsert = (
        results["insert"][
            "binaryHeap"
        ]
    )

    inputSizes = getInputSizes(
        fibonacciInsert
    )

    fibonacciRuntimes = getRuntimes(
        fibonacciInsert
    )

    binaryRuntimes = getRuntimes(
        binaryInsert
    )

    saveSinglePlot(
        inputSizes,
        fibonacciRuntimes,
        "Fibonacci Heap - Insert",
        "01_fibonacci_insert.png",
        "Fibonacci Heap",
    )

    saveSinglePlot(
        inputSizes,
        binaryRuntimes,
        "Binary Heap - Insert",
        "02_binary_insert.png",
        "Binary Heap",
    )

    saveComparisonPlot(
        inputSizes,
        fibonacciRuntimes,
        binaryRuntimes,
        "Fibonacci Heap vs Binary Heap - Insert",
        "03_insert_comparison.png",
    )

    # ========================================================
    # FIND-MIN
    # ========================================================

    fibonacciFindMin = (
        results["findMin"][
            "fibonacciHeap"
        ]
    )

    binaryFindMin = (
        results["findMin"][
            "binaryHeap"
        ]
    )

    inputSizes = getInputSizes(
        fibonacciFindMin
    )

    fibonacciRuntimes = getRuntimes(
        fibonacciFindMin
    )

    binaryRuntimes = getRuntimes(
        binaryFindMin
    )

    saveSinglePlot(
        inputSizes,
        fibonacciRuntimes,
        "Fibonacci Heap - Find-Min",
        "04_fibonacci_findMin.png",
        "Fibonacci Heap",
    )

    saveSinglePlot(
        inputSizes,
        binaryRuntimes,
        "Binary Heap - Find-Min",
        "05_binary_findMin.png",
        "Binary Heap",
    )

    saveComparisonPlot(
        inputSizes,
        fibonacciRuntimes,
        binaryRuntimes,
        "Fibonacci Heap vs Binary Heap - Find-Min",
        "06_findMin_comparison.png",
    )

    # ========================================================
    # EXTRACT-MIN
    # ========================================================

    fibonacciExtractMin = (
        results["extractMin"][
            "fibonacciHeap"
        ]
    )

    binaryExtractMin = (
        results["extractMin"][
            "binaryHeap"
        ]
    )

    inputSizes = getInputSizes(
        fibonacciExtractMin
    )

    fibonacciRuntimes = getRuntimes(
        fibonacciExtractMin
    )

    binaryRuntimes = getRuntimes(
        binaryExtractMin
    )

    saveSinglePlot(
        inputSizes,
        fibonacciRuntimes,
        "Fibonacci Heap - Extract-Min",
        "07_fibonacci_extractMin.png",
        "Fibonacci Heap",
    )

    saveSinglePlot(
        inputSizes,
        binaryRuntimes,
        "Binary Heap - Extract-Min",
        "08_binary_extractMin.png",
        "Binary Heap",
    )

    saveComparisonPlot(
        inputSizes,
        fibonacciRuntimes,
        binaryRuntimes,
        "Fibonacci Heap vs Binary Heap - Extract-Min",
        "09_extractMin_comparison.png",
    )

    print()
    print("=" * 70)
    print("ALL 9 PLOTS GENERATED")
    print("=" * 70)

    print(
        f"Saved to: {OUTPUT_FOLDER}"
    )


if __name__ == "__main__":
    generatePlots()