# SSLCheck - SSL Certificate Monitor

SSLCheck connects to a domain and verifies the SSL certificate expiration date.

## Purpose
Prevent website downtime by getting alerted before certificates expire.

## Installation
No dependencies required. Standard library only.

## Usage
```bash
# Check google.com
python sslcheck.py google.com

# Check internal service on port 8443
python sslcheck.py internal.corp --port 8443

# Set custom warning threshold (e.g. 30 days)
python sslcheck.py google.com --days 30
```
