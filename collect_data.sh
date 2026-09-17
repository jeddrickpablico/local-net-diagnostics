#!/bin/bash
# Gathers raw ping data for the lab environment

RAW_FILE="raw_output.txt"
TARGETS="targets.txt"

# BUG FIX: The script kept endlessly appending old data with '>>'.
# FIX: Used a single '>' on the first echo to wipe the file fresh on every run.
echo "Timestamp: $(date)" > "$RAW_FILE"
echo "=== PING TESTS ===" >> "$RAW_FILE"

while read -r line; do

    # Step 1: Skip the line if it is completely empty
    if [[ -z "$line" ]]; then
        continue
    fi

    # Step 2: Use regex to check if the line starts with a hashtag (comment)
    if [[ "$line" =~ ^# ]]; then
        continue
    fi

    # Step 3: Use awk to extract just the first column (the IP address)
    target=$(echo "$line" | awk '{print $1}')

    # Step 4: Ping the isolated target with a 1-second timeout
    ping -c 3 -W 1 "$target" >> "$RAW_FILE" 2>&1
    echo "---" >> "$RAW_FILE"

done < "$TARGETS"

# NEW FEATURE: Adding local port scanning
echo "=== LOCAL OPEN PORTS ===" >> "$RAW_FILE"
# -t = TCP only, -l = listening ports only, -n = numeric
ss -tln >> "$RAW_FILE"
