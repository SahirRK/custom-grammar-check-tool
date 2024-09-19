#!/bin/bash

cd "$(dirname "$0")/.." || exit

run_docker_compose() {
    docker-compose run --rm vale "$@"
}

echo "Syncing Vale packages ..."
run_docker_compose sync

echo "Running Vale ..."
run_docker_compose "$@"