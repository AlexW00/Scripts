#!/bin/bash

# Get display width and height
SCREEN_WIDTH=$(xrandr | grep '*' | uniq | awk '{print $1}' | cut -d 'x' -f1)
SCREEN_HEIGHT=$(xrandr | grep '*' | uniq | awk '{print $1}' | cut -d 'x' -f2)

echo "Screen width: $SCREEN_WIDTH"
echo "Screen height: $SCREEN_HEIGHT"

# Get current workspace 
workspace=$(wmctrl -d | awk '/\*/ {print $1}')

echo "Current workspace: $workspace"

wmctrl -lG | awk -v workspace="$workspace" '$2==workspace' | while read -r id ws x y w h rest; do

  if xwininfo -id "$id" | grep -q "IsViewable"; then
    echo "WINDOW-TITLE: $rest"

    # Correct window dimensions for screenshot (exclude off-screen parts)
    [[ $x -lt 0 ]] && w=$((w+x)) && x=0 
    [[ $y -lt 0 ]] && h=$((h+y)) && y=0 
    [[ $((x+w)) -gt $SCREEN_WIDTH ]] && w=$((SCREEN_WIDTH-x))
    [[ $((y+h)) -gt $SCREEN_HEIGHT ]] && h=$((SCREEN_HEIGHT-y))

    # Calculate position and dimension relative to screen size
    x_rel=$(echo "scale=2; $x/$SCREEN_WIDTH*100" | bc)
    y_rel=$(echo "scale=2; $y/$SCREEN_HEIGHT*100" | bc)
    w_rel=$(echo "scale=2; $w/$SCREEN_WIDTH*100" | bc)
    h_rel=$(echo "scale=2; $h/$SCREEN_HEIGHT*100" | bc)

    # Print relative position and dimension
    printf 'Position: X=%s%% Y=%s%%\n' "$x_rel" "$y_rel"
    printf 'Size: Width=%s%% Height=%s%%\n' "$w_rel" "$h_rel"
    
  else
    echo "Window $id is not viewable."
  fi

  # Create a screenshot for each window (must also work with occluded windows!!) and save to ~/Pictures
  import -window "$id" ~/Pictures/Screen/"$rest".png

done