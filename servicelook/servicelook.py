import subprocess
import argparse
import sys
import shutil

# ANSI Colors
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def get_services(all_units=False):
    """
    Run systemctl list-units.
    Returns list of dicts: {unit, load, active, sub, description}
    """
    cmd = ['systemctl', 'list-units', '--type=service', '--no-pager', '--no-legend']
    if all_units:
        cmd.append('--all')

    try:
        # systemctl output is distinct columns, but spacing varies.
        # We try to trust the columns or split carefully.
        # Format: UNIT LOAD ACTIVE SUB DESCRIPTION
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"Error running systemctl: {res.stderr}")
            return []
        
        services = []
        for line in res.stdout.splitlines():
            parts = line.split(maxsplit=4)
            if len(parts) >= 5:
                services.append({
                    "unit": parts[0],
                    "load": parts[1],
                    "active": parts[2],
                    "sub": parts[3],
                    "desc": parts[4]
                })
        return services

    except FileNotFoundError:
        print("Error: 'systemctl' not found. Is this a systemd Linux?")
        return []

def main():
    parser = argparse.ArgumentParser(description="ServiceLook: System Service Viewer")
    parser.add_argument("--all", action="store_true", help="Show all services (inactive too)")
    parser.add_argument("--grep", help="Filter services by name", default="")
    parser.add_argument("--running", action="store_true", help="Show ONLY running services")
    parser.add_argument("--failed", action="store_true", help="Show ONLY failed services")
    
    args = parser.parse_args()
    
    if not shutil.which("systemctl"):
        print("Error: systemctl command not found.")
        sys.exit(1)

    print(f"[*] Listing Services...")
    
    # If user wants failed/running, we imply --all to search everything if needed, 
    # but strictly systemctl defaults to active only.
    # usually --all is needed to see 'dead' or 'failed' if they are not loaded?
    # actually failed are usually loaded.
    
    # If filtering, get all
    fetch_all = args.all or args.failed or args.grep
    services = get_services(all_units=fetch_all)
    
    # Headers
    print(f"{Colors.BOLD}{'UNIT':<40} {'STATUS':<15} {'SUB':<15} {'DESCRIPTION'}{Colors.RESET}")
    print("-" * 100)
    
    count = 0
    for s in services:
        # Filters
        if args.grep and args.grep.lower() not in s['unit'].lower():
            continue
        
        if args.running and s['active'] != 'active':
            continue
            
        if args.failed and s['active'] != 'failed':
            continue
            
        # Colorize
        color = Colors.RESET
        status = s['active']
        
        if status == 'active':
            color = Colors.GREEN
        elif status == 'failed':
            color = Colors.RED
        elif status == 'inactive':
            color = Colors.YELLOW
            
        print(f"{s['unit']:<40} {color}{status:<15}{Colors.RESET} {s['sub']:<15} {s['desc']}")
        count += 1
        
    print("-" * 100)
    print(f"Total shown: {count}")

if __name__ == "__main__":
    main()
