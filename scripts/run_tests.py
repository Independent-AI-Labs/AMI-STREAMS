#!/usr/bin/env python
"""Test runner for streams module."""

import sys
from pathlib import Path

# Get module root
MODULE_ROOT = Path(__file__).resolve().parent.parent

# Add streams and base to path (base imported as 'base')
sys.path.insert(0, str(MODULE_ROOT))
sys.path.insert(0, str(MODULE_ROOT.parent))

# Import from base using proper base. prefix
from base.scripts.run_tests import main  # noqa: E402

if __name__ == "__main__":
    # Run tests using base test runner with streams module root
    sys.exit(main(project_root=MODULE_ROOT, project_name="Streams"))
