# Master Backlog - Backend Development

This document tracks the overall progress of the backend development tasks.

## Progress Overview

| Phase  | Description                   | Status            | Priority | FE Unblocks                                |
| :----- | :---------------------------- | :---------------- | :------- | :----------------------------------------- |
| **P0** | **Foundation**                | `[ ]` Not Started | P0       | Project Structure, DB Schema               |
| **P1** | **Core API (Auth & Catalog)** | `[ ]` Not Started | P0       | Login, Registration, Product List, Details |
| **P1** | **Order API & Stock Logic**   | `[ ]` Not Started | P1       | Checkout, Cart, Order History              |
| **P2** | **Hardening & Admin**         | `[ ]` Not Started | P2       | Admin Dashboard, Image Management          |
| **P3** | **Deployment & Polish**       | `[ ]` Not Started | P3       | Production Readiness                       |

## Detailed Task List

### Phase P0: Foundation

- [ ] [P0-01] Initialize Project & Docker Environment (Ref: [06-p0-foundation.md](./06-p0-foundation.md))
- [ ] [P0-02] Core Architecture & Folder Structure (Ref: [06-p0-foundation.md](./06-p0-foundation.md))
- [ ] [P0-03] Database Schema & Base Models (Ref: [06-p0-foundation.md](./06-p0-foundation.md))
- [ ] [P0-04] CI/CD Pipeline Setup (Ref: [06-p0-foundation.md](./06-p0-foundation.md))
- [ ] [P0-05] Global Error Handling & Idempotency (Ref: [06-p0-foundation.md](./06-p0-foundation.md))

### Phase P1: Core API

- [ ] [P1-01] Authentication (JWT & Social) (Ref: [07-p1-core-api.md](./07-p1-core-api.md))
- [ ] [P1-02] Catalog API (Categories & Products) (Ref: [07-p1-core-api.md](./07-p1-core-api.md))
- [ ] [P1-03] User Profiles (Ref: [07-p1-core-api.md](./07-p1-core-api.md))
- [ ] [P1-04] Order Management API (Ref: [08-p1-order-api.md](./08-p1-order-api.md))
- [ ] [P1-05] Stock Management (Atomic Transactions) (Ref: [08-p1-order-api.md](./08-p1-order-api.md))
- [ ] [P1-06] Seed Data & Factory Setup (Ref: [10-seed-data.md](./10-seed-data.md))

### Phase P2: Hardening & Optimization

- [ ] [P2-01] Cloudinary Integration (Media) (Ref: [09-p2-hardening-admin.md](./09-p2-hardening-admin.md))
- [ ] [P2-02] Sentry & Monitoring (Ref: [09-p2-hardening-admin.md](./09-p2-hardening-admin.md))
- [ ] [P2-03] Admin Dashboard APIs (Ref: [09-p2-hardening-admin.md](./09-p2-hardening-admin.md))
- [ ] [P2-04] Security Hardening (Ref: [09-p2-hardening-admin.md](./09-p2-hardening-admin.md))

### Reference Documentation

- [01-conventions-standards.md](./01-conventions-standards.md)
- [02-api-contract.md](./02-api-contract.md)
- [03-error-handling.md](./03-error-handling.md)
- [04-permission-matrix.md](./04-permission-matrix.md)
- [05-order-lifecycle.md](./05-order-lifecycle.md)
- [10-seed-data.md](./10-seed-data.md)
- [11-api-versioning.md](./11-api-versioning.md)
