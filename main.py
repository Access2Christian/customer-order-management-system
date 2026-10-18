
"""
main.py — Customer Order Processing & Support Management System

Module:     SEN 306 — Software Construction
Author:     Christian Chijioke Nnaji (2024/B/SENG/0246)
Student ID: 30037606
Purpose:    Interactive driver that integrates the Stack, Queue, and Singly
            Linked List modules into a unified e-commerce order management
            workflow with menu-driven operations.

Workflow
--------
  1. New checkout events are ENQUEUED into the processing pipeline (Queue).
  2. Processing DEQUEUES the next order and INSERTS it into the active
     orders catalog (Singly Linked List), while PUSHING an undo record
     onto the operations stack (Stack).
  3. Orders can be searched, updated, or removed from the catalog.
  4. The undo mechanism POPS the most recent mutation to reverse it.
"""

from queue_module import Queue            # FIFO processing pipeline
from stack import Stack                   # LIFO undo mechanism
from linkedlist import SinglyLinkedList   # active orders catalog

# ═══════════════════════════════════════════════════════════════
# GLOBAL INSTANCES — one of each data structure
# ═══════════════════════════════════════════════════════════════
order_pipeline = Queue()              # incoming orders queue
active_catalog = SinglyLinkedList()   # confirmed orders database
undo_stack = Stack()                  # mutation history for undo

# auto-incrementing order ID counter
_next_order_id = 1001


def _generate_order_id():
    """Return a unique, incrementing order identifier."""
    global _next_order_id
    oid = _next_order_id
    _next_order_id += 1
    return oid


# ═══════════════════════════════════════════════════════════════
# MENU ACTIONS
# ═══════════════════════════════════════════════════════════════

def place_new_order():
    """Capture order details from the user and enqueue them."""
    print("\n── Place New Order ──")
    customer = input("  Customer name : ").strip()
    product = input("  Product name  : ").strip()
    quantity = input("  Quantity      : ").strip()

    # basic input validation
    if not customer or not product or not quantity:
        print("  ✗ All fields are required. Order not placed.")
        return
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        print("  ✗ Quantity must be a positive whole number.")
        return

    order = {
        "order_id": _generate_order_id(),
        "customer": customer,
        "product": product,
        "quantity": quantity,
        "status": "Pending"
    }
    order_pipeline.enqueue(order)
    print(f"  ✓ Order #{order['order_id']} enqueued for {customer} "
          f"({product} x{quantity}).")


def process_next_order():
    """
    Dequeue the front order, mark it as confirmed, insert it
    into the active catalog, and push an undo record onto the stack.
    """
    print("\n── Process Next Order ──")
    order = order_pipeline.dequeue()
    if order is None:
        return  # message already printed by Queue

    order["status"] = "Confirmed"
    active_catalog.insert_at_tail(order)

    # record the mutation so it can be undone
    undo_record = {
        "action": "CONFIRM",
        "order_id": order["order_id"],
        "detail": f"Confirmed order #{order['order_id']} for "
                  f"{order['customer']} — {order['product']} x{order['quantity']}"
    }
    undo_stack.push(undo_record)
    print(f"  ✓ Order #{order['order_id']} confirmed and added to the catalog.")


def search_order():
    """Look up an order in the active catalog by its ID."""
    print("\n── Search Order ──")
    raw_id = input("  Enter Order ID to search: ").strip()
    try:
        order_id = int(raw_id)
    except ValueError:
        print("  ✗ Order ID must be a number.")
        return

    result = active_catalog.search_by_field("order_id", order_id)
    if result:
        print(f"  ✓ Found: [#{result['order_id']}] {result['customer']} — "
              f"{result['product']} x{result['quantity']} | "
              f"Status: {result['status']}")
    else:
        print(f"  ✗ No active order with ID #{order_id}.")


def update_order_status():
    """Change the status of an active order (e.g., Shipped, Delivered)."""
    print("\n── Update Order Status ──")
    raw_id = input("  Enter Order ID to update: ").strip()
    try:
        order_id = int(raw_id)
    except ValueError:
        print("  ✗ Order ID must be a number.")
        return

    record = active_catalog.search_by_field("order_id", order_id)
    if record is None:
        print(f"  ✗ No active order with ID #{order_id}.")
        return

    print(f"  Current status: {record['status']}")
    print("  Available statuses: Confirmed | Shipped | Delivered | Cancelled")
    new_status = input("  New status     : ").strip().title()

    valid_statuses = {"Confirmed", "Shipped", "Delivered", "Cancelled"}
    if new_status not in valid_statuses:
        print(f"  ✗ '{new_status}' is not a valid status.")
        return

    old_status = record["status"]
    record["status"] = new_status

    # push the mutation for undo
    undo_record = {
        "action": "STATUS_CHANGE",
        "order_id": order_id,
        "old_status": old_status,
        "new_status": new_status,
        "detail": f"Changed order #{order_id} from '{old_status}' to '{new_status}'"
    }
    undo_stack.push(undo_record)
    print(f"  ✓ Order #{order_id} status updated: {old_status} → {new_status}.")


