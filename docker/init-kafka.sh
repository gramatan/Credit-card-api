#!/bin/bash

topics=$(kafka-topics.sh --list --bootstrap-server kafka:9092)

if ! echo "$topics" | grep -q "gran_verify"; then
    kafka-topics.sh --create --bootstrap-server kafka:9092 --topic gran_verify
fi

if ! echo "$topics" | grep -q "gran_verify_response"; then
    kafka-topics.sh --create --bootstrap-server kafka:9092 --topic gran_verify_response
fi

exit 0
