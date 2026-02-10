import argparse
import os
import sys

def parse_env(filepath):
    """Parse .env file into a set of keys"""
    keys = set()
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key = line.split('=', 1)[0].strip()
                    keys.add(key)
    except FileNotFoundError:
        return None
    return keys

def main():
    parser = argparse.ArgumentParser(description="EnvCheck: Environment Configuration Validator")
    parser.add_argument("env_file", help="Path to actual .env file (e.g., .env)")
    parser.add_argument("example_file", help="Path to example file (e.g., .env.example)")
    parser.add_argument("--strict", action="store_true", help="Fail if extra keys are present in .env")
    
    args = parser.parse_args()
    
    print(f"[*] Comparing {args.env_file} vs {args.example_file}...")
    
    env_keys = parse_env(args.env_file)
    example_keys = parse_env(args.example_file)
    
    if env_keys is None:
        print(f"[!] Error: {args.env_file} not found.")
        sys.exit(1)
    if example_keys is None:
        print(f"[!] Error: {args.example_file} not found.")
        sys.exit(1)
        
    missing_in_env = example_keys - env_keys
    extra_in_env = env_keys - example_keys
    
    errors = 0
    
    if missing_in_env:
        print("\n[!] MISSING KEYS (Present in example, missing in .env):")
        for k in missing_in_env:
            print(f"    - {k}")
        errors += 1
    else:
        print("\n[OK] All required keys are present.")
        
    if extra_in_env:
        print("\n[i] EXTRA KEYS (Present in .env, not in example):")
        for k in extra_in_env:
            print(f"    + {k}")
        if args.strict:
            errors += 1
            
    if errors > 0:
        print("\n[FAILED] Verification failed.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] Environment config is valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()
