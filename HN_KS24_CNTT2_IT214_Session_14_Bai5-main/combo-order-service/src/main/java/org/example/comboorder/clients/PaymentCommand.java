package org.example.comboorder.clients;

import java.math.BigDecimal;

public record PaymentCommand(String sagaId, String customerId, BigDecimal amount, String scenario) {
}

