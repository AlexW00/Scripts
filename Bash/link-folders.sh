#!/usr/bin/env bash
set -eu

# MAP: one “dropbox_path:local_path” per line
MAP=$(cat <<'EOF'
~/Dropbox/Pictures:~/Pictures
~/Dropbox/Documents:~/Documents
~/Dropbox/Music:~/Music
~/Dropbox/Videos:~/Movies
EOF
)

while IFS=: read -r DROP LOCAL; do
  DROP=${DROP//\~/$HOME}
  LOCAL=${LOCAL//\~/$HOME}
  [ -d "$DROP" ] || { echo "MISSING $DROP"; continue; }
  mkdir -p "$LOCAL"

  find "$DROP" -mindepth 1 -maxdepth 1 -type d -print0 |
  while IFS= read -r -d '' sub; do
    link="$LOCAL/$(basename "$sub")"
    [ -L "$link" ] && continue                     # correct symlink already there
    [ -e "$link" ] && { echo "SKIP $link"; continue; }
    echo "LINK  $link → $sub"
    ln -s "$sub" "$link"
  done
done <<< "$MAP"
