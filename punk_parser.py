#!/usr/bin/env python3
import subprocess as sp
import re
from datetime import datetime
from collections import Counter
import pandas as pd
from colorama import Fore, Style

def fetch_logs():
    """Fetch logs from journalctl and filter for SASL failures"""
    flcmd = "journalctl -u postfix -n 5000 --no-pager | grep 'SASL LOGIN authentication failed'"
    flresult = sp.run(flcmd, shell=True, capture_output=True, text=True)
    return flresult.stdout.splitlines()

def parse_logs(logs):
    """Using regular express, (RE) parse the logs and extract IPs, usernames, and timestamps"""
    ip_pattern = re.compile(r"unknown\[(\d+\.\d+\.\d+\.\d+)\]")
    user_pattern = re.compile(r"sasl_username=([\w\.\@]+)")
    time_pattern = re.compile(r"(\w{3} \d{1,2} \d{2}:\d{2}:\d{2})")

    ips = []
    usernames = []
    timestamps = []

    for log in logs:
        ip_match = ip_pattern.search(log)
        user_match = user_pattern.search(log)
        time_match = time_pattern.search(log)

        if ip_match:
            ips.append(ip_match.group(1))
        if user_match:
            usernames.append(user_match.group(1))
        if time_match:
            timestamps.append(time_match.group(1))

    return ips, usernames, timestamps

def calculate_time_range(timestamps):
    """ Calculate the time range (earliest to latest) of log entries. """
    current_year = datetime.now().year
    # Convert timestamp strings to datetime objects
    time_format = "%b %d %H:%M:%S"  # Example: Mar 05 14:23:01
    times = [datetime.strptime(f"{current_year} {ts}", f"%Y {time_format}") for ts in timestamps]

    # Find the earliest and latest timestamps
    earliest_time = min(times)
    latest_time = max(times)

    # Calculate the difference between the times
    time_diff = latest_time - earliest_time
    days = time_diff.days
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    # Summary of time range
    time_range = f"Time Range: \n{earliest_time} to {latest_time}"
    time_window =f"Time Window:\n({days} days, {hours} hours, {minutes} minutes)"
    return time_range, time_window

def create_dataframes(ips, usernames):
    """ Convert IPs and usernames to pandas DataFrames. """
    ip_counts = Counter(ips)
    user_counts = Counter(usernames)

    df_ips = pd.DataFrame(ip_counts.items(), columns=["IP Address", "Attempts"])
    df_ips = df_ips.sort_values(by="Attempts", ascending=False)

    df_users = pd.DataFrame(user_counts.items(), columns=["Username", "Attempts"])
    df_users = df_users.sort_values(by="Attempts", ascending=False)

    return df_ips, df_users

def display_results(ips, usernames, time_range, time_window):
    """ Display the analysis results in a structured format. """
    unique_ips = Counter(ips)
    unique_users = Counter(usernames)

    print(f"{Fore.CYAN}Total Failed Authentication Attempts:{Style.RESET_ALL} {len(ips)}")
    print(f"{Fore.GREEN}Unique IP Addresses:{Style.RESET_ALL} {len(unique_ips)}")
    print(f"{Fore.YELLOW}Unique Usernames:{Style.RESET_ALL} {len(unique_users)}\n")
    print(f"{Fore.MAGENTA}{time_range}{Style.RESET_ALL}\n")
    print(f"{Fore.WHITE}{time_window}{Style.RESET_ALL}\n")

    print(f"{Fore.MAGENTA}Top Offending IPs:{Style.RESET_ALL}")
    for ip, count in unique_ips.most_common(10):
        print(f"{Fore.RED}{ip}{Style.RESET_ALL}: {count} attempts")

    print(f"\n{Fore.BLUE}Top Used Usernames:{Style.RESET_ALL}")
    for user, count in unique_users.most_common(10):
        print(f"{Fore.LIGHTBLUE_EX}{user}{Style.RESET_ALL}: {count} attempts")


def main():
    """ Main functions """
    logs = fetch_logs()
    ips, usernames, timestamps = parse_logs(logs)

    # Calculate the time range for the log entries
    time_range, time_window = calculate_time_range(timestamps)

    df_ips, df_users = create_dataframes(ips, usernames)

    display_results(ips, usernames, time_range, time_window)

# Directly call main
main()
