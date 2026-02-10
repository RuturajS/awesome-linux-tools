# Awesome Linux CLI Tools

A collection of safe, modular, and useful Python CLI utilities for Linux system administration and DevOps.

## Tools Included

| Tool | Purpose | Key Features |
|------|---------|--------------|
| **[syscheck](syscheck/)** | System Monitor | CPU/Mem/Disk usage, Top processes, Threshold warnings |
| **[logscan](logscan/)** | Log Analyzer | Scan logs for errors/patterns, Summary reports |
| **[fileguard](fileguard/)** | File Security | Find large files, world-writable files, checksums |
| **[netcheck](netcheck/)** | Network Dialog | Ping, Port check, Public IP |
| **[dockeraudit](dockeraudit/)** | Docker Security | Audit running containers for root/privileged mode |
| **[autoflow](autoflow/)** | Automation | Safe sequential command execution from YAML |

## Getting Started

1. **Install Requirements**:
   Each tool is standalone, but some have dependencies (check inner `requirements.txt`).
   ```bash
   pip install -r syscheck/requirements.txt
   pip install -r autoflow/requirements.txt
   ```

2. **Run a Tool**:
   ```bash
   python syscheck/syscheck.py --cpu --memory
   python logscan/logscan.py /var/log/syslog
   ```

## Philosophy
- **Safe**: Non-destructive defaults.
- **Audit**: JSON output available for all tools.
- **Simple**: Easy to read and modify Python code.

## License
MIT
