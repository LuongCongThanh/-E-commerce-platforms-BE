# 07. Order Lifecycle Implementation Checklist — Backend (VI)

Last updated: 2026-05-03
Source of truth: `CONTEXT.md`, `docs/adr/0001-order-inventory-lifecycle.md`, `docs/be/01-mvp-overview.vi.md`
Owner: BE Lead

## Purpose

Checklist BE-first, ngắn và theo đúng thứ tự code thật để triển khai lifecycle order MVP đã được chốt.

## Checklist

- [x] Chuẩn hóa `OrderStatus` thành `PENDING`, `CONFIRMED`, `SHIPPED`, `DELIVERED`, `CANCELLED`
- [x] Giữ `POST /api/orders/` chỉ tạo order ở `PENDING`, không trừ kho
- [x] Thêm admin action `confirm` để commit inventory tại `PENDING -> CONFIRMED`
- [x] Dùng `select_for_update()` trong `confirm` để lock variant và rollback toàn bộ khi thiếu kho
- [x] Thêm customer cancel chỉ cho `PENDING`
- [x] Thêm admin cancel cho `PENDING` hoặc `CONFIRMED`, chỉ restock khi cancel từ `CONFIRMED`
- [x] Thêm admin `ship` chỉ cho `CONFIRMED`
- [x] Thêm admin `deliver` chỉ cho `SHIPPED`
- [x] Chuẩn hóa lỗi nghiệp vụ sang `ORDER_INVALID_STATE` và `OUT_OF_STOCK`
- [x] Chuẩn hóa response error sang `{ code, message, errors }`
- [x] Bỏ customer confirm endpoint
- [x] Chuyển routing từ `/api/v1/...` sang `/api/...`
- [x] Đổi Django Admin URL sang `/secret-panel/`
- [x] Verify nhanh `create -> confirm -> ship -> deliver -> cancel` theo rule hợp lệ/không hợp lệ (`manage.py check` pass)

## Notes

- `PENDING` không giữ kho.
- Confirm fail vì thiếu tồn kho phải giữ order ở `PENDING`.
- Email `PENDING` là email “đã nhận yêu cầu đặt hàng / chờ xác nhận”.
- Email `CONFIRMED` chưa nằm trong pass đầu.
