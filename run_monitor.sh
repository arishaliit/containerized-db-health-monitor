#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

DB_CONTAINER_NAME="db-health-monitor-db" # A unique name for the docker-compose project

echo "--- Stopping and Removing Previous Containers and Volumes (if any) ---"
# Ensure a clean slate by stopping and removing any previous containers and the volume
# This is crucial for ensuring init.sql runs on fresh database starts
docker-compose -p "$DB_CONTAINER_NAME" down -v || true # -v removes volumes, || true prevents script from exiting if nothing is running

echo "--- Starting Database and Monitor Containers ---"
# Start both services. docker-compose will handle dependencies and
# the monitor service will wait for the DB to be healthy due to 'depends_on' in docker-compose.yml.
# --build: Ensures the monitor image is built if changes are made to its Dockerfile.
# --abort-on-container-exit: Stops all containers if any container exits.
# --exit-code-from monitor: Uses the exit code of the 'monitor' service as the overall exit code.
docker-compose -p "$DB_CONTAINER_NAME" up --build --abort-on-container-exit --exit-code-from monitor

# Check the exit status of the monitor service (which is now the script's exit code)
if [ $? -eq 0 ]; then
    echo "--- Database Health Checks PASSED ---"
else
    echo "--- Database Health Checks FAILED ---"
    # Show logs of the monitor container for debugging if it failed
    docker-compose -p "$DB_CONTAINER_NAME" logs monitor
    exit 1 # Exit with error if Python script failed
fi

echo "--- Stopping and Removing Containers ---"
# Stop and remove all containers defined in docker-compose.yml for this project.
# The -v flag is already used at the beginning for a clean slate.
docker-compose -p "$DB_CONTAINER_NAME" down
