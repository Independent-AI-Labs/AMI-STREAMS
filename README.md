# AMI Streams Module

The Streams module is a work-in-progress space for real-time orchestration experiments. At the moment it provides scaffolding (package layout, tests, setup scripts) but no production-ready services.

## Current State

- `module_setup.py` delegates to Base `EnvironmentSetup` and installs dependencies without third-party imports at module scope.
- `backend/` contains prototype code for future stream processors; none of it is wired into runners yet.
- `scripts/run_tests.py` executes the Python test suite (currently minimal smoke coverage).

## Development Expectations

- When introducing runnable services or MCP servers, document the entry points here and in `docs/Architecture-Map.md`.
- Reuse Base `PathFinder` helpers for any runners that need to manipulate import paths.
- Update `docs/Next-Steps.md` once the module ships an initial streaming pipeline so the modernization checklist reflects reality.

Until runtime components are implemented, treat this module as dormant and avoid marketing it as operational.
