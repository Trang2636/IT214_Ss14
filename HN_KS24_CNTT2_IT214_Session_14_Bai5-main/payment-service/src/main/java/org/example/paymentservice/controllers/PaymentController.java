package org.example.paymentservice.controllers;

import org.example.paymentservice.models.Payment;
import org.example.paymentservice.models.PaymentCommand;
import org.example.paymentservice.services.PaymentService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/payments")
public class PaymentController {
    private final PaymentService service;

    public PaymentController(PaymentService service) {
        this.service = service;
    }

    @PostMapping("/charges")
    public ResponseEntity<Payment> charge(@RequestBody PaymentCommand command) {
        return ResponseEntity.ok(service.charge(command));
    }

    @PostMapping("/refunds/{sagaId}")
    public ResponseEntity<Payment> refund(@PathVariable String sagaId) {
        return ResponseEntity.ok(service.refund(sagaId));
    }
}

