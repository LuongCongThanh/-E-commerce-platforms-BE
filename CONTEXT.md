# E-commerce Platform

Core domain language for the backend that serves catalog browsing, account identity, and order flow.

## Language

**User**:
An authenticated account identity represented by a unique email and optional profile fields.
_Avoid_: Customer, account holder, member

**Product**:
A catalog item definition used for merchandising and description, not the sellable stock unit.
_Avoid_: SKU item, stock unit

**Category**:
A taxonomy node for catalog navigation where each node has at most one parent category.
_Avoid_: Tag, collection

**Product Variant**:
The sellable stock unit of a Product, identified by SKU and carrying price and inventory.
_Avoid_: Product, item option

**Product Image**:
An image asset attached to a Product, with at most one designated thumbnail per Product.
_Avoid_: Variant image, gallery item

**Order**:
A purchase commitment from a User at a point in time, containing line items with snapshot unit prices.
_Avoid_: Cart, checkout session

**Cart**:
A mutable pre-purchase container where a User prepares intended items before placing an Order.
_Avoid_: Order, purchase commitment

## Relationships

- A **User** can place zero or more future **Orders**
- A **User** has zero or one active **Cart**
- A **Category** can have zero or more child **Categories**
- A **Product** has one or more **Product Variants**
- A **Product** belongs to exactly one **Category**
- A **Product** can have zero or more **Product Images**
- A **Product** has at most one thumbnail **Product Image**
- A **Product Variant** belongs to exactly one **Product**
- Inventory quantity is tracked at **Product Variant** level only
- An **Order** belongs to exactly one **User**
- An **Order** contains one or more line items, each referencing one **Product Variant**
- A **Cart** can be converted into an **Order**
- An **Order** lifecycle is `PENDING` -> `CONFIRMED` -> `SHIPPED` -> `DELIVERED`, with `CANCELLED` as an alternate terminal path
- Cancellation is allowed only when an **Order** is `PENDING` or `CONFIRMED`
- Order line items store snapshot unit price and currency from the selected **Product Variant**
- A single **Order** uses one currency consistently across all its line items
- Inventory cannot go negative when converting a **Cart** to an **Order**
- Inventory is deducted when an **Order** transitions to `CONFIRMED`
- Inventory is automatically restocked when a `CONFIRMED` **Order** transitions to `CANCELLED`

## Example dialogue

> **Dev:** "Can a **User** exist before placing any order?"
> **Domain expert:** "Yes, a **User** can register and authenticate without creating an order."

> **Dev:** "Where do price and stock live?"
> **Domain expert:** "On **Product Variant**, not on **Product**."

> **Dev:** "Do we track inventory on Product or Category?"
> **Domain expert:** "No, inventory is tracked only on **Product Variant**."

> **Dev:** "Is an Order just a cart?"
> **Domain expert:** "No, **Order** is a confirmed purchase commitment with price snapshots."

> **Dev:** "Can Cart and Order be used interchangeably?"
> **Domain expert:** "No, **Cart** is editable pre-purchase; **Order** is a confirmed commitment."

## Flagged ambiguities

- "customer" and "user" were potentially interchangeable — resolved to **User** for current domain language.
