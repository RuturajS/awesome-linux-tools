# Awesome Linux CLI Tools

A collection of safe, modular, and useful Python CLI utilities for Linux system administration and DevOps.

## 🚀 Central Runner & History
Use `runner.py` to execute tools and automatically save a history of your commands.
```bash
# Run a tool
python runner.py syscheck --cpu

# View Command History
python runner.py --history
```

## Tools Included

| Tool | Purpose | Key Features |
|------|---------|--------------|
| **[syscheck](syscheck/)** | System Monitor | CPU/Mem/Disk usage, Top processes, Threshold warnings |
| **[servicelook](servicelook/)** | Service Viewer | Color-coded `systemctl` list, find failed services |
| **[pkgcheck](pkgcheck/)** | Package Audit | List manually installed apt/dnf packages |
| **[logscan](logscan/)** | Log Analyzer | Scan logs for errors/patterns, Summary reports |
| **[fileguard](fileguard/)** | File Security | Find large files, world-writable files, checksums |
| **[netcheck](netcheck/)** | Network Dialog | Ping, Port check, Public IP |
| **[portaudit](portaudit/)** | Port Visualizer | List open ports, identify services, color output |
| **[dockeraudit](dockeraudit/)** | Docker Security | Audit running containers for root/privileged mode |
| **[crashreport](crashreport/)** | Crash Forensic | Scan logs for segfaults/panics, generate incident report |
| **[autoflow](autoflow/)** | Automation | Safe sequential command execution from YAML |
| **[sslcheck](sslcheck/)** | Cert Monitor | Check SSL certificate expiry info for domains |
| **[useraudit](useraudit/)** | User Auditor | Find UID 0 users, sudoers, and empty passwords |
| **[envcheck](envcheck/)** | Config Validator | Compare .env vs .env.example for missing keys |
| **[cronlook](cronlook/)** | Cron Visualizer | List user and system cron jobs clearly |

## Getting Started

1. **Install Requirements**:
   Each tool is standalone, but some have dependencies (check inner `requirements.txt`).
   ```bash
   pip install -r syscheck/requirements.txt
   pip install -r portaudit/requirements.txt
   ```

2. **Run a Tool (Directly)**:
   ```bash
   python syscheck/syscheck.py --cpu --memory
   python sslcheck/sslcheck.py google.com
   ```

3. **Run via Runner (Logs History)**:
   ```bash
   python runner.py sslcheck google.com
   ```

## Philosophy
- **Safe**: Non-destructive defaults.
- **Audit**: JSON output available for all tools.
- **Simple**: Easy to read and modify Python code.

## License
MIT

Author: Ruturaj Sharbidre


