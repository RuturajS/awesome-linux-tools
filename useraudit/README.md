# UserAudit - User & Privilege Scanner

UserAudit parses system files (/etc/passwd, /etc/group) to identify users, privileges, and potential security risks.

## Purpose
Audit who has access to the system and who has root privileges.

## Installation
No dependencies required. Standard library only.

## Usage
```bash
# Basic audit (UID 0 and Sudoers)
python useraudit.py

# List users with login shells (bash/sh)
python useraudit.py --shells

# Check if home directories exist for users
python useraudit.py --home
```

## Checks
- **UID 0**: Identifies any user with ID 0 (root equivalent).
- **Privileged Groups**: Lists members of `sudo`, `wheel`, `admin`.
- **Login Shells**: filters service accounts to show real humans.
