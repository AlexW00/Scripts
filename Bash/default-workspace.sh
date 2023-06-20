#!/bin/sh

# Start applications
evolution
flatpak run com.discordapp.Discord
flatpak run com.spotify.Client
flatpak run com.todoist.Todoist
gnome-terminal

# Wait for applications to open
sleep 5

# Move windows to desired workspaces
wmctrl -r 'Evolution' -t 0
wmctrl -r 'Discord' -t 0
wmctrl -r 'Spotify' -t 2
wmctrl -r 'Todoist' -t 2
wmctrl -r 'Terminal' -t 2