import argparse
import subprocess
import json
import sys

def check_docker_installed():
    """Check if docker is installed and accessible"""
    try:
        subprocess.run(["docker", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_containers(all=False):
    """Get list of containers"""
    cmd = ["docker", "ps", "--format", "{{.ID}}|{{.Image}}|{{.Status}}|{{.Names}}"]
    if all:
        cmd.append("-a")
        
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) == 4:
                    containers.append({
                        "id": parts[0],
                        "image": parts[1],
                        "status": parts[2],
                        "name": parts[3]
                    })
        return containers
    except subprocess.CalledProcessError as e:
        print(f"Error listing containers: {e.stderr}")
        return []

def inspect_container(container_id):
    """Inspect a container for security issues (privileged, root user)"""
    try:
        cmd = ["docker", "inspect", container_id]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        data = json.loads(result.stdout)
        if not data:
            return None
        
        config = data[0].get("Config", {})
        host_config = data[0].get("HostConfig", {})
        
        return {
            "user": config.get("User", ""),
            "privileged": host_config.get("Privileged", False),
            "pid_mode": host_config.get("PidMode", ""),
            "network_mode": host_config.get("NetworkMode", "")
        }
    except Exception:
        return None

def main():
    parser = argparse.ArgumentParser(description="DockerAudit: Simple Container Security Auditor")
    
    parser.add_argument("--audit", action="store_true", help="Audit running containers for security risks")
    parser.add_argument("--list", action="store_true", help="List active containers")
    parser.add_argument("--all", action="store_true", help="List all containers (including stopped)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if not check_docker_installed():
        print("Error: Docker is not installed or not in PATH.")
        sys.exit(1)

    report = {"containers": [], "issues": []}

    containers = get_containers(all=args.all)
    report["containers"] = containers
    
    if args.list or args.audit:
        if not args.json:
            print(f"Found {len(containers)} containers.")
            if args.list:
                for c in containers:
                    print(f"[{c['id']}] {c['name']} ({c['image']}) - {c['status']}")

    if args.audit:
        print("\n[*] Auditing Containers...")
        for c in containers:
            details = inspect_container(c['id'])
            if details:
                issues = []
                if details['privileged']:
                    issues.append("Privileged Mode")
                if details['user'] == "" or details['user'] == "0" or details['user'] == "root":
                   issues.append("Running as Root")
                if details['pid_mode'] == "host":
                    issues.append("Host PID Shared")
                
                if issues:
                    c['issues'] = issues
                    report["issues"].append({"id": c['id'], "name": c['name'], "issues": issues})
                    if not args.json:
                        print(f"[WARN] {c['name']} ({c['id']}): {', '.join(issues)}")
                else:
                    if not args.json:
                        print(f"[OK] {c['name']}")

    if args.json:
        print(json.dumps(report, indent=4))

if __name__ == "__main__":
    main()
