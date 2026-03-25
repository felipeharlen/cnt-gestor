# CNT Gestor

Full-stack system for tracking stock movements of insulin pens.

---

## Overview

CNT Gestor is a system designed to record and monitor incoming and outgoing
insulin pens, providing basic inventory control and traceability.
It aims to support reliable stock management in healthcare-related contexts,
with a structure prepared for future expansion.

---

## Problem Domain

Managing medical supplies requires accurate control of stock movements to
ensure availability, accountability, and auditability. CNT Gestor addresses
this need by registering each stock entry and exit, creating a clear history
of inventory operations.

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
- Persistent storage of stock movements
- REST endpoints for inventory operations
- Web frontend
- Deployment

---

## Project Structure
```
cnt-gestor/
├── src/
│ ├── backend/
│ ├── frontend/
│ └── docs/
└── README.md
```

---

## Development Notes

The project is being developed incrementally, starting from a minimal and
functional backend and evolving toward a complete full-stack solution. Each
development stage is versioned to reflect practical, real-world workflows.
