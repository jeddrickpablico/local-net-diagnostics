#!/bin/bash
# Gathers raw ping data for the lab environment

RAW_FILE="raw_output.txt"
TARGETS="targets.txt"

echo "Timestamp: $(date)" >> "$RAW_FILE"
echo "=== PING TESTS ===" >> "$RAW_FILE"

# BUG FIX: The for-loop broke on comments and took too long on offline IPs.
# FIX: I am using a while read loop to process the file line by line.
while read -r line; do

    # Step 1: Skip the line if it is completely empty
    if [[ -z "$line" ]]; then
        continue
    fi

    # Step 2: Use regex to check if the line starts with a hashtag (comment)
    if [[ "$line" =~ ^# ]]; then
        continue
    fi

    # Step 3: Use awk to extract just the first column (the IP address).
    # This ensures any inline comments after the IP are ignored.
    target=$(echo "$line" | awk '{print $1}')

    # Step 4: Ping the isolated target.
    # FIX: Added -W 1 so the ping times out after 1 second per packet.
    # This stops the script from hanging indefinitely on dead targets.
    ping -c 3 -W 1 "$target" >> "$RAW_FILE" 2>&1
    echo "---" >> "$RAW_FILE"

done < "$TARGETS"
