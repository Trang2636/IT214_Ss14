package org.example.hotelservice.models;

public record BookingCommand(String sagaId, String customerId, String resourceId, String scenario) {
}

