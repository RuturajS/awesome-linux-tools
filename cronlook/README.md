# CronLook - Cron Job Visualizer

CronLook lists active cron jobs for the current user and system-wide configurations.

## Purpose
Quickly view all scheduled tasks in a readable format.

## Installation
No dependencies required. Standard library only.

## Usage
```bash
# List current user's cron jobs
python cronlook.py

# List system-wide cron jobs (requires read access to /etc/crontab)
python cronlook.py --system
```
