# Postfix Punk Parser

A Python script designed to fetch and analyze logs from Postfix, specifically identifying failed SASL authentication attempts, and providing a colorful summary of recent attack activity. This tool helps you monitor brute-force login attempts, track suspicious activity, and identify the most frequently targeted IPs and usernames.

## Features

- **Fetch Logs**: Pulls recent Postfix logs using `journalctl` and filters for SASL authentication failures.
- **Log Parsing**: Extracts relevant information such as IP addresses, usernames, and timestamps from the logs using regular expressions.
- **Data Analysis**: Computes time ranges and generates frequency counts of unique IP addresses and usernames involved in the failed attempts.
- **Colorful Output**: Provides a visually appealing, color-coded terminal output highlighting key information like total failed attempts, unique IP addresses, and most frequently used usernames.
- **Time Range Calculation**: Displays the time window of failed authentication attempts, helping you track when attacks occurred.

## Requirements

- Python 3.x
- `colorama` for colored terminal output
- `pandas` for data manipulation
- `subprocess`, `re`, `datetime`, and `collections` (standard Python libraries)

Install the required Python libraries using pip:

```bash
pip install colorama pandas
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/yourusername/postfix-punk-parser.git
cd postfix-punk-parser
```

2. Ensure that your system allows running journalctl for Postfix logs. The script assumes that you're running on a system with journalctl access (e.g., most Linux distributions).

3. Run the script:

```bash
python3 postfix_punk_parser.py
```

## Output Example

When executed, the script will display output similar to the following:

```bash
Total Failed Authentication Attempts: 150
Unique IP Addresses: 50
Unique Usernames: 45

Time Range: 
Mar 05 14:23:01 to Mar 05 15:23:01

Time Window:
(0 days, 1 hours, 0 minutes)

Top Offending IPs:
192.168.1.1: 10 attempts
192.168.1.2: 8 attempts

Top Used Usernames:
admin: 12 attempts
testuser: 8 attempts
```

## How It Works

- **Fetch Logs**: The script uses `journalctl` to pull the latest 5000 lines from Postfix logs, filtering for the term `SASL LOGIN authentication failed`.
- **Parse Logs**: The logs are parsed to extract IP addresses, usernames, and timestamps using regular expressions.
- **Analyze Data**: It calculates the time range of the log entries and generates a frequency count for IP addresses and usernames.
- **Display Results**: The results are displayed in the terminal with color-coded outputs using `colorama` to enhance readability.

## Contributing

Contributions are welcome! Please fork the repository, create a branch, and submit a pull request with your changes.

- **Bug Reports**: If you encounter any issues, please report them via GitHub Issues.
- **Feature Requests**: Have a feature in mind? Feel free to open an issue with your suggestion.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
