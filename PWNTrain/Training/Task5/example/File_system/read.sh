#!/bin/bash
# Goal: read /flag

file="$1"
# Check if the file contains "flag"
if [[ "$file" != *"flag"* ]]; then
    # Check if the file is a symlink
    if [ ! -h "$file" ]; then
        # < EXPLOITABLE WINDOW >
        cat "$file"
    else
        echo "Error: File is a symlink."
    fi
else
    echo "Error: File may not contain 'flag'."
fi