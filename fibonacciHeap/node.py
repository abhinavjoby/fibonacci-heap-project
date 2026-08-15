"""Node implementation for the Fibonacci Heap."""

from __future__ import annotations
from typing import Generic, Optional, TypeVar

KeyType = TypeVar("KeyType")


class FibonacciNode(Generic[KeyType]):
    """A node in a Fibonacci Heap."""

    def __init__(self, key: KeyType) -> None:
        self.key = key
        self.degree = 0
        self.parent: Optional["FibonacciNode[KeyType]"] = None
        self.child: Optional["FibonacciNode[KeyType]"] = None

        # Every node starts as a one-node circular doubly linked list.
        self.left: "FibonacciNode[KeyType]" = self
        self.right: "FibonacciNode[KeyType]" = self

        # A marked node has already lost one child while attached to a parent.
        self.mark = False

    def __repr__(self) -> str:
        return f"FibonacciNode(key={self.key!r}, degree={self.degree})"
