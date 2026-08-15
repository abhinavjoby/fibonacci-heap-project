from __future__ import annotations
from typing import Generator, Generic, Optional, TypeVar

from .node import FibonacciNode

KeyType = TypeVar("KeyType")


class FibonacciHeap(Generic[KeyType]):
    """A min Fibonacci Heap with standard priority-queue operations."""

    def __init__(self) -> None:
        self.minNode: Optional[FibonacciNode[KeyType]] = None
        self.nodeCount = 0

    # ---------- Circular doubly linked-list helpers ----------

    @staticmethod
    def _iterateList(startNode: Optional[FibonacciNode[KeyType]]) -> Generator[FibonacciNode[KeyType], None, None]:
        """Yield every node in a circular list exactly once."""
        if startNode is None:
            return
        currentNode = startNode
        while True:
            nextNode = currentNode.right
            yield currentNode
            if nextNode is startNode:
                break
            currentNode = nextNode

    @staticmethod
    def _insertAfter(existingNode: FibonacciNode[KeyType], newNode: FibonacciNode[KeyType]) -> None:
        """Insert newNode immediately after existingNode."""
        nextNode = existingNode.right
        newNode.left = existingNode
        newNode.right = nextNode
        existingNode.right = newNode
        nextNode.left = newNode

    @staticmethod
    def _removeFromList(node: FibonacciNode[KeyType]) -> None:
        """Detach node from its current circular doubly linked list."""
        node.left.right = node.right
        node.right.left = node.left
        node.left = node
        node.right = node

    # ---------- Root-list helpers ----------

    def _addToRootList(self, node: FibonacciNode[KeyType]) -> None:
        """Add node to the root list and update the minimum pointer."""
        node.parent = None
        node.mark = False
        if self.minNode is None:
            node.left = node
            node.right = node
            self.minNode = node
            return
        self._insertAfter(self.minNode, node)
        if node.key < self.minNode.key:
            self.minNode = node

    # ---------- Public operations ----------

    def insert(self, key: KeyType) -> FibonacciNode[KeyType]:
        """Insert a key and return its node handle. Amortized O(1)."""
        newNode = FibonacciNode(key)
        self._addToRootList(newNode)
        self.nodeCount += 1
        return newNode

    def findMin(self) -> Optional[FibonacciNode[KeyType]]:
        """Return the minimum node without removing it. O(1)."""
        return self.minNode

    def union(self, otherHeap: "FibonacciHeap[KeyType]") -> "FibonacciHeap[KeyType]":
        """Destructively meld otherHeap into this heap. Amortized O(1)."""
        if self is otherHeap:
            raise ValueError("Cannot union a heap with itself.")
        if otherHeap.minNode is None:
            return self
        if self.minNode is None:
            self.minNode = otherHeap.minNode
            self.nodeCount = otherHeap.nodeCount
            otherHeap.minNode = None
            otherHeap.nodeCount = 0
            return self

        firstMin = self.minNode
        secondMin = otherHeap.minNode
        firstRight = firstMin.right
        secondLeft = secondMin.left

        # Splice the two circular root lists together in O(1).
        firstMin.right = secondMin
        secondMin.left = firstMin
        secondLeft.right = firstRight
        firstRight.left = secondLeft

        if secondMin.key < firstMin.key:
            self.minNode = secondMin

        self.nodeCount += otherHeap.nodeCount
        otherHeap.minNode = None
        otherHeap.nodeCount = 0
        return self

    def extractMin(self) -> Optional[KeyType]:
        """Remove and return the minimum key. Amortized O(log n)."""
        minimumNode = self.minNode
        if minimumNode is None:
            return None

        # Promote every child of the minimum root into the root list.
        childNodes = list(self._iterateList(minimumNode.child))
        for childNode in childNodes:
            self._removeFromList(childNode)
            childNode.parent = None
            childNode.mark = False
            self._addToRootList(childNode)

        # Remove the minimum root itself.
        if minimumNode.right is minimumNode:
            self.minNode = None
        else:
            if self.minNode is minimumNode:
                self.minNode = minimumNode.right
            self._removeFromList(minimumNode)

        self.nodeCount -= 1

        # Isolate the removed handle.
        minimumNode.parent = None
        minimumNode.child = None
        minimumNode.degree = 0
        minimumNode.mark = False

        if self.minNode is not None:
            self._consolidate()

        return minimumNode.key

    def decreaseKey(self, node: FibonacciNode[KeyType], newKey: KeyType) -> None:
        """Decrease a node key. Amortized O(1)."""
        if newKey > node.key:
            raise ValueError("newKey cannot be greater than the current key.")

        node.key = newKey
        parentNode = node.parent

        # If heap order is broken, cut the node and move it to the roots.
        if parentNode is not None and node.key < parentNode.key:
            self._cut(node, parentNode)
            self._cascadingCut(parentNode)

        if self.minNode is None or node.key < self.minNode.key:
            self.minNode = node

    def delete(self, node: FibonacciNode[KeyType]) -> None:
        """Delete a numeric-key node using decrease-key plus extract-min."""
        self.decreaseKey(node, float("-inf"))  # type: ignore[arg-type]
        self.extractMin()

    # ---------- Consolidation ----------

    def _link(self, childNode: FibonacciNode[KeyType], parentNode: FibonacciNode[KeyType]) -> None:
        """Make childNode a child of parentNode during consolidation."""
        self._removeFromList(childNode)
        childNode.parent = parentNode
        childNode.mark = False

        if parentNode.child is None:
            parentNode.child = childNode
            childNode.left = childNode
            childNode.right = childNode
        else:
            self._insertAfter(parentNode.child, childNode)

        parentNode.degree += 1

    def _consolidate(self) -> None:
        """Combine roots of equal degree until each degree occurs once."""
        degreeTable: list[Optional[FibonacciNode[KeyType]]] = [None] * (self.nodeCount.bit_length() + 2)
        rootNodes = list(self._iterateList(self.minNode))

        for currentNode in rootNodes:
            if currentNode.parent is not None:
                continue

            while True:
                degree = currentNode.degree
                if degree >= len(degreeTable):
                    degreeTable.extend([None] * (degree - len(degreeTable) + 2))

                existingNode = degreeTable[degree]
                if existingNode is None:
                    degreeTable[degree] = currentNode
                    break

                # The smaller root becomes the parent.
                if existingNode.key < currentNode.key:
                    currentNode, existingNode = existingNode, currentNode

                self._link(existingNode, currentNode)
                degreeTable[degree] = None

        # Rebuild a clean root list from the degree table.
        self.minNode = None
        for rootNode in degreeTable:
            if rootNode is None:
                continue
            rootNode.parent = None
            rootNode.mark = False
            rootNode.left = rootNode
            rootNode.right = rootNode
            if self.minNode is None:
                self.minNode = rootNode
            else:
                self._insertAfter(self.minNode, rootNode)
                if rootNode.key < self.minNode.key:
                    self.minNode = rootNode

    # ---------- Cuts and cascading cuts ----------

    def _cut(self, node: FibonacciNode[KeyType], parentNode: FibonacciNode[KeyType]) -> None:
        """Cut a child from its parent and move it to the root list."""
        if parentNode.child is node:
            if node.right is node:
                parentNode.child = None
            else:
                parentNode.child = node.right

        self._removeFromList(node)
        parentNode.degree -= 1
        node.parent = None
        node.mark = False
        self._addToRootList(node)

    def _cascadingCut(self, node: FibonacciNode[KeyType]) -> None:
        """Perform cascading cuts toward the root."""
        parentNode = node.parent
        if parentNode is None:
            return
        if not node.mark:
            # First child loss: mark the node.
            node.mark = True
            return
        # Second child loss: cut the node and continue upward.
        self._cut(node, parentNode)
        self._cascadingCut(parentNode)

    # ---------- Utilities ----------

    def isEmpty(self) -> bool:
        """Return True when the heap has no nodes."""
        return self.nodeCount == 0

    def getSize(self) -> int:
        """Return the number of nodes in the heap."""
        return self.nodeCount

    def validate(self) -> None:
        """Assert important heap invariants. Intended for tests/debugging."""
        if self.minNode is None:
            assert self.nodeCount == 0
            return

        visitedNodes: set[int] = set()

        def validateTree(node: FibonacciNode[KeyType], expectedParent: Optional[FibonacciNode[KeyType]]) -> int:
            assert node.parent is expectedParent
            assert node.left.right is node
            assert node.right.left is node
            nodeId = id(node)
            assert nodeId not in visitedNodes
            visitedNodes.add(nodeId)

            if expectedParent is not None:
                assert expectedParent.key <= node.key

            if node.child is None:
                assert node.degree == 0
                return 1

            children = list(self._iterateList(node.child))
            assert len(children) == node.degree
            subtreeSize = 1
            for childNode in children:
                subtreeSize += validateTree(childNode, node)
            return subtreeSize

        roots = list(self._iterateList(self.minNode))
        totalNodes = sum(validateTree(rootNode, None) for rootNode in roots)
        assert self.minNode.key == min(rootNode.key for rootNode in roots)
        assert totalNodes == self.nodeCount
