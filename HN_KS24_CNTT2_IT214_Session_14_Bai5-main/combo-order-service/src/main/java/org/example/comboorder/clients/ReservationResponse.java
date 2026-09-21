package org.example.comboorder.clients;

import java.time.Instant;

public record ReservationResponse(String reservationId, String sagaId, String resourceId,
                                  String status, Instant updatedAt) {
}

