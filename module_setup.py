#!/usr/bin/env python
"""Streams module setup - uses base AMIModuleSetup."""

import subprocess
import sys
from pathlib import Path

# Get this module's root
MODULE_ROOT = Path(__file__).resolve().parent


def main():
    """Run setup for streams module by calling base module_setup.py directly."""
    # Find base module_setup.py
    base_setup = MODULE_ROOT.parent / "base" / "module_setup.py"
    if not base_setup.exists():
        print("ERROR: Cannot find base/module_setup.py")
        sys.exit(1)

    # Call base module_setup.py with appropriate arguments
    cmd = [sys.executable, str(base_setup), "--project-dir", str(MODULE_ROOT), "--project-name", "Streams Module"]

    result = subprocess.run(cmd, check=False)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