def remove_order():
    """Delete an order from the active catalog by its ID."""
    print("\n── Remove Order ──")
    raw_id = input("  Enter Order ID to remove: ").strip()
    try:
        order_id = int(raw_id)
    except ValueError:
        print("  ✗ Order ID must be a number.")
        return

    removed = active_catalog.delete_by_field("order_id", order_id)
    if removed:
        undo_record = {
            "action": "DELETE",
            "order_id": order_id,
            "order_data": removed,
            "detail": f"Deleted order #{order_id} ({removed['customer']} — "
                      f"{removed['product']} x{removed['quantity']})"
        }
        undo_stack.push(undo_record)
        print(f"  ✓ Order #{order_id} removed from the catalog.")
    # else: message already printed by the linked list


def undo_last_action():
    """
    Pop the most recent mutation from the stack and reverse it.
    Supports undoing confirmations, status changes, and deletions.
    """
    print("\n── Undo Last Action ──")
    record = undo_stack.pop()
    if record is None:
        return  # message already printed by Stack

    action = record["action"]
    order_id = record["order_id"]

    if action == "CONFIRM":
        # reverse: remove the order from the catalog
        active_catalog.delete_by_field("order_id", order_id)
        print(f"  ↩ Undone: Order #{order_id} removed from catalog "
              f"(confirmation reversed).")

    elif action == "STATUS_CHANGE":
        # reverse: restore the previous status
        target = active_catalog.search_by_field("order_id", order_id)
        if target:
            target["status"] = record["old_status"]
            print(f"  ↩ Undone: Order #{order_id} status reverted to "
                  f"'{record['old_status']}'.")
        else:
            print(f"  ⚠ Order #{order_id} no longer in catalog; "
                  f"cannot revert status.")

    elif action == "DELETE":
        # reverse: re-insert the deleted order
        active_catalog.insert_at_tail(record["order_data"])
        print(f"  ↩ Undone: Order #{order_id} restored to the catalog.")

    else:
        print(f"  ⚠ Unknown action type '{action}'; cannot undo.")


def view_pipeline():
    """Display all orders waiting in the processing queue."""
    print("\n── Order Processing Pipeline ──")
    order_pipeline.display()


def view_catalog():
    """Display all confirmed orders in the active catalog."""
    print("\n── Active Orders Catalog ──")
    active_catalog.display()


def view_undo_history():
    """Display the stack of recorded mutations."""
    print("\n── Undo History ──")
    undo_stack.display()


def view_system_summary():
    """Print a high-level dashboard of all three data structures."""
    print("\n══════════════════════════════════════════════")
    print("          SYSTEM SUMMARY DASHBOARD")
    print("══════════════════════════════════════════════")
    print(f"  Orders in pipeline (Queue)    : {order_pipeline.size()}")
    print(f"  Active orders (Linked List)   : {active_catalog.size()}")
    print(f"  Undo records (Stack)          : {undo_stack.size()}")
    print("══════════════════════════════════════════════")


# ═══════════════════════════════════════════════════════════════
# MAIN MENU LOOP
# ═══════════════════════════════════════════════════════════════

MENU = """
╔══════════════════════════════════════════════════════════════╗
║   CUSTOMER ORDER PROCESSING & SUPPORT MANAGEMENT SYSTEM     ║
║   SEN 306 — Software Construction                           ║
║   Christian Chijioke Nnaji | 2024/B/SENG/0246               ║
╠══════════════════════════════════════════════════════════════╣
║  [1]  Place a new order          (Enqueue)                  ║
║  [2]  Process next order         (Dequeue → Catalog)        ║
║  [3]  Search for an order        (Linked List lookup)       ║
║  [4]  Update order status        (Catalog mutation)         ║
║  [5]  Remove an order            (Catalog deletion)         ║
║  [6]  Undo last action           (Stack pop)                ║
║  [7]  View processing pipeline   (Queue display)            ║
║  [8]  View active orders         (Linked List display)      ║
║  [9]  View undo history          (Stack display)            ║
║  [10] System summary dashboard                              ║
║  [0]  Exit                                                  ║
╚══════════════════════════════════════════════════════════════╝
"""

# map menu choices to handler functions
_DISPATCH = {
    "1": place_new_order,
    "2": process_next_order,
    "3": search_order,
    "4": update_order_status,
    "5": remove_order,
    "6": undo_last_action,
    "7": view_pipeline,
    "8": view_catalog,
    "9": view_undo_history,
    "10": view_system_summary,
}


def main():
    """Entry point: display the menu and dispatch user selections."""
    print("\n  Welcome to the Customer Order Processing System!")
    print("  ─────────────────────────────────────────────────")

    while True:
        print(MENU)
        choice = input("  Select an option [0-10]: ").strip()

        if choice == "0":
            print("\n  Thank you for using the Order Management System.")
            print("  Session ended. Goodbye!\n")
            break

        handler = _DISPATCH.get(choice)
        if handler:
            handler()
        else:
            print("  ✗ Invalid selection. Please choose 0–10.")


if __name__ == "__main__":
    main()

