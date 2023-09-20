#!/bin/bash
set -e

/opt/bitnami/scripts/kafka/entrypoint.sh /opt/bitnami/scripts/kafka/run.sh &

sleep 30

/create-topics.sh

wait $!
