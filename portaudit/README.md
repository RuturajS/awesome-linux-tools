# PortAudit - Port & Service Visualizer

PortAudit shows which programs are using which network ports on your machine, with a clean color-coded output.

## Purpose
Identify what services are listening on your system and detect unauthorized open ports.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
# Show all network connections (Listening & Established)
python portaudit.py

# Show ONLY listening ports (Server services)
python portaudit.py --listen

# Check who is using a specific port (e.g., 80)
python portaudit.py --port 80
```

## Features
- **Color-coded Status**:
  - `LISTEN` (Green): Open ports waiting for connections.
  - `ESTABLISHED` (Blue): Active connections.
  - `TIME_WAIT` etc. (Yellow): Other states.
- **Process Mapping**: Shows the PID and Name of the program using the port.
- **Service Lookup**: Guesses the standard service name (e.g., http, ssh) for the port.
