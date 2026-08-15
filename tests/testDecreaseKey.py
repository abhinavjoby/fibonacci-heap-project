import unittest
from fibonacciHeap import FibonacciHeap


class TestDecreaseKey(unittest.TestCase):
    def testDecreaseRoot(self):
        heap = FibonacciHeap()
        node = heap.insert(10)
        heap.insert(20)
        heap.decreaseKey(node, 2)
        self.assertEqual(heap.findMin().key, 2)
        heap.validate()

    def testDecreaseAndCut(self):
        heap = FibonacciHeap()
        nodes = [heap.insert(value) for value in [10, 20, 30, 40, 50, 60, 70]]
        heap.extractMin()
        heap.decreaseKey(nodes[-1], 0)
        self.assertEqual(heap.findMin().key, 0)
        heap.validate()


if __name__ == "__main__":
    unittest.main()
