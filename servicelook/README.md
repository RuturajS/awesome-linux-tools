# ServiceLook - Systemd Service Viewer

ServiceLook provides a clean, colored list of systemd services.

## Purpose
Easily check what is running, what failed, and what is installed on your server.

## Installation
No dependencies required. Needs a `systemd` based Linux (Ubuntu, Debian, CentOS 7+, etc.).

## Usage
```bash
# List active services
python servicelook.py

# List ALL services (including stopped)
python servicelook.py --all

# Search for a service
python servicelook.py --grep ssh

# Show only FAILED services
python servicelook.py --failed
```
