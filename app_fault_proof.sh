#!/bin/bash

while true; do
    ./app.sh
    exit_code=$?
    echo "Fault occurred. Restarting script..."
done