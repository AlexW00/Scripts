#!/bin/bash

# Get a list of all tmux sessions
tmux_sessions=$(tmux list-sessions -F "#{session_name}")

# Loop over each session
for session in $tmux_sessions; do
    # Get the number of windows in the session
    num_windows=$(tmux list-windows -t $session | wc -l)

    # Get the number of panes in the session
    num_panes=$(tmux list-panes -s -t $session | wc -l)

    # If there's only one window and one pane (i.e., no splits)
    if [ $num_windows -eq 1 ] && [ $num_panes -eq 1 ]; then
        # Get the pane ID
        pane_id=$(tmux list-panes -t $session -F "#{pane_id}")

        # Get the number of running processes in the pane
        num_procs=$(tmux list-panes -t $session -F "#{pane_pid}" | xargs -I {} pgrep -P {} | wc -l)

        # If there are no running processes, kill the session
        if [ $num_procs -eq 0 ]; then
            tmux kill-session -t $session
        fi
    fi
done
