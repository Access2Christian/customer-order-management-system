
"""
linkedlist.py — Active Orders Catalog (Singly Linked List)

Module:     SEN 306 — Software Construction
Author:     Christian Chijioke Nnaji (2024/B/SENG/0246)
Purpose:    Implements a Singly Linked List that serves as the live database
            of confirmed customer orders. Orders promoted from the processing
            queue are inserted here; completed or cancelled orders are removed
            by condition-based search.

Design:     - Pure linked-node implementation; no built-in list used internally.
            - Supports insert-at-head, insert-at-tail, search, and targeted deletion.
            - Completely self-contained; communicates via standard Python types.
"""


class _ListNode:
    """Internal node for the singly linked list."""

    __slots__ = ("data", "next_node")

    def __init__(self, data):
        self.data = data          # order record dictionary
        self.next_node = None     # reference to the following node


class SinglyLinkedList:
    """
    A singly linked list that acts as the active orders catalog.
    Each node holds an order record (dict), enabling field-level search
    and condition-based deletion.

    Public API
    ----------
    insert_at_head(item)               → None
    insert_at_tail(item)               → None
    search_by_field(field, value)      → item | None
    delete_by_field(field, value)      → item | None
    is_empty()                         → bool
    size()                             → int
    display()                          → None
    to_list()                          → list
    clear()                            → None
    """

    def __init__(self):
        """Initialise an empty linked list."""
        self._head = None    # pointer to the first node
        self._length = 0     # running count of nodes

    # ── insertion operations ─────────────────────────────────

    def insert_at_head(self, item):
        """Insert *item* at the beginning of the list."""
        new_node = _ListNode(item)
        new_node.next_node = self._head
        self._head = new_node
        self._length += 1

    def insert_at_tail(self, item):
        """Append *item* to the end of the list."""
        new_node = _ListNode(item)
        if self.is_empty():
            self._head = new_node
        else:
            current = self._head
            while current.next_node is not None:
                current = current.next_node
            current.next_node = new_node
        self._length += 1

    # ── search operation ─────────────────────────────────────

    def search_by_field(self, field, value):
        """
        Traverse the list and return the first record whose
        *field* matches *value*. Returns None if not found.
        """
        current = self._head
        while current is not None:
            if isinstance(current.data, dict) and current.data.get(field) == value:
                return current.data
            current = current.next_node
        return None

    # ── deletion operation ───────────────────────────────────

    def delete_by_field(self, field, value):
        """
        Remove the first node whose *field* matches *value*.
        Returns the removed record, or None if no match exists.
        """
        if self.is_empty():
            print("  [Catalog] No orders in the catalog.")
            return None

        # check if the head node matches
        if isinstance(self._head.data, dict) and self._head.data.get(field) == value:
            removed = self._head.data
            self._head = self._head.next_node
            self._length -= 1
            return removed

        # traverse to find the target node
        previous = self._head
        current = self._head.next_node
        while current is not None:
            if isinstance(current.data, dict) and current.data.get(field) == value:
                removed = current.data
                previous.next_node = current.next_node
                self._length -= 1
                return removed
            previous = current
            current = current.next_node

        print(f"  [Catalog] No order with {field} = '{value}' found.")
        return None

    # ── utility methods ──────────────────────────────────────

    def is_empty(self):
        """Return True when the list contains no nodes."""
        return self._head is None

    def size(self):
        """Return the number of nodes in the list."""
        return self._length

    def display(self):
        """Print every record in traversal order."""
        if self.is_empty():
            print("  [Catalog] Active orders catalog is empty.")
            return
        print(f"  [Catalog] Active orders ({self._length} record(s)):")
        current = self._head
        position = 1
        while current is not None:
            if isinstance(current.data, dict):
                order_id = current.data.get("order_id", "N/A")
                customer = current.data.get("customer", "N/A")
                product = current.data.get("product", "N/A")
                quantity = current.data.get("quantity", "N/A")
                status = current.data.get("status", "N/A")
                print(f"    {position}. [#{order_id}] {customer} — "
                      f"{product} x{quantity} | Status: {status}")
            else:
                print(f"    {position}. {current.data}")
            current = current.next_node
            position += 1

    def to_list(self):
        """Return all records as a standard Python list (for reporting)."""
        result = []
        current = self._head
        while current is not None:
            result.append(current.data)
            current = current.next_node
        return result

    def clear(self):
        """Remove all nodes and reset the list."""
        self._head = None
        self._length = 0
        print("  [Catalog] Active orders catalog cleared.")

