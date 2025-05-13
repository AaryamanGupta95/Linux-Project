import os
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import datetime
import subprocess

# Paths to the log files
log_file_path = os.path.expanduser('~/UserSudoLogger/logs/sudo_logger.log')
log_dir = os.path.expanduser('~/UserSudoLogger/logs/')

# Ensure log directory exists
os.makedirs(log_dir, exist_ok=True)

# Function to handle command entry
def handle_command(event=None):
    cmd = entry_command.get().strip()
    entry_command.delete(0, tk.END)

    if not cmd:
        return

    # Only log if it's a sudo command
    if "sudo" not in cmd:
        return
    
    # Get current timestamp, user, and directory
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user = os.getenv('USER') or os.getenv('USERNAME') or "unknown"
    cwd = os.getcwd()
    
    # Log the command to the log file
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{timestamp} | {user} | {cmd} | {cwd}\n")
    
    # Generate daily report
    generate_daily_report()

    # Check for dangerous commands
    dangerous_commands = ["rm -rf /", "useradd", "userdel", "passwd", "chmod 777 /", "mkfs", "shutdown", "reboot"]
    if any(dangerous_cmd in cmd for dangerous_cmd in dangerous_commands):
        send_alert(user, cmd, timestamp)

# Function to send alert via alert-email.sh
def send_alert(user, cmd, timestamp):
    try:
        subprocess.run(['bash', './alert-email.sh', user, cmd, timestamp], check=True)
        messagebox.showwarning("ALERT", f"Dangerous command detected:\n{cmd}\nUser: {user}\nTime: {timestamp}")
    except Exception as e:
        messagebox.showerror("Alert Failed", f"Could not send alert:\n{e}")

# Function to generate daily report
def generate_daily_report():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    report_file_path = os.path.join(log_dir, f"daily_{today}.txt")

    try:
        with open(log_file_path, 'r') as file:
            logs = file.readlines()
        
        today_logs = [log for log in logs if today in log]
        
        with open(report_file_path, 'w') as report_file:
            report_file.writelines(today_logs)
    except Exception as e:
        messagebox.showerror("Error", f"Error generating daily report: {e}")

# Function to view all logs
def view_logs():
    try:
        with open(log_file_path, 'r') as file:
            logs = file.read()
        
        log_window = tk.Toplevel(window)
        log_window.title("View Logs")
        text_widget = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, width=80, height=20)
        text_widget.insert(tk.INSERT, logs)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(padx=10, pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open log file: {e}")

# Function to view a specific day's daily report
def view_daily_report():
    date_str = simpledialog.askstring("Select Date", "Enter the date (YYYY-MM-DD):")
    
    if not date_str:
        messagebox.showerror("Error", "No date entered.")
        return
    
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
        return

    report_file_path = os.path.join(log_dir, f"daily_{date_str}.txt")
    
    try:
        with open(report_file_path, 'r') as file:
            report = file.read()
        
        report_window = tk.Toplevel(window)
        report_window.title(f"Daily Report - {date_str}")
        text_widget = scrolledtext.ScrolledText(report_window, wrap=tk.WORD, width=80, height=20)
        text_widget.insert(tk.INSERT, report)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(padx=10, pady=10)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Daily report for {date_str} not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open daily report: {e}")

# Function to clear logs
def clear_logs():
    try:
        with open(log_file_path, 'w') as file:
            file.truncate(0)
        messagebox.showinfo("Success", "Logs cleared successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not clear logs: {e}")

# Setup GUI
window = tk.Tk()
window.title("Sudo Command Logger")
window.geometry("420x320")

label_command = tk.Label(window, text="Enter command:")
label_command.pack(pady=10)

entry_command = tk.Entry(window, width=50)
entry_command.pack(pady=5)
entry_command.bind("<Return>", handle_command)  # Automatically log on Enter key

button_view_logs = tk.Button(window, text="View Logs", command=view_logs)
button_view_logs.pack(pady=5)

button_view_reports = tk.Button(window, text="View Daily Reports", command=view_daily_report)
button_view_reports.pack(pady=5)

button_clear_logs = tk.Button(window, text="Clear Logs", command=clear_logs)
button_clear_logs.pack(pady=5)

window.mainloop()
