# Contributing to Awesome Linux Tools

We welcome contributions to make this CLI toolkit even more awesome! Whether you're fixing a bug, adding a new tool, or improving documentation, here's how you can help.

## 🛠️ How to Add a New Tool

1. **Create a Folder**: Name it after your tool (e.g., `mytool/`).
2. **Standard Files**: Ensure your folder has:
   - `mytool.py`: The main script.
   - `README.md`: Short description and usage examples.
   - `requirements.txt`: Python dependencies (if any).
3. **Follow the Philosophy**:
   - **Safe**: No destructive actions by default.
   - **Modular**: Keep it self-contained.
   - **Audit**: Support `--json` output if possible.

## 🐛 Reporting Bugs

Open an issue on GitHub with:
- The tool name
- The command you ran
- The error message or unexpected behavior

## 📝 Style Guide

- Use standard Python libraries whenever possible.
- If external libraries are needed (e.g., `requests`, `psutil`), add them to `requirements.txt`.
- Add a shebang `#!/usr/bin/env python3` if intended for direct execution.
- Use `argparse` for command-line arguments.

## Pull Request Process

1. Fork the repo.
2. Create a new branch (`git checkout -b feature/new-tool`).
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.

Thank you for contributing!
