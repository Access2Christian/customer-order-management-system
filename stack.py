
"""
stack.py — Operational Undo Mechanism (LIFO Stack)

Module:     SEN 306 — Software Construction
Author:     Christian Chijioke Nnaji (2024/B/SENG/0246)
Purpose:    Implements a node-based Stack (Last-In-First-Out) data structure
            used to track and reverse recent order mutations, providing a
            robust undo mechanism for the Customer Order Processing System.

Design:     - No Python list shortcuts; uses linked-node chaining.
            - Single-responsibility: manages push/pop/peek only.
            - Zero cross-module imports (low coupling).
"""


class _StackNode:
    """Internal node for the stack's linked chain."""

    __slots__ = ("data", "below")

    def __init__(self, data):
        self.data = data      # payload stored at this level
        self.below = None     # reference to the node underneath


class Stack:
    """
    A linked-node LIFO stack that records every order mutation
    so the most recent action can be undone instantly.

    Public API
    ----------
    push(item)      → None          Place an item on top.
    pop()           → item | None   Remove and return the top item.
    peek()          → item | None   View the top item without removal.
    is_empty()      → bool          Check whether the stack is empty.
    size()          → int           Return the current depth.
    display()       → None          Print the stack contents top-to-bottom.
    clear()         → None          Remove all items from the stack.
    """

    def __init__(self):
        """Initialise an empty stack."""
        self._top = None     # pointer to the topmost node
        self._depth = 0      # running count of elements

    # ── core operations ──────────────────────────────────────

    def push(self, item):
        """Push *item* onto the top of the stack."""
        new_node = _StackNode(item)
        new_node.below = self._top
        self._top = new_node
        self._depth += 1

    def pop(self):
        """
        Remove and return the top item.
        Returns None if the stack is empty.
        """
        if self.is_empty():
            print("  [Stack] Nothing to undo — history is empty.")
            return None
        removed = self._top
        self._top = self._top.below
        self._depth -= 1
        return removed.data

    def peek(self):
        """
        Return the top item without removing it.
        Returns None if the stack is empty.
        """
        if self.is_empty():
            return None
        return self._top.data

    # ── utility methods ──────────────────────────────────────

    def is_empty(self):
        """Return True when no items are on the stack."""
        return self._top is None

    def size(self):
        """Return the number of items currently on the stack."""
        return self._depth

    def display(self):
        """Print every item from top to bottom."""
        if self.is_empty():
            print("  [Stack] Undo history is empty.")
            return
        print(f"  [Stack] Undo history ({self._depth} record(s)), most recent first:")
        current = self._top
        position = 1
        while current is not None:
            print(f"    {position}. {current.data}")
            current = current.below
            position += 1

    def clear(self):
        """Discard all items and reset the stack."""
        self._top = None
        self._depth = 0
        print("  [Stack] Undo history cleared.")

