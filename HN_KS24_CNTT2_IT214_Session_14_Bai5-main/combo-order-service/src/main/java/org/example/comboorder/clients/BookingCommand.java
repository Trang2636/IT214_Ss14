package org.example.comboorder.clients;

public record BookingCommand(String sagaId, String customerId, String resourceId, String scenario) {
}

