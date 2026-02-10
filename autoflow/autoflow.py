import argparse
import sys
import subprocess
import os

# Try to import yaml
try:
    import yaml
except ImportError:
    print("Error: 'PyYAML' module not found.")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

ALLOWED_COMMANDS = ['echo', 'ls', 'date', 'uptime', 'whoami', 'pwd', 'cat', 'grep', 'wc', 'head', 'tail']

def is_safe(command_parts):
    """Check if command uses only whitelisted binaries"""
    if not command_parts:
        return False
    
    # Simple check: the binary must be in whitelist
    binary = command_parts[0]
    binary_name = os.path.basename(binary)
    
    return binary_name in ALLOWED_COMMANDS

def run_step(step, dry_run=False, force=False):
    """Run a single step"""
    import shlex
    
    name = step.get('name', 'Unnamed Step')
    cmd_str = step.get('run', '')
    
    print(f"[*] Step: {name}")
    print(f"    Command: {cmd_str}")
    
    if not cmd_str:
        print("    [!] Empty command. Skipping.")
        return False

    try:
        # Split command for shell=False execution
        cmd_parts = shlex.split(cmd_str)
    except ValueError:
        print(f"    [ERROR] Could not parse command string: {cmd_str}")
        return False

    # Security Check
    if not force:
        if not is_safe(cmd_parts):
            print(f"    [BLOCKED] Binary '{cmd_parts[0]}' is not in whitelist.")
            print(f"    Use --force to override. Allowed: {ALLOWED_COMMANDS}")
            return False

    if dry_run:
        print("    [DRY-RUN] Would execute now.")
        return True

    try:
        # Run command SAFELY without shell=True
        # This prevents shell injection (e.g. "echo hi; rm -rf /")
        result = subprocess.run(cmd_parts, shell=False, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"    [OUTPUT]: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"    [ERROR]: Command failed with exit code {e.returncode}")
        print(f"    [STDERR]: {e.stderr.strip()}")
        return False
    except FileNotFoundError:
        print(f"    [ERROR]: Command not found: {cmd_parts[0]}")
        return False


def main():
    parser = argparse.ArgumentParser(description="AutoFlow: Safe Workflow Automator")
    
    parser.add_argument("workflow", help="Path to YAML workflow file")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution")
    parser.add_argument("--force", action="store_true", help="Allow unsafe commands (DANGEROUS)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.workflow):
        print(f"Error: Workflow file {args.workflow} not found.")
        sys.exit(1)

    try:
        with open(args.workflow, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error parsing YAML: {e}")
        sys.exit(1)

    steps = data.get('steps', [])
    if not steps:
        print("No steps found in workflow.")
        sys.exit(0)

    print(f"Loaded {len(steps)} steps from {args.workflow}")
    
    if args.force:
        print("[!!!] FORCE MODE ENABLED - SECURITY CHECKS DISABLED [!!!]")

    for i, step in enumerate(steps, 1):
        print(f"\n--- Step {i}/{len(steps)} ---")
        success = run_step(step, dry_run=args.dry_run, force=args.force)
        if not success and not args.dry_run:
            print("\n[!] Workflow stopped due to error.")
            sys.exit(1)

    print("\n[+] Workflow Completed Successfully.")

if __name__ == "__main__":
    main()
