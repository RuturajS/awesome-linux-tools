import argparse
import subprocess
import sys
import os

def get_user_crons():
    """Get current user's cron jobs"""
    try:
        result = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return []
        return [l for l in result.stdout.split('\n') if l.strip() and not l.strip().startswith('#')]
    except FileNotFoundError:
        return []

def get_system_crons():
    """Read /etc/crontab"""
    crons = []
    if os.path.exists('/etc/crontab'):
        try:
            with open('/etc/crontab', 'r') as f:
                for line in f:
                    if line.strip() and not line.strip().startswith('#') and not line.startswith('SHELL') and not line.startswith('PATH'):
                         crons.append(line.strip())
        except PermissionError:
            pass
    return crons

def parse_line(line):
    parts = line.split()
    if len(parts) < 6:
        return None
    
    # Simple Heuristic
    # * * * * * command
    schedule = " ".join(parts[:5])
    command = " ".join(parts[5:])
    
    return {"schedule": schedule, "command": command}

def main():
    parser = argparse.ArgumentParser(description="CronLook: Cron Job Visualizer")
    parser.add_argument("--system", action="store_true", help="Include system-wide crontab (/etc/crontab)")
    
    args = parser.parse_args()
    
    print("[*] Listing Cron Jobs...\n")
    
    jobs = []
    
    # User Crons
    user_crons = get_user_crons()
    if user_crons:
        print(f"--- User Crons ({len(user_crons)}) ---")
        for line in user_crons:
            parsed = parse_line(line)
            if parsed:
                print(f"[{parsed['schedule']:<15}] {parsed['command']}")
            else:
                print(f"[???] {line}")
    else:
        print("--- User Crons ---")
        print("No user cron jobs found (or no permission).")

    # System Crons
    if args.system:
        print("\n--- System Crons (/etc/crontab) ---")
        sys_crons = get_system_crons()
        for line in sys_crons:
            # System crons have an extra user field
            # * * * * * user command
            parts = line.split()
            if len(parts) >= 6:
                schedule = " ".join(parts[:5])
                user = parts[5]
                command = " ".join(parts[6:])
                print(f"[{schedule:<15}] {user:<10} {command}")
            else:
                print(line)

if __name__ == "__main__":
    main()
