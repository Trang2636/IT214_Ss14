package org.example.hotelservice.services;

import org.example.hotelservice.models.BookingCommand;
import org.example.hotelservice.models.Reservation;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.time.Instant;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

import static org.springframework.http.HttpStatus.CONFLICT;

@Service
public class HotelReservationService {
    private final Map<String, Reservation> reservations = new ConcurrentHashMap<>();
    private final Set<String> cancelledSagas = ConcurrentHashMap.newKeySet();

    public Reservation reserve(BookingCommand command) {
        Reservation existing = reservations.get(command.sagaId());
        if (existing != null) return existing;

        if ("HOTEL_FAILURE".equals(command.scenario())) {
            throw new ResponseStatusException(CONFLICT, "Đối tác Hotel hết phòng");
        }

        if ("HOTEL_TIMEOUT".equals(command.scenario())) {
            try {
                Thread.sleep(5_000);
            } catch (InterruptedException ex) {
                Thread.currentThread().interrupt();
                throw new IllegalStateException("Hotel request bị gián đoạn", ex);
            }
        }

        // Có thể lệnh cancel đã tới trong lúc request cũ còn đang xử lý.
        if (cancelledSagas.contains(command.sagaId())) {
            return new Reservation("N/A", command.sagaId(), command.resourceId(),
                    "CANCELLED", Instant.now());
        }

        Reservation created = new Reservation(
                "HTL-" + UUID.randomUUID(), command.sagaId(), command.resourceId(),
                "RESERVED", Instant.now());
        reservations.put(command.sagaId(), created);
        return created;
    }

    public Reservation cancel(String sagaId) {
        cancelledSagas.add(sagaId);
        return reservations.compute(sagaId, (key, current) -> {
            if (current == null) {
                return new Reservation("N/A", sagaId, "N/A", "CANCELLED", Instant.now());
            }
            return new Reservation(current.reservationId(), current.sagaId(), current.resourceId(),
                    "CANCELLED", Instant.now());
        });
    }
}

