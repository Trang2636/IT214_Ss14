package org.example.hotelservice.controllers;

import org.example.hotelservice.models.BookingCommand;
import org.example.hotelservice.models.Reservation;
import org.example.hotelservice.services.HotelReservationService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/hotels")
public class HotelController {
    private final HotelReservationService service;

    public HotelController(HotelReservationService service) {
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

