#!/usr/bin/env bash
set -euo pipefail

API_URL="http://localhost:8080/api/v1/combo-orders"

run_scenario() {
  local scenario="$1"
  local customer="$2"
  curl --silent --show-error --request POST "$API_URL" \
    --header 'Content-Type: application/json' \
    --data "{\"customerId\":\"$customer\",\"flightId\":\"VN123\",\"hotelId\":\"HTL001\",\"amount\":3500000,\"scenario\":\"$scenario\"}"
  printf '\n\n'
}

run_scenario "SUCCESS" "CUS-001"
run_scenario "HOTEL_FAILURE" "CUS-002"
run_scenario "PAYMENT_FAILURE" "CUS-003"
run_scenario "HOTEL_TIMEOUT" "CUS-004"

