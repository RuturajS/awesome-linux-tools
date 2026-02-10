import psutil
import socket
import argparse
import sys
from datetime import datetime

# Try to import colorama
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    # Fallback class if colorama missing
    class Fore:
        GREEN = ""
        RED = ""
        YELLOW = ""
        CYAN = ""
        WHITE = ""
        BLUE = ""
        MAGENTA = ""
    class Style:
        RESET_ALL = ""
        BRIGHT = ""
    print("Suggestion: Install 'colorama' for colored output: pip install colorama")

def get_service_name(port, proto):
    try:
        return socket.getservbyport(port, proto)
    except:
        return "?"

def get_process_name(pid):
    if not pid:
        return "-"
    try:
        return psutil.Process(pid).name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return "Unknown"

def audit_ports(args):
    """
    Scan local network connections.
    """
    print(f"{Fore.CYAN}[*] Auditing Local Ports...{Style.RESET_ALL}")
    
    # Header
    header = f"{'PROTO':<5} {'LOCAL ADDRESS':<20} {'PORT':<8} {'STATUS':<15} {'PID':<8} {'SERVICE / PROCESS'}"
    print(f"\n{Style.BRIGHT}{header}{Style.RESET_ALL}")
    print("-" * len(header))
    
    connections = psutil.net_connections(kind='inet')
    
    # Sort: Listen first, then by port
    connections.sort(key=lambda x: (x.status != 'LISTEN', x.laddr.port))
    
    count_open = 0
    
    for conn in connections:
        if args.listen and conn.status != 'LISTEN':
            continue
            
        laddr = f"{conn.laddr.ip}"
        lport = conn.laddr.port
        
        # Filter logic
        if args.port and args.port != lport:
            continue
            
        proto = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
        status = conn.status
        pid = conn.pid
        
        proc_name = get_process_name(pid)
        service = get_service_name(lport, proto.lower())
        
        # Color logic
        status_color = Fore.GREEN if status == 'LISTEN' else Fore.YELLOW
        if status == 'ESTABLISHED':
            status_color = Fore.BLUE
            
        port_color = Fore.CYAN if lport < 1024 else Fore.WHITE
        
        # Format line
        line = f"{proto:<5} {laddr:<20} {port_color}{lport:<8}{Style.RESET_ALL} {status_color}{status:<15}{Style.RESET_ALL} {pid or '-':<8} {Fore.MAGENTA}{proc_name}{Style.RESET_ALL} ({service})"
        print(line)
        
        if status == 'LISTEN':
            count_open += 1
            
    print(f"\n{Fore.GREEN}[+] Found {count_open} listening ports.{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="PortAudit: Process & Port Usage Visualizer")
    
    parser.add_argument("--listen", action="store_true", help="Show ONLY listening ports (default: show all)")
    parser.add_argument("--port", type=int, help="Filter by specific port number")
    
    args = parser.parse_args()
    
    # Check for psutil
    if 'psutil' not in sys.modules:
        print("Error: 'psutil' module is required.")
        sys.exit(1)

    audit_ports(args)

if __name__ == "__main__":
    main()
