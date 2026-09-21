package org.example.paymentservice.models;

import java.math.BigDecimal;
import java.time.Instant;

public record Payment(String paymentId, String sagaId, BigDecimal amount,
                      String status, Instant updatedAt) {
}

