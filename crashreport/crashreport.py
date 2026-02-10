import argparse
import sys
import os
import re
from datetime import datetime
import platform

# Default patterns that indicate a crash or critical failure
DEFAULT_PATTERNS = [
    r"segfault at",
    r"Segmentation fault",
    r"General Protection Fault",
    r"dumped core",
    r"kernel panic",
    r"Out of memory",
    r"oom-killer",
    r"Main process exited, code=exited",
    r"Process .* died",
    r"traceback \(most recent call last\)",
    r"Uncaught exception",
    r"fatal error"
]

def scan_file(filepath, patterns, context):
    """
    Scan a file for crash patterns and extract context.
    Returns a list of crash events.
    """
    events = []
    
    if not os.path.isfile(filepath):
        return events

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Found a crash! Extract context
                    start = max(0, i - context)
                    end = min(len(lines), i + context + 1)
                    
                    event = {
                        "file": filepath,
                        "line_number": i + 1,
                        "pattern": pattern,
                        "timestamp": extract_timestamp(line) or "Unknown",
                        "snippet": lines[start:end]
                    }
                    events.append(event)
                    break # Avoid duplicate hits for same line
    except Exception as e:
        print(f"[!] Error reading {filepath}: {e}")
        
    return events

def extract_timestamp(line):
    # Common log timestamp formats
    # Syslog: Feb 10 09:00:00
    # ISO: 2026-02-10T09:00:00
    ts_regexs = [
        r'^\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}',
        r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}'
    ]
    for r in ts_regexs:
        m = re.match(r, line)
        if m:
            return m.group(0)
    return None

def generate_report(events, output_file):
    """
    Write a formatted report to the output file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write(f"SYSTEM CRASH REPORT\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Host: {platform.node()} ({platform.system()})\n")
        f.write(f"Events Found: {len(events)}\n")
        f.write("=" * 60 + "\n\n")
        
        if not events:
            f.write("No crash events detected in scanned logs.\n")
            return

        for i, event in enumerate(events, 1):
            f.write(f"EVENT #{i}\n")
            f.write("-" * 20 + "\n")
            f.write(f"File: {event['file']}\n")
            f.write(f"Line: {event['line_number']}\n")
            f.write(f"Pattern Matched: '{event['pattern']}'\n")
            f.write(f"Timestamp: {event['timestamp']}\n\n")
            f.write("Context Snippet:\n")
            f.write("." * 40 + "\n")
            for line in event['snippet']:
                prefix = "> " if event['line_number'] in [l for l in range(1)] else "  " # Determine marker later
                # Simple strip
                f.write(f"  {line.strip()}\n")
            f.write("." * 40 + "\n\n")

def main():
    parser = argparse.ArgumentParser(description="CrashReport: Service Crash Analyzer & Reporter")
    
    parser.add_argument("path", help="Log file or Directory to scan")
    parser.add_argument("--output", "-o", default=f"crash_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", help="Output report file")
    parser.add_argument("--context", type=int, default=5, help="Number of context lines before/after crash (default: 5)")
    parser.add_argument("--pattern", action="append", help="Add custom regex pattern")
    
    args = parser.parse_args()
    
    patterns = DEFAULT_PATTERNS
    if args.pattern:
        patterns.extend(args.pattern)
        
    target = os.path.abspath(args.path)
    if not os.path.exists(target):
        print(f"Error: Path {target} not found.")
        sys.exit(1)
        
    print(f"[*] Scanning {target} for crash signatures...")
    events = []
    
    if os.path.isfile(target):
        events.extend(scan_file(target, patterns, args.context))
    else:
        for root, dirs, files in os.walk(target):
            for file in files:
                if file.endswith(('.log', '.txt', '.out', '.err')) or 'syslog' in file or 'messages' in file:
                    fpath = os.path.join(root, file)
                    events.extend(scan_file(fpath, patterns, args.context))
                    
    print(f"[*] Found {len(events)} potential crash events.")
    generate_report(events, args.output)
    print(f"[+] Report generated: {args.output}")

if __name__ == "__main__":
    main()
