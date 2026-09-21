package org.example.comboorder.clients;

import feign.Request;
import feign.Retryer;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.context.annotation.Bean;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.time.Duration;

@FeignClient(name = "hotel-service", configuration = HotelClient.HotelFeignConfiguration.class)
public interface HotelClient {
    @PostMapping("/api/v1/hotels/reservations")
    ReservationResponse reserve(@RequestBody BookingCommand command);

    @DeleteMapping("/api/v1/hotels/reservations/{sagaId}")
    ReservationResponse cancel(@PathVariable("sagaId") String sagaId);

    class HotelFeignConfiguration {
        @Bean
        Request.Options hotelRequestOptions() {
            return new Request.Options(Duration.ofSeconds(1), Duration.ofSeconds(2), true);
        }

        @Bean
        Retryer hotelRetryer() {
            return new Retryer.Default(200, 1_000, 3);
        }
    }
}

