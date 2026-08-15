import unittest
from fibonacciHeap import FibonacciHeap


class TestBasic(unittest.TestCase):
    def testInsertAndFindMin(self):
        heap = FibonacciHeap()
        for value in [10, 3, 7, 1]:
            heap.insert(value)
        self.assertEqual(heap.findMin().key, 1)
        self.assertEqual(heap.getSize(), 4)
        heap.validate()

    def testExtractMinSortedOrder(self):
        heap = FibonacciHeap()
        values = [7, 3, 17, 24, 10, 1, 5]
        for value in values:
            heap.insert(value)
        extractedValues = []
        while not heap.isEmpty():
            extractedValues.append(heap.extractMin())
        self.assertEqual(extractedValues, sorted(values))

    def testUnion(self):
        firstHeap = FibonacciHeap()
        secondHeap = FibonacciHeap()
        for value in [10, 4, 18]:
            firstHeap.insert(value)
        for value in [7, 2, 15]:
            secondHeap.insert(value)
        firstHeap.union(secondHeap)
        self.assertEqual(firstHeap.getSize(), 6)
        self.assertTrue(secondHeap.isEmpty())
        self.assertEqual(firstHeap.findMin().key, 2)
        extractedValues = []
        while not firstHeap.isEmpty():
            extractedValues.append(firstHeap.extractMin())
        self.assertEqual(extractedValues, [2, 4, 7, 10, 15, 18])


if __name__ == "__main__":
    unittest.main()
