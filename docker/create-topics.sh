#!/bin/bash

while ! /opt/bitnami/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092 >/dev/null 2>&1; do
    echo "Waiting for Kafka to be ready..."
    sleep 2
done

/opt/bitnami/kafka/bin/kafka-topics.sh --create --topic gran_verify --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
/opt/bitnami/kafka/bin/kafka-topics.sh --create --topic gran_verify_response --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
