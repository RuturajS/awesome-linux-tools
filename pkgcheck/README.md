# PkgCheck - Installed Package Auditor

PkgCheck lists packages that were installed **manually** by the user (not as dependencies).

## Purpose
Identify what software has been explicitly added to the system, helping to clean up bloat or document server setup.

## Supported Managers
- **APT** (Debian, Ubuntu, Kali) via `apt-mark showmanual`
- **DNF** (Fedora, RHEL, CentOS) via `dnf history userinstalled`

## Usage
```bash
# List all manually installed packages
python pkgcheck.py

# Just show the count
python pkgcheck.py --count
```
