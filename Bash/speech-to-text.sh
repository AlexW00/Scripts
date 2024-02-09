#!/bin/bash

TMP_DIR=/tmp/stt
TMP_WAV_FILE="$TMP_DIR/recording.wav"
TMP_TXT_FILE="$TMP_DIR/recording.txt"

rm -rf $TMP_DIR > /dev/null 2>&1
mkdir -p $TMP_DIR > /dev/null 2>&1

echo "Recording from microphone. Press any key to stop recording."
arecord -f "cd" --device="hw:3,0" -d 0 "$TMP_WAV_FILE" > /dev/null 2>&1 &
PID=$!

read -r -n 1 -s
kill -15 $PID

echo "Converting speech to text..."
whisper $TMP_WAV_FILE --model medium --output_format txt --output_dir "$TMP_DIR" > /dev/null 2>&1
# echo contents of the file
echo "Converted:"
CONTENT=$(cat $TMP_TXT_FILE)
echo "$CONTENT"
printf '%s' "$CONTENT" | xclip -selection clipboard
