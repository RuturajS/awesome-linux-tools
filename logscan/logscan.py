import argparse
import sys
import os
import re
from datetime import datetime

TIMESTAMP_REGEX = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}' # Simple ISO format start

def scan_line(line, patterns):
    """
    Check if line matches any pattern.
    Returns the pattern that matched, or None.
    """
    for p in patterns:
        if re.search(p, line, re.IGNORECASE):
            return p
    return None

def analyze_file(filepath, patterns, args):
    """
    Analyze a single log file.
    """
    results = {p: 0 for p in patterns}
    matches = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for l_idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                    
                matched_pattern = scan_line(line, patterns)
                if matched_pattern:
                    results[matched_pattern] += 1
                    
                    if len(matches) < args.limit:
                        matches.append({
                            "line": l_idx + 1,
                            "file": filepath,
                            "pattern": matched_pattern,
                            "content": line[:200]  # Truncate long lines
                        })
    except Exception as e:
        print(f"[ERROR] Could not read {filepath}: {e}", file=sys.stderr)
        return None

    return {"counts": results, "matches": matches}

def main():
    parser = argparse.ArgumentParser(description="LogScan: Simple Log Analyzer")
    
    parser.add_argument("path", help="File or Directory to scan")
    parser.add_argument("--pattern", action="append", help="Regex patterns to search for (default: ERROR, CRITICAL, FAIL)")
    parser.add_argument("--limit", type=int, default=10, help="Max detailed matches to show per file (default: 10)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Default patterns if none provided
    if not args.pattern:
        patterns = ["ERROR", "CRITICAL", "FAIL", "EXCEPTION"]
    else:
        patterns = args.pattern

    # Resolve paths
    target_path = os.path.abspath(args.path)
    if not os.path.exists(target_path):
        print(f"Error: Path not found: {target_path}")
        sys.exit(1)

    print(f"[*] Scanning {target_path} for patterns: {patterns}...")
    
    files_to_scan = []
    if os.path.isfile(target_path):
        files_to_scan.append(target_path)
    else:
        for root, dirs, files in os.walk(target_path):
            for file in files:
                if file.endswith(('.log', '.txt', '.out', '.err')):
                    files_to_scan.append(os.path.join(root, file))
    
    overall_report = {}
    
    for fpath in files_to_scan:
        start_time = datetime.now()
        data = analyze_file(fpath, patterns, args)
        if data:
            overall_report[fpath] = data
            
            if not args.json:
                print(f"\n--- Report for: {fpath} ---")
                for p, count in data['counts'].items():
                    if count > 0:
                        print(f"  [{p}]: {count}")
                
                if data['matches']:
                    print(f"  First {len(data['matches'])} matches:")
                    for m in data['matches']:
                        print(f"    Line {m['line']}: {m['content']}")
        else:
            if not args.json:
               print(f"[Skipped/Error] {fpath}")

    if args.json:
        print(json.dumps(overall_report, indent=4))
    else:
        print("\n[*] Scan Complete.")

if __name__ == "__main__":
    main()
