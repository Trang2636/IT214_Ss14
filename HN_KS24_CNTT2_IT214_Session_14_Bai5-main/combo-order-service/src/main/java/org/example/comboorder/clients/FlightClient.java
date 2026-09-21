package org.example.comboorder.clients;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@FeignClient(name = "flight-service")
public interface FlightClient {
    @PostMapping("/api/v1/flights/reservations")
    ReservationResponse reserve(@RequestBody BookingCommand command);

    @DeleteMapping("/api/v1/flights/reservations/{sagaId}")
    ReservationResponse cancel(@PathVariable("sagaId") String sagaId);
}

