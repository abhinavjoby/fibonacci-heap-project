import unittest
from fibonacciHeap import FibonacciHeap


class TestDelete(unittest.TestCase):
    def testDelete(self):
        heap = FibonacciHeap()
        nodes = {value: heap.insert(value) for value in [4, 8, 15, 16, 23, 42]}
        heap.delete(nodes[23])
        extractedValues = []
        while not heap.isEmpty():
            extractedValues.append(heap.extractMin())
        self.assertEqual(extractedValues, [4, 8, 15, 16, 42])


if __name__ == "__main__":
    unittest.main()
