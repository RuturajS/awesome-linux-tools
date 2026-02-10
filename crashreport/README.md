# CrashReport - Automated Crash Analyzer

CrashReport scans log files for signatures of system crashes, segfaults, and critical service failures, then generates a detailed text report with context.

## Purpose
Automate the "post-mortem" analysis of system logs to find out why and when services crashed.

## Installation
No dependencies required. Standard library only.

## Usage
```bash
# Scan a single log file
python crashreport.py /var/log/syslog

# Scan an entire log directory
python crashreport.py /var/log/nginx/

# Specify custom output file
python crashreport.py /var/log/syslog --output my_investigation.txt

# Add custom crash pattern (regex)
python crashreport.py app.log --pattern "CRITICAL FAILURE"
```

## Default Patterns Detected
- `segfault at`
- `Segmentation fault`
- `General Protection Fault`
- `dumped core`
- `kernel panic`
- `OOM-killer` (Out of Memory)
- `traceback`
- `uncaught exception`
