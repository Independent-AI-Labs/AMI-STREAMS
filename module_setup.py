#!/usr/bin/env python
"""Module setup for streams."""

import sys
from pathlib import Path

# Add paths FIRST!
LOCAL_DIR = Path(__file__).parent
sys.path.insert(0, str(LOCAL_DIR / "scripts"))

# Import ami_path directly from local scripts directory
from ami_path import setup_ami_paths  # noqa: E402

# Add other paths AFTER importing ami_path to avoid conflicts
sys.path.insert(0, str(LOCAL_DIR))
sys.path.insert(0, str(LOCAL_DIR.parent))

ORCHESTRATOR_ROOT, MODULE_ROOT, MODULE_NAME = setup_ami_paths()

# NOW safe to import from base
from base.module_setup import AMIModuleSetup  # noqa: E402


def main() -> int:
    """Set up the streams module."""
    try:
        # Create module setup with proper parameters
        module_setup = AMIModuleSetup(project_root=MODULE_ROOT, project_name=MODULE_NAME)

        # Run setup
        return module_setup.setup()

    except Exception as e:
        print(f"ERROR: Failed to set up streams module: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
