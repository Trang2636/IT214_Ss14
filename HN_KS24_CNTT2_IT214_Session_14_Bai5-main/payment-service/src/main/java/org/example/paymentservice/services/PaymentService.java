package org.example.paymentservice.services;

import org.example.paymentservice.models.Payment;
import org.example.paymentservice.models.PaymentCommand;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.time.Instant;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

import static org.springframework.http.HttpStatus.PAYMENT_REQUIRED;

@Service
public class PaymentService {
    private final Map<String, Payment> payments = new ConcurrentHashMap<>();

    public Payment charge(PaymentCommand command) {
        Payment existing = payments.get(command.sagaId());
        if (existing != null) return existing;

        if ("PAYMENT_FAILURE".equals(command.scenario())) {
            throw new ResponseStatusException(PAYMENT_REQUIRED, "Thanh toán bị từ chối");
        }

        Payment created = new Payment("PAY-" + UUID.randomUUID(), command.sagaId(),
                command.amount(), "CAPTURED", Instant.now());
        payments.put(command.sagaId(), created);
        return created;
    }

    public Payment refund(String sagaId) {
        return payments.compute(sagaId, (key, current) -> {
            if (current == null) {
                return new Payment("N/A", sagaId, null, "REFUND_NOT_REQUIRED", Instant.now());
            }
            return new Payment(current.paymentId(), current.sagaId(), current.amount(),
                    "REFUNDED", Instant.now());
        });
    }
}

