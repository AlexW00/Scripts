#!/usr/bin/env zsh

# Get clipboard content
clipboard_content=$(xclip -o -selection clipboard)

# Construct the URL
url="https://jpdb.io/search?q=${clipboard_content}&lang=german"

# Open the URL in Firefox
firefox "$url" &!
