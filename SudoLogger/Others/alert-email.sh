#!/bin/bash

# Variables from sudo logger
user=$1
cmd=$2
time=$3

# ✅ STEP 1: Put your Gmail address here to receive alerts
ADMIN_EMAIL="aaryaman.g95@gmail.com"  # <-- Change this if needed

# ✅ STEP 2: Define alert message
message="[ALERT] Dangerous command detected!
User: $user
Command: $cmd
Time: $time"

# ✅ STEP 3: Send email using 'mail'
echo "$message" | mail -s "SUDO ALERT" "$ADMIN_EMAIL"

# Check if the email was sent successfully
if [[ $? -eq 0 ]]; then
    zenity --info --text="Email alert sent to $ADMIN_EMAIL"
else
    zenity --error --text="Failed to send email to $ADMIN_EMAIL"
fi

# Optional: show in terminal (for debug/logging)
echo "[ALERT] Dangerous command detected!"
echo "User: $user"
echo "Command: $cmd"
echo "Time: $time"
echo "Sending email alert to $ADMIN_EMAIL"
