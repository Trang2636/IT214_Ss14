# Bài 5 - Hệ thống đặt vé combo "Chuyến đi trọn gói"

Project mô phỏng Saga Orchestration cho giao dịch đặt **vé máy bay + phòng khách sạn + thanh toán**. Cấu trúc và công nghệ bám theo project mẫu của Session 14: Java 21, Spring Boot 4.1, Spring Cloud OpenFeign, Eureka và Gradle Wrapper.

## 1. Cấu trúc project

```text
Bai5/
├── eureka-server/          # Service discovery - port 8761
├── combo-order-service/    # Saga Orchestrator - port 8080
├── flight-service/         # REST mock đối tác vé máy bay - port 8081
├── hotel-service/          # REST mock đối tác khách sạn - port 8082
├── payment-service/        # REST mock cổng thanh toán - port 8083
├── scripts/demo.sh         # Chạy nhanh 4 kịch bản
├── demo.http               # Request mẫu cho IntelliJ/VS Code
├── HUONG_DAN_VIDEO_DEMO.md # Kịch bản quay video 5-7 phút
├── HO_SO_THIET_KE.md       # Hồ sơ thiết kế chi tiết
└── output/pdf/             # Hồ sơ thiết kế dạng PDF
```

Các service nghiệp vụ dùng bộ nhớ trong (`ConcurrentHashMap`), không cần MySQL/Kafka. Mỗi lệnh nhận `sagaId` làm idempotency key để retry/compensate an toàn.

## 2. Chạy hệ thống

Yêu cầu: JDK 21.

Mở 5 terminal, chạy theo thứ tự:

```bash
cd eureka-server && ./gradlew bootRun
cd flight-service && ./gradlew bootRun
cd hotel-service && ./gradlew bootRun
cd payment-service && ./gradlew bootRun
cd combo-order-service && ./gradlew bootRun
```

Đợi các service đăng ký với Eureka tại `http://localhost:8761`, sau đó:

```bash
chmod +x scripts/demo.sh
./scripts/demo.sh
```

Hoặc gửi từng request trong `demo.http`. API chính:

```http
POST http://localhost:8080/api/v1/combo-orders
Content-Type: application/json

{
  "customerId": "CUS-001",
  "flightId": "VN123",
  "hotelId": "HTL-001",
  "amount": 3500000,
  "scenario": "SUCCESS"
}
```

`scenario` nhận một trong bốn giá trị:

- `SUCCESS`
- `HOTEL_FAILURE`
- `PAYMENT_FAILURE`
- `HOTEL_TIMEOUT`

Tra cứu kết quả Saga: `GET /api/v1/combo-orders/{sagaId}`.

## 3. Kết quả mong đợi

| Kịch bản | Trạng thái cuối | Hành động bù |
|---|---|---|
| SUCCESS | COMPLETED | Không có |
| HOTEL_FAILURE | CANCELLED | Hủy giữ chỗ Flight; lệnh hủy Hotel idempotent |
| PAYMENT_FAILURE | CANCELLED | Hủy Hotel rồi hủy Flight |
| HOTEL_TIMEOUT | CANCELLED | Retry Hotel tối đa 3 lần, sau đó hủy Hotel và Flight |

Chi tiết kiến trúc, điểm lỗi, timeout/retry và sequence diagram nằm trong `HO_SO_THIET_KE.md` và bản PDF tương ứng.
