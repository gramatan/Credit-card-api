#!/bin/bash
set -e

/opt/bitnami/scripts/kafka/entrypoint.sh /opt/bitnami/scripts/kafka/run.sh &

sleep 20

/create-topics.sh

wait $!
