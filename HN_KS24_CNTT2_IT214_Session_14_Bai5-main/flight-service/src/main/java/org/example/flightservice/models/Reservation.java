package org.example.flightservice.models;

import java.time.Instant;

public record Reservation(String reservationId, String sagaId, String resourceId,
                          String status, Instant updatedAt) {
}

