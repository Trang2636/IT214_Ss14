package org.example.flightservice.controllers;

import org.example.flightservice.models.BookingCommand;
import org.example.flightservice.models.Reservation;
import org.example.flightservice.services.FlightReservationService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/flights")
public class FlightController {
    private final FlightReservationService service;

    public FlightController(FlightReservationService service) {
        this.service = service;
    }

    @PostMapping("/reservations")
    public ResponseEntity<Reservation> reserve(@RequestBody BookingCommand command) {
        return ResponseEntity.ok(service.reserve(command));
    }

    @DeleteMapping("/reservations/{sagaId}")
    public ResponseEntity<Reservation> cancel(@PathVariable String sagaId) {
        return ResponseEntity.ok(service.cancel(sagaId));
    }
}

