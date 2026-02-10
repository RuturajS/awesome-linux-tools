import argparse
import os
import sys
import stat
import hashlib

def get_file_hash(filepath, algo='sha256'):
    """Calculate SHA256 hash of a file"""
    hash_func = hashlib.sha256() if algo == 'sha256' else hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        return f"Error: {e}"

def is_world_writable(filepath):
    """Check if file has world writable permissions"""
    try:
        st = os.stat(filepath)
        return bool(st.st_mode & stat.S_IWOTH)
    except Exception:
        return False

def scan_directory(path, args):
    """Scan directory for large files and world writable files"""
    print(f"[*] Scanning {path}...")
    
    large_files = []
    writable_files = []
    
    limit_bytes = args.size * 1024 * 1024 # Convert MB to Bytes
    
    for root, dirs, files in os.walk(path):
        for name in files:
            filepath = os.path.join(root, name)
            
            # Check size
            try:
                fsize = os.path.getsize(filepath)
                if fsize > limit_bytes:
                    large_files.append((filepath, fsize))
            except OSError:
                continue
                
            # Check permissions
            if args.writable:
                if is_world_writable(filepath):
                    writable_files.append(filepath)

    return large_files, writable_files

def main():
    parser = argparse.ArgumentParser(description="FileGuard: File Integrity and Security Scanner")
    
    parser.add_argument("path", help="Directory to scan")
    parser.add_argument("--size", type=int, default=100, help="Size threshold in MB (default: 100MB)")
    parser.add_argument("--writable", action="store_true", help="Scan for world-writable files")
    parser.add_argument("--checksum", action="store_true", help="Calculate Checksum for large files")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: Path {args.path} does not exist.")
        sys.exit(1)
        
    large, writable = scan_directory(args.path, args)
    
    # Report
    print(f"\n--- Scan Report for {args.path} ---")
    
    if large:
        print(f"\n[!] Large Files (> {args.size}MB):")
        for f, s in large:
            size_mb = s / (1024 * 1024)
            hash_val = ""
            if args.checksum:
                hash_val = f" | SHA256: {get_file_hash(f)}"
            print(f"  {f} ({size_mb:.2f} MB){hash_val}")
    else:
        print(f"\n[+] No large files found (> {args.size}MB).")
        
    if args.writable:
        if writable:
            print("\n[!!!] World Writable Files (Security Risk):")
            for f in writable:
                print(f"  {f}")
        else:
            print("\n[+] No world-writable files found.")

if __name__ == "__main__":
    main()
