
"""
queue.py — Order Processing Pipeline (FIFO Queue)

Module:     SEN 306 — Software Construction
Author:     Christian Chijioke Nnaji (2024/B/SENG/0246)
Purpose:    Implements a node-based Queue (First-In-First-Out) data structure
            used to stage incoming customer checkout events so they are
            processed in strict arrival order — ensuring transactional fairness.

Design:     - Built on linked nodes; no Python list or deque usage.
            - Head/tail pointer management for O(1) enqueue/dequeue.
            - Self-contained module with zero external dependencies.
"""


class _QueueNode:
    """Internal node for the queue's linked chain."""

    __slots__ = ("data", "next_node")

    def __init__(self, data):
        self.data = data          # order payload
        self.next_node = None     # reference to the next node in line


class Queue:
    """
    A linked-node FIFO queue that models the order processing pipeline.
    Checkout events enter at the rear and are served from the front.

    Public API
    ----------
    enqueue(item)   → None          Add an item to the rear.
    dequeue()       → item | None   Remove and return the front item.
    front()         → item | None   View the front item without removal.
    is_empty()      → bool          Check whether the queue is empty.
    size()          → int           Return the current length.
    display()       → None          Print all queued items front-to-rear.
    clear()         → None          Remove every item from the queue.
    """

    def __init__(self):
        """Initialise an empty queue."""
        self._head = None    # front of the line (next to be served)
        self._tail = None    # rear of the line (most recently added)
        self._count = 0      # running total of enqueued items

    # ── core operations ──────────────────────────────────────

    def enqueue(self, item):
        """Add *item* to the rear of the queue."""
        new_node = _QueueNode(item)
        if self.is_empty():
            # first element becomes both head and tail
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next_node = new_node
            self._tail = new_node
        self._count += 1

    def dequeue(self):
        """
        Remove and return the item at the front of the queue.
        Returns None if the queue is empty.
        """
        if self.is_empty():
            print("  [Queue] No orders in the pipeline to process.")
            return None
        served = self._head
        self._head = self._head.next_node
        if self._head is None:
            # queue is now empty; reset tail pointer
            self._tail = None
        self._count -= 1
        return served.data

    def front(self):
        """
        Return the front item without removing it.
        Returns None if the queue is empty.
        """
        if self.is_empty():
            return None
        return self._head.data

    # ── utility methods ──────────────────────────────────────

    def is_empty(self):
        """Return True when no items are in the queue."""
        return self._head is None

    def size(self):
        """Return the number of items currently queued."""
        return self._count

    def display(self):
        """Print every queued item from front to rear."""
        if self.is_empty():
            print("  [Queue] Processing pipeline is empty.")
            return
        print(f"  [Queue] Processing pipeline ({self._count} order(s)), front first:")
        current = self._head
        position = 1
        while current is not None:
            print(f"    {position}. {current.data}")
            current = current.next_node
            position += 1

    def clear(self):
        """Discard all queued items and reset pointers."""
        self._head = None
        self._tail = None
        self._count = 0
        print("  [Queue] Processing pipeline cleared.")

