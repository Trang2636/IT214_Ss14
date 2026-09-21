package org.example.comboorder.clients;

import java.math.BigDecimal;
import java.time.Instant;

public record PaymentResponse(String paymentId, String sagaId, BigDecimal amount,
                              String status, Instant updatedAt) {
}

