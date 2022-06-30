#!/bin/zsh
if [-z "$1"]; then 
    echo "No argument provided"
else
    curl "cheat.sh/$1"
fi
