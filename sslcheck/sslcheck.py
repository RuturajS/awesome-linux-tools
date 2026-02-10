import argparse
import ssl
import socket
import sys
from datetime import datetime

def check_ssl_expiry(host, port=443):
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=host,
    )
    
    # Set timeout
    conn.settimeout(5.0)

    try:
        conn.connect((host, port))
        ssl_info = conn.getpeercert()
        
        # Parse expiry date
        # Format: 'May 20 12:00:00 2025 GMT'
        expire_str = ssl_info['notAfter']
        expire_date = datetime.strptime(expire_str, r'%b %d %H:%M:%S %Y %Z')
        
        return expire_date
    except Exception as e:
        print(f"[!] Error connecting to {host}: {e}")
        return None
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(description="SSLCheck: SSL Certificate Expiry Monitor")
    parser.add_argument("domain", help="Domain to check (e.g., google.com)")
    parser.add_argument("--port", type=int, default=443, help="Port (default: 443)")
    parser.add_argument("--days", type=int, default=14, help="Warning threshold in days (default: 14)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    print(f"[*] Checking SSL for {args.domain}:{args.port}...")
    
    expiry = check_ssl_expiry(args.domain, args.port)
    
    if expiry:
        remaining = expiry - datetime.utcnow()
        days_left = remaining.days
        
        print(f"\nSubject: {args.domain}")
        print(f"Expires On: {expiry}")
        print(f"Time Left: {days_left} days")
        
        if days_left < 0:
            print(f"\n[!!!] CERTIFICATE EXPIRED {abs(days_left)} DAYS AGO [!!!]")
            sys.exit(1)
        elif days_left < args.days:
            print(f"\n[!] WARNING: Certificate expires soon (< {args.days} days)!")
            sys.exit(1)
        else:
            print(f"\n[OK] Certificate is valid.")
            sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
