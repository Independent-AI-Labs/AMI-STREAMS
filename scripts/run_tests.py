#!/usr/bin/env python
"""Test runner for streams module."""

import subprocess
import sys
from pathlib import Path

# Add current directory to path for ami_path import
sys.path.insert(0, str(Path(__file__).parent))

from ami_path import setup_ami_paths  # noqa: E402


def main() -> int:
    """Run tests for streams module."""
    # Pytest exit codes
    pytest_no_tests_collected = 5

    # Setup paths
    orchestrator_root, module_root, module_name = setup_ami_paths()

    # Find venv python executable
    venv_python = orchestrator_root / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        print("ERROR: Virtual environment not found at expected location")
        return 1

    # Check if tests directory exists
    tests_dir = module_root / "tests"
    if not tests_dir.exists():
        print("No tests directory found - nothing to test")
        return 0

    # Build pytest command
    cmd = [str(venv_python), "-m", "pytest", "tests/", "-v", "--timeout=600"]

    print(f"Running tests in {module_root}")
    print(f"Command: {' '.join(cmd)}")

    # Run pytest
    result = subprocess.run(cmd, cwd=str(module_root), check=False)

    # Exit code 5 means no tests collected - that's OK
    if result.returncode == pytest_no_tests_collected:
        print("No tests collected - that's OK")
        return 0

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
