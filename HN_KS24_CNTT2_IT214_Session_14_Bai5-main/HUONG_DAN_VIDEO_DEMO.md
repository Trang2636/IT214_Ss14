# Hướng dẫn quay video demo Bài 5

## Chuẩn bị

Mở 5 terminal và khởi động lần lượt:

```bash
cd eureka-server && ./gradlew bootRun
cd flight-service && ./gradlew bootRun
cd hotel-service && ./gradlew bootRun
cd payment-service && ./gradlew bootRun
cd combo-order-service && ./gradlew bootRun
```

Mở Eureka tại `http://localhost:8761` và xác nhận bốn service nghiệp vụ đã đăng ký.

## Kịch bản quay (5-7 phút)

1. Giới thiệu kiến trúc trong `HO_SO_THIET_KE.md`: Combo Order là Saga Orchestrator; Flight, Hotel và Payment là participant có dữ liệu riêng.
2. Gửi request `SUCCESS` trong `demo.http`. Chỉ ra `status=COMPLETED`, ba mã reservation/payment và trace theo đúng thứ tự.
3. Gửi `HOTEL_FAILURE`. Chỉ ra Flight đã giữ chỗ, Hotel báo lỗi, sau đó trace có `Hủy giữ phòng Hotel` và `Hủy giữ chỗ Flight`; kết quả cuối `CANCELLED`.
4. Gửi `PAYMENT_FAILURE`. Chỉ ra Flight và Hotel đều đã giữ chỗ, Payment bị từ chối, compensate chạy Hotel trước Flight; kết quả cuối `CANCELLED`.
5. Gửi `HOTEL_TIMEOUT`. Giải thích Hotel cố tình chậm 5 giây trong khi read timeout là 2 giây, retry tối đa 3 lần, rồi orchestrator gửi Hotel cancel/tombstone và Flight cancel.
6. Kết luận: hệ thống đạt eventual consistency; mọi command dùng `sagaId` để retry và compensate idempotent.

Có thể chạy bốn kịch bản liên tiếp bằng:

```bash
./scripts/demo.sh
```

Khi quay, nên đặt cửa sổ response cạnh log `combo-order-service` để thấy đồng thời state cuối và các bước tự phục hồi.

