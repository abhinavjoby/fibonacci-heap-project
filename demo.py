"""Simple Fibonacci Heap demonstration."""
from fibonacciHeap import FibonacciHeap


def main() -> None:
    heap = FibonacciHeap()
    values = [10, 3, 7, 1, 20]
    print("Fibonacci Heap Demo")
    print("===================")
    print("Inserting:", values)
    for value in values:
        heap.insert(value)
    print("Minimum:", heap.findMin().key)
    print("Extracted:", heap.extractMin())
    print("New minimum:", heap.findMin().key)
    node = heap.insert(25)
    print("Inserted 25")
    heap.decreaseKey(node, 2)
    print("decreaseKey(25 -> 2), minimum:", heap.findMin().key)
    heap.delete(node)
    print("Deleted that node")
    print("Remaining values:", end=" ")
    while not heap.isEmpty():
        print(heap.extractMin(), end=" ")
    print()


if __name__ == "__main__":
    main()
