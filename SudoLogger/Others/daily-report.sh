#!/bin/bash

log_file="$HOME/UserSudoLogger/logs/sudo_logger.log"
report="$HOME/UserSudoLogger/logs/daily_$(date '+%Y-%m-%d').txt"

grep "$(date '+%Y-%m-%d')" "$log_file" > "$report"
echo "Daily report saved to $report"
