package org.example.comboorder.services;

import org.example.comboorder.clients.*;
import org.example.comboorder.models.ComboOrder;
import org.example.comboorder.models.ComboOrderRequest;
import org.example.comboorder.models.ComboStatus;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class ComboSagaOrchestrator {
    private final FlightClient flightClient;
    private final HotelClient hotelClient;
    private final PaymentClient paymentClient;
    private final Map<String, ComboOrder> orders = new ConcurrentHashMap<>();

    public ComboSagaOrchestrator(FlightClient flightClient, HotelClient hotelClient,
                                 PaymentClient paymentClient) {
        this.flightClient = flightClient;
        this.hotelClient = hotelClient;
        this.paymentClient = paymentClient;
    }

    public ComboOrder execute(ComboOrderRequest request) {
        String sagaId = UUID.randomUUID().toString();
        ComboOrder order = new ComboOrder(sagaId, request);
        orders.put(sagaId, order);

        boolean flightReserved = false;
        boolean hotelReserved = false;
        boolean paymentCaptured = false;

        try {
            BookingCommand flightCommand = new BookingCommand(sagaId, request.customerId(),
                    request.flightId(), request.scenario().name());
            ReservationResponse flight = flightClient.reserve(flightCommand);
            flightReserved = true;
            order.setFlightReservationId(flight.reservationId());
            order.transition(ComboStatus.FLIGHT_RESERVED, "Flight giữ chỗ thành công: " + flight.reservationId());

            BookingCommand hotelCommand = new BookingCommand(sagaId, request.customerId(),
                    request.hotelId(), request.scenario().name());
            ReservationResponse hotel = hotelClient.reserve(hotelCommand);
            hotelReserved = true;
            order.setHotelReservationId(hotel.reservationId());
            order.transition(ComboStatus.HOTEL_RESERVED, "Hotel giữ phòng thành công: " + hotel.reservationId());

            PaymentResponse payment = paymentClient.charge(new PaymentCommand(sagaId,
                    request.customerId(), request.amount(), request.scenario().name()));
            paymentCaptured = true;
            order.setPaymentId(payment.paymentId());
            order.transition(ComboStatus.PAYMENT_COMPLETED, "Payment thu tiền thành công: " + payment.paymentId());

            order.transition(ComboStatus.COMPLETED, "Saga hoàn tất - combo được xác nhận");
            return order;
        } catch (Exception failure) {
            order.setFailureReason(rootMessage(failure));
            order.transition(ComboStatus.COMPENSATING,
                    "Saga lỗi, bắt đầu compensate theo thứ tự ngược: " + rootMessage(failure));

            boolean compensationOk = true;
            if (paymentCaptured) {
                compensationOk &= compensate(order, "Hoàn tiền Payment",
                        () -> paymentClient.refund(sagaId));
            }

            // Sau khi đã giữ Flight, luôn gửi lệnh hủy Hotel. Việc này xử lý cả trường hợp
            // timeout có kết quả không chắc chắn (Hotel có thể đã tạo booking nhưng response bị trễ).
            if (flightReserved) {
                compensationOk &= compensate(order, "Hủy giữ phòng Hotel",
                        () -> hotelClient.cancel(sagaId));
            }

            if (flightReserved) {
                compensationOk &= compensate(order, "Hủy giữ chỗ Flight",
                        () -> flightClient.cancel(sagaId));
            }

            order.transition(compensationOk ? ComboStatus.CANCELLED : ComboStatus.COMPENSATION_FAILED,
                    compensationOk ? "Compensate hoàn tất - toàn bộ combo đã hủy"
                            : "Có lệnh compensate lỗi - cần đưa vào hàng đợi retry/DLQ");
            return order;
        }
    }

    public ComboOrder findById(String sagaId) {
        ComboOrder order = orders.get(sagaId);
        if (order == null) throw new IllegalArgumentException("Không tìm thấy sagaId: " + sagaId);
        return order;
    }

    private boolean compensate(ComboOrder order, String action, Runnable command) {
        try {
            command.run();
            order.addTrace("[COMPENSATE OK] " + action);
            return true;
        } catch (Exception ex) {
            order.addTrace("[COMPENSATE FAILED] " + action + ": " + rootMessage(ex));
            return false;
        }
    }

    private String rootMessage(Throwable throwable) {
        Throwable root = throwable;
        while (root.getCause() != null) root = root.getCause();
        return root.getMessage() == null ? root.getClass().getSimpleName() : root.getMessage();
    }
}

