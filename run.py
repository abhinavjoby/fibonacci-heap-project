"""Run the complete project pipeline with one command."""
from __future__ import annotations
import subprocess
import sys


def runCommand(command: list[str]) -> None:
    print("\n" + "=" * 60)
    print("Running:", " ".join(command))
    print("=" * 60)
    result = subprocess.run(command)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> None:
    runCommand([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test*.py", "-v"])
    runCommand([sys.executable, "benchmarks/benchmarkHeap.py"])
    runCommand([sys.executable, "plots/generatePlots.py"])
    print("\nAll tests, benchmarks, and plots completed successfully.")


if __name__ == "__main__":
    main()
