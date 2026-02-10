# NetCheck - Network Diagnostic Tool

NetCheck checks network connectivity, ports, and external IP.

## Purpose
Diagnose connection issues and verify service availability.

## Installation
No dependencies required. Standard library only.

## Usage
```bash
# Check internet connectivity
python netcheck.py --ping google.com

# Check if a local service is running (e.g., Web Server)
python netcheck.py --port 80

# Check remote port
python netcheck.py --port scanned.site:443

# Get Public IP address
python netcheck.py --ip
```

## Arguments
- `--ping <host>`: Check connectivity to a host.
- `--port <host:port>`: Check if a specific TCP port is open.
- `--ip`: Retrieve current public IP address.
