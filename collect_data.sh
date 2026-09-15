#!/bin/bash
# Gathers raw ping data for the lab environment

RAW_FILE="raw_output.txt"
TARGETS="targets.txt"

echo "Timestamp: $(date)" >> "$RAW_FILE"
echo "=== PING TESTS ===" >> "$RAW_FILE"

# NOTE: Using a standard for-loop to iterate through targets.txt. 
for ip in $(cat $TARGETS); do
    ping -c 3 "$ip" >> "$RAW_FILE" 2>&1
    echo "---" >> "$RAW_FILE"
done
