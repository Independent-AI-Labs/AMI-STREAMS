# AMI Streams Module

Streams is where AMI explores real-time intelligence. It exists to incubate streaming pipelines and event-driven agent workflows that will eventually power responsive user experiences.

## What You Get Today

Right now the module provides scaffolding (package layout, tests, setup scripts) but no production-ready services.

## Current State

- `module_setup.py` delegates to Base `EnvironmentSetup` and installs dependencies without third-party imports at module scope.
- `backend/` contains prototype code for future stream processors; none of it is wired into runners yet.
- `scripts/run_tests.py` executes the Python test suite (currently minimal smoke coverage).

## Development Expectations

- When introducing runnable services or MCP servers, document the entry points here and in `docs/Architecture-Map.md`.
- Reuse Base `PathFinder` helpers for any runners that need to manipulate import paths.
- Update `docs/Next-Steps.md` once the module ships an initial streaming pipeline so the modernization checklist reflects reality.

Until runtime components are implemented, treat this module as dormant and avoid marketing it as operational.
