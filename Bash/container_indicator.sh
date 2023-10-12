#!/bin/bash

# Check if we're in a Docker container
if [ -f /.dockerenv ]; then
    echo "🐋 $hostname"
    exit 0
fi

if [ ! -z "$CONTAINER_ID" ]; then
    echo "📦️ $CONTAINER_ID"
    exit 0
fi

if [ ! -z "${container}" ]; then
    echo "📦️ ${container}"
    exit 0
fi

echo "λ"
exit 0
