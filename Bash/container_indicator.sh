#!/bin/bash

# Check if we're in a Docker container
if [ -f /.dockerenv ]; then
    echo "🐋 $hostname"
elif [ ! -z "$CONTAINER_ID" ]; then
    echo "📦️ $CONTAINER_ID"
elif [ ! -z "${container}" ]; then
    echo "📦️ ${container}"
else
    echo "λ"
fi
