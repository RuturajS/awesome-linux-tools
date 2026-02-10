import sys
import os
import subprocess
import datetime
import shlex

HISTORY_FILE = "tool_history.log"
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

def log_command(tool_name, args):
    """Log the command execution to history file"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cmd_str = f"{tool_name} {' '.join(args)}"
    
    try:
        with open(os.path.join(TOOLS_DIR, HISTORY_FILE), "a") as f:
            f.write(f"[{timestamp}] {cmd_str}\n")
    except Exception as e:
        print(f"[!] Warning: Could not write to history file: {e}")

def list_tools():
    """List available tools in the directory"""
    print("Available Tools:")
    for item in os.listdir(TOOLS_DIR):
        if os.path.isdir(os.path.join(TOOLS_DIR, item)):
            # Check if it has a .py file with the same name
            main_script = os.path.join(TOOLS_DIR, item, item + ".py")
            if os.path.exists(main_script):
                print(f"  - {item}")

def show_history():
    """Show execution history"""
    hist_path = os.path.join(TOOLS_DIR, HISTORY_FILE)
    if not os.path.exists(hist_path):
        print("No history found.")
        return

    print(f"--- Command History ({HISTORY_FILE}) ---")
    with open(hist_path, "r") as f:
        print(f.read())

def main():
    if len(sys.argv) < 2:
        print("Usage: python runner.py <tool_name> [args...]")
        print("       python runner.py --list      (List tools)")
        print("       python runner.py --history   (Show history)")
        sys.exit(1)

    tool_name = sys.argv[1]
    tool_args = sys.argv[2:]

    if tool_name == "--list":
        list_tools()
        sys.exit(0)
    
    if tool_name == "--history":
        show_history()
        sys.exit(0)

    # Find the tool script
    # Expected structure: tools_dir/toolname/toolname.py
    script_path = os.path.join(TOOLS_DIR, tool_name, f"{tool_name}.py")
    
    if not os.path.exists(script_path):
        print(f"Error: Tool '{tool_name}' not found.")
        print(f"Expected path: {script_path}")
        list_tools()
        sys.exit(1)

    # Log execution
    log_command(tool_name, tool_args)

    # Construct python command
    cmd = [sys.executable, script_path] + tool_args
    
    try:
        # Run the tool
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[!] Execution interrupted.")
    except Exception as e:
        print(f"[!] Error running tool: {e}")

if __name__ == "__main__":
    main()
