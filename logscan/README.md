# LogScan - Simple Log Analyzer

LogScan scans log files for specific keywords or regex patterns (e.g., ERROR, CRITICAL).

## Purpose
Quickly identify errors and failures in log files without manually opening them.

## Installation
No dependencies required. Standard library only.

## Usage
```bash
# Scan a single file for default errors (ERROR, CRITICAL, FAIL, EXCEPTION)
python logscan.py /var/log/syslog

# Scan a directory recursively
python logscan.py /var/log/nginx/

# Scan for custom patterns
python logscan.py app.log --pattern "TIMEOUT" --pattern "Connection Refused"

# JSON output
python logscan.py app.log --json
```

## Arguments
- `path`: File or directory to scan.
- `--pattern`: Custom regex pattern to search for. Can be used multiple times.
- `--limit`: Number of sample lines to display per file.
- `--json`: Output as JSON.
