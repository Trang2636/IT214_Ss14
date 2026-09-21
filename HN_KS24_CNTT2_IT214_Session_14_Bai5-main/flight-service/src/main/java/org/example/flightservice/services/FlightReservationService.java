package org.example.flightservice.services;

import org.example.flightservice.models.BookingCommand;
import org.example.flightservice.models.Reservation;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.time.Instant;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

import static org.springframework.http.HttpStatus.CONFLICT;

@Service
public class FlightReservationService {
    private final Map<String, Reservation> reservations = new ConcurrentHashMap<>();

    public Reservation reserve(BookingCommand command) {
        Reservation existing = reservations.get(command.sagaId());
        if (existing != null) return existing;

        if ("FLIGHT_FAILURE".equals(command.scenario())) {
            throw new ResponseStatusException(CONFLICT, "Đối tác Flight từ chối giữ chỗ");
        }

        Reservation created = new Reservation(
                "FLT-" + UUID.randomUUID(), command.sagaId(), command.resourceId(),
                "RESERVED", Instant.now());
        reservations.put(command.sagaId(), created);
        return created;
    }

    public Reservation cancel(String sagaId) {
        return reservations.compute(sagaId, (key, current) -> {
            if (current == null) {
                return new Reservation("N/A", sagaId, "N/A", "CANCELLED", Instant.now());
            }
            return new Reservation(current.reservationId(), current.sagaId(), current.resourceId(),
                    "CANCELLED", Instant.now());
        });
    }
}

