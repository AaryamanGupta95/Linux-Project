#!/bin/bash

# Set log file path
log_file="$HOME/UserSudoLogger/logs/sudo_logger.log"

# Display a Zenity input dialog to get the command from the user
cmd=$(zenity --entry --title="Sudo Command Logger" --text="Enter a sudo command:")

# If user cancels or doesn't provide a command, exit the script
if [[ -z "$cmd" ]]; then
    zenity --error --text="No command entered. Exiting..."
    exit 1
fi

# Get current timestamp and user details
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
user=$(whoami)
cwd=$(pwd)

# Log the command to the log file with timestamp, user, command, and directory
echo "$timestamp | $user | $cmd | $cwd" >> "$log_file"

# Display confirmation that the command was logged
zenity --info --text="Command successfully logged."

# Check for dangerous commands (such as rm -rf / or useradd) and trigger an alert
if [[ "$cmd" == *"rm -rf /"* || "$cmd" == *"useradd"* || "$cmd" == *"userdel"* ]]; then
    # Trigger an email alert for dangerous commands
    bash ./alert-email.sh "$user" "$cmd" "$timestamp"

    # Show a warning in the GUI
    zenity --warning --text="[ALERT] Dangerous command detected!\nUser: $user\nCommand: $cmd\nTime: $timestamp"
