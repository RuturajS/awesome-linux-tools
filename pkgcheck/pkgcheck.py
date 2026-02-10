import subprocess
import shutil
import sys
import argparse

def get_manual_apt():
    """Debian/Ubuntu: apt-mark showmanual"""
    print("[*] Detecting APT (Debian/Ubuntu)...")
    try:
        res = subprocess.run(['apt-mark', 'showmanual'], stdout=subprocess.PIPE, text=True)
        return res.stdout.splitlines()
    except FileNotFoundError:
        return None

def get_manual_dnf():
    """Fedora/RHEL: dnf history userinstalled"""
    print("[*] Detecting DNF (Fedora/RHEL)...")
    try:
        res = subprocess.run(['dnf', 'history', 'userinstalled'], stdout=subprocess.PIPE, text=True)
        # Output format might vary, simpler to just return lines
        return res.stdout.splitlines()
    except FileNotFoundError:
        return None

def main():
    parser = argparse.ArgumentParser(description="PkgCheck: List Manually Installed Packages")
    parser.add_argument("--count", action="store_true", help="Only show count")
    args = parser.parse_args()

    packages = []
    manager = "Unknown"

    if shutil.which("apt-mark"):
        manager = "APT"
        packages = get_manual_apt()
    elif shutil.which("dnf"):
        manager = "DNF"
        packages = get_manual_dnf()
    else:
        print("[!] No supported package manager found (apt/dnf).")
        sys.exit(1)

    if packages is None:
        print("[!] Error running package manager command.")
        sys.exit(1)

    print(f"\n[+] Found {len(packages)} manually installed packages via {manager}.")
    
    if args.count:
        sys.exit(0)

    print("-" * 40)
    # Sort and print
    for pkg in sorted(packages):
        if pkg.strip():
            print(pkg)

if __name__ == "__main__":
    main()
