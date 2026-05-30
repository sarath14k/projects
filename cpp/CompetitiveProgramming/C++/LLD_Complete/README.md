# LLD Complete Guide — C++ Code Examples
*Based on the YouTube video: "How I learnt System Design to Crack Remote Job | LLD"*

---

## Folder Structure

```
LLD_Complete/
├── 1_OOPs/
│   ├── 1_Abstraction.cpp         — Pure virtual, hide internals
│   ├── 2_Encapsulation.cpp       — Private data + controlled getters/setters
│   ├── 3_Inheritance.cpp         — IS-A, multilevel inheritance
│   └── 4_Polymorphism.cpp        — Compile-time (overload, templates) + Runtime (vtable)
│
├── 2_SOLID/
│   ├── 1_SRP_SingleResponsibility.cpp  — One class, one reason to change
│   ├── 2_OCP_OpenClosed.cpp            — Extend without modifying existing code
│   ├── 3_LSP_LiskovSubstitution.cpp    — Rectangle/Square problem + fix
│   ├── 4_ISP_InterfaceSegregation.cpp  — Small focused interfaces (Robot/Human)
│   └── 5_DIP_DependencyInversion.cpp   — Depend on abstractions, inject concrete
│
├── 3_DesignPatterns/
│   ├── 1_Singleton.cpp           — One instance, global access (Logger)
│   ├── 2_Factory.cpp             — Centralized object creation (Notifications)
│   ├── 3_Observer.cpp            — 1-to-many notification (StockMarket)
│   └── 4_Strategy.cpp            — Swappable algorithms at runtime (Sorting)
│
└── 4_UML_and_Relationships/
    ├── 1_UML_Relationships.cpp        — All 6 UML relationships in C++
    ├── 2_UML_ParkingLot_CRUD.cpp      — Full LLD: UML→Code + CRUD
    └── 3_DontOvercomplicate.cpp       — KISS, DRY, YAGNI rules
```

---

## Quick Reference

### 4 Pillars of OOP

| Pillar | One Line | C++ Tool |
|---|---|---|
| Abstraction | Hide HOW, show WHAT | `virtual void foo() = 0` |
| Encapsulation | Bundle data + methods, control access | `private` + getters |
| Inheritance | Reuse parent code, IS-A relationship | `class Child : public Parent` |
| Polymorphism | One name, many forms | Overloading (compile) + `virtual` (runtime) |

### SOLID Cheat Sheet

| Letter | Principle | Rule |
|---|---|---|
| S | Single Responsibility | One class = one job |
| O | Open / Closed | Add features by adding code, not modifying |
| L | Liskov Substitution | Child must work wherever parent is used |
| I | Interface Segregation | Many small interfaces > one fat interface |
| D | Dependency Inversion | Depend on interface, inject concrete |

### UML Relationships → C++

| UML Symbol | Name | C++ Code |
|---|---|---|
| `──────▷` | Inheritance | `class Child : public Parent` |
| `- - -▷` | Realization | `class Cls : public Interface` |
| `◆────` | Composition | `unique_ptr<Part> part;` inside class |
| `◇────` | Aggregation | `Part* part;` (pointer, not owned) |
| `────→` | Association | Pointer member, created externally |
| `- - →` | Dependency | Parameter in a method |

### Design Pattern Summary

| Pattern | Type | Problem Solved |
|---|---|---|
| Singleton | Creational | Only ONE instance (Logger, DB connection) |
| Factory | Creational | Centralize object creation, hide `new` |
| Observer | Behavioral | Notify many objects when state changes |
| Strategy | Behavioral | Swap algorithm/behavior at runtime |

---

## Video's Workflow (Machine Coding Rounds)

```
1. CLARIFY requirements (10 min)
       ↓
2. DRAW UML class diagram
       ↓
3. WRITE code based on UML
       ↓
4. ANALYZE the code
       ↓
5. APPLY Design Patterns to improve it
```

## Compile Any File

```bash
g++ -std=c++17 -o out <filename>.cpp && ./out
```
