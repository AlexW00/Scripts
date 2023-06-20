#!/bin/bash

# check if $CHEATSHEETS is set

if [ -z "$CHEATSHEETS" ]; then
    echo "Error: \$CHEATSHEETS is not set"
    exit 1
fi

nested_levels="3" # number of nested levels to search for dotfiles
cheatsheet_file_extensions=(".txt" ".md")

# check if "fzf" and "git" are installed
dependencies="fzf"
for dependency in $dependencies; do
    if ! command -v "$dependency" >/dev/null 2>&1; then
        echo "Error: $dependency is not installed"
        exit 1
    fi
done

#exit on error
set -e

# check if the dotfile dir exists
if [ ! -d "$CHEATSHEETS" ]; then
    # exit 
    echo "Dot directory does not exist: $CHEATSHEETS"
    exit 1
fi

# creates a regex pattern for the dotfile extensions
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

# returns all dotfiles in the dot directory, that match the dotfile regex
getCheatsheetFiles() {
    # get all files from x nested directories
    files=$(find "$CHEATSHEETS" -maxdepth $nested_levels -type f)

    # remove all files that don't end with one of the dot file extensions regex
    files=$(echo "$files" | grep -E "$(buildRegex)")
    echo "$files"
}



# show the files using fzf
files=$(getCheatsheetFiles)
if [ -n "$files" ]; then
    files=$(echo "$files" | fzf --pointer="*" --ansi --preview="./fzf_preview.sh {}")
    if [ -n "$files" ]; then
        $EDITOR "$files"
    fi
else
    echo "No cheatsheets found in $CHEATSHEETS"
fi