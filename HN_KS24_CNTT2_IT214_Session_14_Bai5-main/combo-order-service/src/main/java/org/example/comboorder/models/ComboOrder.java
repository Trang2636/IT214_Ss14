package org.example.comboorder.models;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

public class ComboOrder {
    private final String sagaId;
    private final String customerId;
    private final String flightId;
    private final String hotelId;
    private final BigDecimal amount;
    private final Scenario scenario;
    private final Instant createdAt;
    private final List<String> trace = new CopyOnWriteArrayList<>();
    private volatile ComboStatus status;
    private volatile String flightReservationId;
    private volatile String hotelReservationId;
    private volatile String paymentId;
    private volatile String failureReason;

    public ComboOrder(String sagaId, ComboOrderRequest request) {
        this.sagaId = sagaId;
        this.customerId = request.customerId();
        this.flightId = request.flightId();
        this.hotelId = request.hotelId();
        this.amount = request.amount();
        this.scenario = request.scenario();
        this.createdAt = Instant.now();
        this.status = ComboStatus.PENDING;
        addTrace("Khởi tạo combo PENDING");
    }

    public void transition(ComboStatus next, String message) {
        this.status = next;
        addTrace(message);
    }

    public void addTrace(String message) {
        trace.add(Instant.now() + " | " + message);
    }

    public String getSagaId() { return sagaId; }
    public String getCustomerId() { return customerId; }
    public String getFlightId() { return flightId; }
    public String getHotelId() { return hotelId; }
    public BigDecimal getAmount() { return amount; }
    public Scenario getScenario() { return scenario; }
    public Instant getCreatedAt() { return createdAt; }
    public List<String> getTrace() { return List.copyOf(trace); }
    public ComboStatus getStatus() { return status; }
    public String getFlightReservationId() { return flightReservationId; }
    public void setFlightReservationId(String value) { this.flightReservationId = value; }
    public String getHotelReservationId() { return hotelReservationId; }
    public void setHotelReservationId(String value) { this.hotelReservationId = value; }
    public String getPaymentId() { return paymentId; }
    public void setPaymentId(String value) { this.paymentId = value; }
    public String getFailureReason() { return failureReason; }
    public void setFailureReason(String value) { this.failureReason = value; }
}

