# Customer Order Processing & Support Management System

> **SEN 306 — Software Construction**
> MIVA Open University | 2024/2025 Academic Session

A fully modular, real-life **Customer Order Processing and Support Management System** built in Python. The application demonstrates the practical integration of three core data structures — **Stack**, **Queue**, and **Singly Linked List** — within a unified e-commerce order management workflow.

---

## 🎯 Project Overview

This system models a real-world e-commerce pipeline where:
* **New orders** are placed into a processing queue (FIFO).
* **Processed orders** are confirmed and stored in an active orders catalog.
* **Every mutation** is tracked, enabling instant undo of the most recent action.

No Python built-in list shortcuts or arrays are used in any data structure — all three are implemented from scratch using linked-node architectures to enforce pure software construction mechanics.

---

## 🏗️ Architecture & Data Structures

| Data Structure | Module | Role in System |
| :--- | :--- | :--- |
| **Queue** (FIFO) | `queue_module.py` | **Order Processing Pipeline** — incoming checkout events are enqueued and processed in strict arrival order. |
| **Singly Linked List** | `linkedlist.py` | **Active Orders Catalog** — confirmed orders are stored, searched, updated, and deleted dynamically. |
| **Stack** (LIFO) | `stack.py` | **Undo Mechanism** — every catalog mutation is pushed onto the stack; popping reverses the most recent action. |

### System Workflow

```text
[Customer Checkout]
        │
        ▼
   ┌─────────┐     Dequeue     ┌──────────────────┐     Push     ┌───────────┐
   │  QUEUE  │ ──────────────> │  SINGLY LINKED   │ ───────────> │   STACK   │
   │Pipeline │    (confirm)    │ LIST (Catalog)   │   (track)    │  (Undo)   │
   └─────────┘                 └──────────────────┘              └───────────┘
        ▲                                │                             │
        │           New Orders           │     Search / Update /       │ Pop (undo)
        └────────────────────────────────┴───   Delete operations     ▼
                                              (reverse mutation) ◄─────┘
```

---

## 📂 Project Structure

```text
customer-order-management-system/
│
├── stack.py            # Stack (LIFO) — undo mechanism implementation
├── queue_module.py     # Queue (FIFO) — order processing pipeline implementation
├── linkedlist.py       # Singly Linked List — active orders catalog database implementation
├── main.py             # Application driver engine with full 10-option interactive menu
└── README.md           # Project documentation manual
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8 or higher (No external dependencies required)

### Installation & Usage

```bash
# Clone the repository
git clone https://github.com/Access2Christian/customer-order-management-system.git

# Navigate into the project directory
cd customer-order-management-system

# Run the application
python main.py
```

### Main Interactive Interface Options
```text
=======================================================
 CUSTOMER ORDER PROCESSING & SUPPORT SYSTEM (SEN 306) 
=======================================================
  [1]  Place a new order          (Enqueue)
  [2]  Process next order         (Dequeue -> Catalog)
  [3]  Search for an order        (Linked List lookup)
  [4]  Update order status        (Catalog mutation)
  [5]  Remove an order            (Catalog deletion)
  [6]  Undo last action           (Stack pop)
  [7]  View processing pipeline   (Queue display)
  [8]  View active orders         (Linked List display)
  [9]  View undo history          (Stack display)
  [10] System summary dashboard
  [0]  Exit
=======================================================
```

---

## 🧩 Software Construction Principles Applied

| Principle | How It's Applied |
| :--- | :--- |
| **Modular Design** | Each data structure lives in its own isolated module (`stack.py`, `queue_module.py`, `linkedlist.py`), completely separate from the execution orchestration layer (`main.py`). |
| **High Cohesion** | Every class handles exactly one structural responsibility. The Queue manages structural FIFO node pointer shifting, the Stack handles top-level LIFO states, and the Linked List routes catalog mutations. |
| **Low Coupling** | Data structure modules maintain zero cross-imports or structural interdependencies. They interact via standardized Python object types, making them highly decoupled and independently reusable. |
| **Readable Code** | Strict adherence to clean code standards: `PascalCase` for classes, `snake_case` for variables/methods, explicit docstring tracking records, and uniform formatting blocks. |
| **Input Validation** | Defensive programming via active runtime type mapping. Structural execution paths reject invalid system interactions and intercept exceptions gracefully. |

---

## 📋 Key Features
* **Zero-dependency Architecture:** Runs exclusively on native vanilla Python runtime environments without using external libraries.
* **Node-based Structural Blocks:** Data elements are managed using abstract pointer configurations without wrapping built-in array methods.
* **Dynamic Record Mutation:** Custom lambda criteria functions enable searching and dropping tracking logs safely based on any criteria.
* **State Recovery Ledger:** Transactional states can roll back destructive operations like deletion or status adjustment effortlessly.
* **Interactive CLI Terminal:** Clean administrative summary tracking queue pipelines, database storage capacities, and stack log histories live.

---

## 👤 Author
* **Name:** Christian Chijioke Nnaji
* **Registration No:** 2024/B/SENG/0246
* **Student ID:** 30037606
* **Programme:** B.Sc. Software Engineering
* **Institution:** MIVA Open University

### 📄 License
This project is submitted as coursework for **SEN 306 — Software Construction** at MIVA Open University. All rights reserved © 2025.
