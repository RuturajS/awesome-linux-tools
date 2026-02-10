# DockerAudit - Container Security Scan

DockerAudit checks for common security misconfigurations in running Docker containers.

## Purpose
Identify risky containers (running as root, privileged mode, host PID sharing).

## Installation
Requires `docker` CLI tool to be installed and accessible.
No Python dependencies.

## Usage
```bash
# List all running containers
python dockeraudit.py --list

# Audit running containers for security risks
python dockeraudit.py --audit

# Audit ALL containers (including stopped)
python dockeraudit.py --audit --all

# JSON Report
python dockeraudit.py --audit --json
```

## Checks Performed
- **User**: Warns if running as `root` (User: "0", "root", or empty).
- **Privileged**: Warns if `--privileged` flag is used.
- **PID Mode**: Warns if sharing host PID namespace.
