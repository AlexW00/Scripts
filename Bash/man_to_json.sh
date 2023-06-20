
#!/bin/bash

# Check if a manpage was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <manpage>"
    exit 1
fi

# Check if the manpage exists
if ! man -w "$1" > /dev/null 2>&1; then
    echo "Manpage $1 does not exist"
    exit 1
fi

# Convert the man page to markdown using pandoc
markdown=$(man "$1" | pandoc -f man -t markdown)

# Extract the name, synopsis, and description
name=$(echo "$markdown" | awk '/^# NAME$/,/^#/' | sed -e '1d;$d' | tr -d '\n' | sed 's/ - /: /')
synopsis=$(echo "$markdown" | awk '/^# SYNOPSIS$/,/^#/' | sed -e '1d;$d' | tr -d '\n')
description=$(echo "$markdown" | awk '/^# DESCRIPTION$/,/^#/' | sed -e '1d;$d' | tr -d '\n')

# Extract the options
options=$(echo "$markdown" | awk '/^# OPTIONS$/,/^#/' | sed -e '1d;$d' | awk '/^-/' | tr '\n' ',' | sed 's/,$//')

# Convert to JSON using jq
jq -n --arg name "$name" --arg synopsis "$synopsis" --arg description "$description" --arg options "$options" \
    '{name: $name, synopsis: $synopsis, description: $description, options: $options}'
