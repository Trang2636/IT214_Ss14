package org.example.comboorder.clients;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@FeignClient(name = "payment-service")
public interface PaymentClient {
    @PostMapping("/api/v1/payments/charges")
    PaymentResponse charge(@RequestBody PaymentCommand command);

    @PostMapping("/api/v1/payments/refunds/{sagaId}")
    PaymentResponse refund(@PathVariable("sagaId") String sagaId);
}

