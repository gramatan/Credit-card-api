#!/bin/bash

topics=$(kafka-topics.sh --list --bootstrap-server localhost:9092)

if echo "$topics" | grep -q "gran_verify_response"; then
    exit 0
else
    exit 1
fi
