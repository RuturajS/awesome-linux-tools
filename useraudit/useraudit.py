import argparse
import sys
import os
import glob

def get_users():
    """Parse /etc/passwd"""
    users = []
    try:
        with open("/etc/passwd", "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) >= 7:
                    users.append({
                        "username": parts[0],
                        "uid": int(parts[2]),
                        "gid": int(parts[3]),
                        "shell": parts[6],
                        "home": parts[5]
                    })
    except FileNotFoundError:
        print("[!] /etc/passwd not found (Non-Linux system?)")
        # Dummy data for testing on Windows
        if os.name == 'nt':
            print("[*] Running in Demo Mode (Windows)")
            users.append({"username": "root", "uid": 0, "gid": 0, "shell": "/bin/bash", "home": "/root"})
            users.append({"username": "user", "uid": 1000, "gid": 1000, "shell": "/bin/bash", "home": "/home/user"})
            users.append({"username": "nobody", "uid": 65534, "gid": 65534, "shell": "/bin/false", "home": "/nonexistent"})
    return users

def get_groups():
    """Parse /etc/group"""
    groups = {}
    try:
        with open("/etc/group", "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) >= 4:
                    # group:x:gid:user1,user2
                    groups[parts[0]] = parts[3].split(",") if parts[3] else []
    except FileNotFoundError:
        if os.name == 'nt':
             groups = {"sudo": ["user"], "root": ["root"]}
    return groups

def audit_users(args):
    users = get_users()
    groups = get_groups()
    
    print(f"[*] Auditing {len(users)} users...")
    
    # 1. Check for UID 0 (Non-root)
    print("\n[!] UID 0 Users (Root Privileges):")
    for u in users:
        if u['uid'] == 0:
            print(f"    - {u['username']} (Shell: {u['shell']})")

    # 2. Check for Sudo/Wheel access
    print("\n[!] Superusers (sudo/wheel group members):")
    privileged_groups = ['sudo', 'wheel', 'admin']
    for g_name in privileged_groups:
        if g_name in groups:
            members = groups[g_name]
            if members:
                print(f"    - Group '{g_name}': {', '.join(members)}")

    # 3. Check for users with shells
    if args.shells:
        print("\n[*] Users with Login Shells (bash/sh/zsh):")
        for u in users:
            shell = u['shell']
            if any(s in shell for s in ['bash', 'sh', 'zsh', 'fish']) and 'nologin' not in shell and 'false' not in shell:
                 print(f"    - {u['username']} ({u['shell']})")

    # 4. Check for Empty Password fields (Basic check in /etc/shadow requires root, so we skip specific shadow checks for non-root safety)
    # Instead, we check if home directory exists
    if args.home:
        print("\n[*] Checking Home Directories:")
        for u in users:
             if u['uid'] >= 1000 and u['uid'] < 60000: # Regular users usually
                exists = os.path.exists(u['home'])
                status = "OK" if exists else "MISSING"
                print(f"    - {u['username']}: {u['home']} [{status}]")

def main():
    parser = argparse.ArgumentParser(description="UserAudit: System User & Privilege Scanner")
    parser.add_argument("--shells", action="store_true", help="List users with valid login shells")
    parser.add_argument("--home", action="store_true", help="Check if home directories exist")
    
    args = parser.parse_args()
    
    audit_users(args)

if __name__ == "__main__":
    main()
