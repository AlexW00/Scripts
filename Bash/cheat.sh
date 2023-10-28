#!/bin/bash

# check if $CHEATSHEETS is set
if [ -z "$CHEATSHEETS" ]; then
    echo "Error: \$CHEATSHEETS is not set"
    exit 1
fi

nested_levels="3" # number of nested levels to search for cheatsheets
cheatsheet_file_extensions=(".txt" ".md") # filetypes of the cheatsheets

# check dependencies
dependencies="fzf"
for dependency in $dependencies; do
    if ! command -v "$dependency" >/dev/null 2>&1; then
        echo "Error: $dependency is not installed"
        exit 1
    fi
done

#exit on error
set -e

# check if the dir exists
if [ ! -d "$CHEATSHEETS" ]; then
    # exit 
    echo "Cheatsheet directory does not exist: $CHEATSHEETS"
    exit 1
fi

# creates a regex pattern to match the file extensions
buildRegex() {
    regex=""
    for ext in "${cheatsheet_file_extensions[@]}"; do
        if [ -z "$regex" ]; then
            regex="$ext"
        else
            regex="$regex|$ext"
        fi
    done
    regex="($regex)$" #only match end of string
    echo "$regex"
}

# returns all cheatsheets in the dir
getCheatsheetFiles() {
    # get all files from x nested directories
    files=$(find "$CHEATSHEETS" -maxdepth $nested_levels -type f)

    # remove all files that don't end with one of the cheatsheet file extensions regex
    files=$(echo "$files" | grep -E "$(buildRegex)")
    echo "$files"
}


# show the files using fzf, TODO: pdf/image preview?
files=$(getCheatsheetFiles)
if [ -n "$files" ]; then
    files=$(echo "$files" | fzf --pointer="*" --ansi --preview='cat {}')
    if [ -n "$files" ]; then
        $EDITOR "$files"
    fi
else
    echo "No cheatsheets found in $CHEATSHEETS"
fi
