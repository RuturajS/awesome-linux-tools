# EnvCheck - Environment Config Validator

EnvCheck compares your local `.env` file against a reference `.env.example` to ensure no configuration keys are missing.

## Purpose
Prevent deployment errors caused by missing environment variables.

## Installation
No dependencies required. Standard library only.

## Usage
```bash
# Compare .env with .env.example
python envcheck.py .env .env.example

# Strict mode (Fail if .env has extra keys not in example)
python envcheck.py .env .env.example --strict
```
