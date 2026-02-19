#!/bin/bash

LOG_FILE="$HOME/chrome_fsusage.log"

# Start monitoring Chrome with fs_usage + grep
# Pipe output into tee so it goes to both terminal and a temp log
TEMP_LOG=$(mktemp)

echo "=== Monitoring started at $(date) ===" | tee -a "$TEMP_LOG"

# Trap Ctrl+C (SIGINT) to save log on exit
trap 'echo "=== Monitoring stopped at $(date) ===" >> "$TEMP_LOG"; mv "$TEMP_LOG" "$LOG_FILE"; echo "Logs saved to $LOG_FILE"; exit 0' INT

# Run fs_usage and filter for Chrome
sudo fs_usage -w | grep "Google Chrome" | tee -a "$TEMP_LOG"