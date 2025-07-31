#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Search
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🔎
# @raycast.argument1 { "type": "text", "placeholder": "Query" }
# @raycast.packageName Productivity

# Documentation:
# @raycast.description Search Google or Perplexity, if the query ends in a question mark.
# @raycast.author Alex Weichart

#!/bin/bash
query="$1"
if [[ "$query" == *\? ]]; then
  open "https://www.perplexity.ai/search?q=${query%\?}"
else
  open "https://www.google.com/search?q=$query"
fi
