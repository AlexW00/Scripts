#!/bin/zsh

MERGE_REQUEST_ID=$1  # The ID of the merge request

# Check if merge request ID is provided
if [ -z "$MERGE_REQUEST_ID" ]; then
    echo "Usage: $0 MERGE_REQUEST_ID"
    exit 1
fi

# Check if glab is installed
if ! command -v glab &> /dev/null; then
    echo "Error: glab is not installed."
    exit 1
fi

# Check if pbcopy is available
if ! command -v pbcopy &> /dev/null; then
    echo "Error: pbcopy is not available on this system."
    exit 1
fi

# Fetch the MR details and compare branches
function diff() {
    if ! DIFF=$(glab mr diff "$MERGE_REQUEST_ID"); then
        echo "Error: Failed to get merge request diff."
        exit 1
    fi
    echo "$DIFF"
}

MR_DIFF="$(diff)"

# Check if diff is empty
if [ -z "$MR_DIFF" ]; then
    echo "Error: No diff content to copy."
    exit 1
fi

# Save the diff content to a file
echo "Copied MR diff to clipboard"
echo "$MR_DIFF" | pbcopy
