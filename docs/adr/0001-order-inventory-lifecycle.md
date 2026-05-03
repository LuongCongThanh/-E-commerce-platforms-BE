# Order Inventory Lifecycle Follows Order Status Transitions

We decide to enforce inventory changes through Order lifecycle transitions: inventory is deducted only when an `Order` moves to `CONFIRMED`, and inventory is automatically restocked when a `CONFIRMED` `Order` moves to `CANCELLED`. This keeps `PENDING` and cart activity non-committal, prevents negative inventory at confirmation time, and preserves a clear, auditable invariant that stock reflects only committed purchases.
