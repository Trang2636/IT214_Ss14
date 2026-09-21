package org.example.paymentservice.models;

import java.math.BigDecimal;

public record PaymentCommand(String sagaId, String customerId, BigDecimal amount, String scenario) {
}

