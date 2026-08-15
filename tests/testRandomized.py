import random
import unittest
from fibonacciHeap import FibonacciHeap


class TestRandomized(unittest.TestCase):
    def testRandomInsertAndExtract(self):
        generator = random.Random(42)
        for _ in range(25):
            values = [generator.randint(-10000, 10000) for _ in range(100)]
            heap = FibonacciHeap()
            for value in values:
                heap.insert(value)
            extractedValues = [heap.extractMin() for _ in values]
            self.assertEqual(extractedValues, sorted(values))
            heap.validate()


if __name__ == "__main__":
    unittest.main()
