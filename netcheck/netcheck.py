import argparse
import socket
import sys
import time
import urllib.request
import json
import subprocess
import platform

def check_ping(host):
    """
    Ping a host to check connectivity.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    
    try:
        # Use subprocess to run ping safely
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False

def check_port(host, port):
    """
    Check if a TCP port is open.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2) # 2 second timeout
    result = sock.connect_ex((host, int(port)))
    sock.close()
    return result == 0

def get_public_ip():
    """
    Get Public IP using ipify API.
    """
    try:
        url = "https://api.ipify.org?format=json"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data.get('ip')
    except Exception as e:
        return f"Error: {e}"

def main():
    parser = argparse.ArgumentParser(description="NetCheck: Network Diagnostic Tool")
    
    parser.add_argument("--ping", help="Host to ping")
    parser.add_argument("--port", help="Check port (format: host:port or port for localhost)")
    parser.add_argument("--ip", action="store_true", help="Get Public IP")
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.ip:
        print("[*] limit resolving Public IP...")
        ip = get_public_ip()
        print(f"Public IP: {ip}")

    if args.ping:
        print(f"[*] Pinging {args.ping}...")
        if check_ping(args.ping):
            print(f"[+] {args.ping} is UP")
        else:
            print(f"[-] {args.ping} is DOWN")

    if args.port:
        if ':' in args.port:
            host, port = args.port.split(':')
        else:
            host = '127.0.0.1'
            port = args.port
            
        print(f"[*] Checking {host}:{port}...")
        if check_port(host, port):
            print(f"[+] Port {port} on {host} is OPEN")
        else:
            print(f"[-] Port {port} on {host} is CLOSED/FILTERED")

if __name__ == "__main__":
    main()
