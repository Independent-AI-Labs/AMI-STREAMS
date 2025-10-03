# AMI Streams Module

Streams is where AMI explores real-time intelligence. It exists to incubate streaming pipelines and event-driven agent workflows that will eventually power responsive user experiences.

## What You Get Today

**Operational Services**:
- **Matrix Homeserver** (Synapse + Element): Real-time messaging and event streaming infrastructure
  - Federated messaging protocol for secure communication
  - WebSocket-based event streaming
  - End-to-end encryption support
  - See `config/matrix/` for configuration and setup

**In Development**:
- OBS Studio integration for media streaming
- Virtual display management
- RDP streaming capabilities
- General data stream processing pipelines

## Current State

- `module_setup.py` delegates to Base `EnvironmentSetup` and installs dependencies without third-party imports at module scope.
- `backend/` contains prototype code for future stream processors; Matrix backend integration in progress.
- `config/matrix/` contains production-ready Matrix Synapse homeserver configuration.
- `scripts/run_tests.py` executes the Python test suite (currently minimal smoke coverage).

## Quick Start: Matrix Messaging

```bash
# Start Matrix stack
docker-compose -f ../../docker-compose.services.yml --profile matrix up -d

# Access Element web client
open http://localhost:8888

# Create admin user
docker exec -it ami-matrix-synapse register_new_matrix_user \
  -u admin -p <password> -a http://localhost:8008
```

See [`config/matrix/README.md`](config/matrix/README.md) for complete Matrix setup and integration documentation.

## Development Expectations

- When introducing runnable services or MCP servers, document the entry points here and in `docs/Architecture-Map.md`.
- Reuse Base `PathFinder` helpers for any runners that need to manipulate import paths.
- Update `docs/Next-Steps.md` once the module ships an initial streaming pipeline so the modernization checklist reflects reality.

Until runtime components are implemented, treat this module as dormant and avoid marketing it as operational.
