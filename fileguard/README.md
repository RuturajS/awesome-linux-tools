# FileGuard - File Integrity & Security Scanner

FileGuard scans directories for potential security risks and storage anomalies.

## Purpose
Identify large files wasting space and world-writable files that pose a security risk.

## Installation
No dependencies required. Standard library only.

## Usage
```bash
# Scan directory for large files (>100MB by default)
python fileguard.py /var/www/html

# Scan for files larger than 50MB and check for world-writable permissions
python fileguard.py /home/user --size 50 --writable

# Calculate checksums for found files (for integrity verification)
python fileguard.py /opt/backup --checksum
```

## Arguments
- `path`: Directory to scan.
- `--size`: Size threshold in MB.
- `--writable`: Check for world-writable permissions (chmod 777).
- `--checksum`: Calculate SHA256 hash for flagged files.
