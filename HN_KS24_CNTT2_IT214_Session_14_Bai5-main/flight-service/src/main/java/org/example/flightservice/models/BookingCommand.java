package org.example.flightservice.models;

public record BookingCommand(String sagaId, String customerId, String resourceId, String scenario) {
}

