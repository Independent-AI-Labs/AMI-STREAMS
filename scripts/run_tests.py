#!/usr/bin/env python
"""Run tests for the streams module."""

import subprocess
import sys
from pathlib import Path


def main():
    """Run tests using pytest."""
    # Get module root
    module_root = Path(__file__).parent.parent.resolve()

    # Get Python executable from venv
    if sys.platform == "win32":
        python_exe = module_root / ".venv" / "Scripts" / "python.exe"
    else:
        python_exe = module_root / ".venv" / "bin" / "python"

    if not python_exe.exists():
        print(f"Python executable not found at {python_exe}")
        sys.exit(1)

    # Run pytest with any provided arguments
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    cmd = [str(python_exe), "-m", "pytest"] + args

    print("=" * 60)
    print("Running Streams Tests")
    print("=" * 60)
    print(f"Running tests in {module_root}")
    print(f"Command: {' '.join(cmd)}")

    # Run the tests
    result = subprocess.run(cmd, cwd=str(module_root), check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
