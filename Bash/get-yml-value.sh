#!/bin/bash

# check if yq is installed
if ! command -v yq &> /dev/null; then
    echo "Error: yq is not installed."
    exit 1
fi

# Check if exactly two arguments are given (path to YAML file and key)
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path_to_yaml_file> <key>"
    exit 1
fi

# Assign arguments to variables
yaml_file="$1"
key="$2"

# Check if the YAML file exists
if [ ! -f "$yaml_file" ]; then
    echo "Error: File '$yaml_file' not found!"
    exit 1
fi

# Extract and print the value associated with the key
value=$(yq eval ".$key" "$yaml_file")
if [ "$value" != "null" ]; then
    echo "$value"
else
    echo "Key '$key' not found in '$yaml_file'"
fi
