package org.example.comboorder.controllers;

import jakarta.validation.Valid;
import org.example.comboorder.models.ComboOrder;
import org.example.comboorder.models.ComboOrderRequest;
import org.example.comboorder.services.ComboSagaOrchestrator;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/combo-orders")
public class ComboOrderController {
    private final ComboSagaOrchestrator orchestrator;

    public ComboOrderController(ComboSagaOrchestrator orchestrator) {
        this.orchestrator = orchestrator;
    }

    @PostMapping
    public ResponseEntity<ComboOrder> create(@Valid @RequestBody ComboOrderRequest request) {
        return ResponseEntity.ok(orchestrator.execute(request));
    }

    @GetMapping("/{sagaId}")
    public ResponseEntity<ComboOrder> get(@PathVariable String sagaId) {
        return ResponseEntity.ok(orchestrator.findById(sagaId));
    }
}

