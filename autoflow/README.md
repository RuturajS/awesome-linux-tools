# AutoFlow - Safe Workflow Automation

AutoFlow executes sequential commands from a YAML file.

## Purpose
Automate routine tasks safely. By default, only safe "read-only" commands are allowed.

## Installation
```bash
pip install -r requirements.txt
```

## Security
Unless `--force` is used, only the following commands are allowed:
`echo`, `ls`, `date`, `uptime`, `whoami`, `pwd`, `cat`, `grep`, `wc`, `head`, `tail`

## Usage
1. Create a workflow YAML file (see `sample.yaml`).
2. Run the tool:

```bash
# Dry run to verify steps
python autoflow.py sample.yaml --dry-run

# Execute workflow
python autoflow.py sample.yaml

# Execute risky workflow (allows non-whitelisted commands like mkdir, rm)
python autoflow.py deploy_script.yaml --force
```

## Workflow Format
```yaml
steps:
  - name: "Step Description"
    run: "command_to_execute"
```
