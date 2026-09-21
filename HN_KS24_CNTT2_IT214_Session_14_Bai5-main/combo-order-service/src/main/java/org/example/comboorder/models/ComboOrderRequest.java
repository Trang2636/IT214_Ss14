package org.example.comboorder.models;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

import java.math.BigDecimal;

public record ComboOrderRequest(
        @NotBlank String customerId,
        @NotBlank String flightId,
        @NotBlank String hotelId,
        @NotNull @Positive BigDecimal amount,
        @NotNull Scenario scenario) {
}

