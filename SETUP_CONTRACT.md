# Streams Module - Setup Contract

Status
- `module_setup.py` delegates to Base `AMIModuleSetup` (Python 3.12) and contains no third-party imports at module scope.
- The module ships a `scripts/run_tests.py` runner but no production services yet; backend prototypes live under `backend/` and are considered experimental.

Contract
- Keep runner scripts responsible for path setup (use Base `PathFinder` helpers once streaming services are ready to run).
- Document any new MCP servers or pipelines alongside their runners/tests so the orchestrator can enforce the same contract as other modules.

Policy references
- Orchestrator contract: `docs/Setup-Contract.md`
- Base setup utilities: `base/backend/utils/{path_finder.py,environment_setup.py,path_utils.py}`
