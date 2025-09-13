# Streams Module — Setup Contract

Delegation
- `module_setup.py` delegates to Base `AMIModuleSetup` for venv creation and dependency installation.

Entrypoints
- Runner scripts under `streams/scripts/` (TBD) must perform path setup; application packages must not mutate `sys.path`.

Status
- Current `module_setup.py` adheres to delegation pattern and avoids third-party imports at top-level.

Policy references
- Orchestrator contract: `/docs/Setup-Contract.md`
- Base setup utilities: `base/backend/utils/{path_finder.py, environment_setup.py, path_utils.py}`
