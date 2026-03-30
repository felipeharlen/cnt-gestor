# CNT Gestor

Full-stack project to a system for tracking stock movements of insulin pens.

---

## Overview

CNT Gestor is a system designed to register and monitor incoming and outgoing
insulin pens, providing basic inventory control and traceability.
It aims to support reliable stock management in healthcare-related contexts,
with a structure prepared for future expansion.

---

## Problem Domain

Managing medical supplies goes beyond tracking stock quantities. In this
context, insulin applicator pens are distributed to individuals according
to specific eligibility rules.

Each individual may require one or two pens, and once a pen is delivered,
it remains valid for a fixed period of time (e.g., three years from the first
use). The system must therefore track deliveries, determine how many pens an
individual has already received, and identify when they become eligible to
receive new ones.

CNT Gestor is designed to support these rules by maintaining a clear and
auditable history of stock movements and deliveries, enabling both inventory
control and eligibility management.

---

## Tech Stack

**Backend**
- Python
- FastAPI

**Database**
- SQLite (initial stage)

**Frontend**
- Planned (web interface)

---

## Project Status

**Current stage:** Early development

### Implemented
- Base project structure
- FastAPI application setup
- Health check endpoint (`/health`)

### In Progress
- Database configuration
- Domain modeling for stock movements

### Planned
- Stock movement persistence
- Tracking of pen deliveries per individual
- Eligibility calculation based on delivery dates
- REST endpoints for inventory and delivery operations
- Web frontend
- Deployment

---

## Project Structure
```
cnt-gestor/
├── src/
│ ├── __init__.py
│ ├── main.py
│ │
│ ├── api/
│ │ ├── __init__.py
│ │ └── health.py
│ │
│ ├── core/
│ │ └── config.py
│ │
│ ├── db/
│ │ └── db.py
│
└── README.md
```