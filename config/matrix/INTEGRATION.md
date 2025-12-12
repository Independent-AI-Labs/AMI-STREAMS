# Matrix Homeserver Integration with Nodes Launcher

This document explains how the Matrix ISMS infrastructure integrates with the AMI Orchestrator service launcher system.

## Overview

The Matrix ISMS stack has been integrated into the AMI Orchestrator's service management system, allowing it to be launched and managed alongside other infrastructure services using the unified launcher interface.

## Integration Components

### 1. Docker Compose Services

**File**: `docker-compose.services.yml`

Three services added to support Matrix ISMS:

```yaml
services:
  matrix-postgres:
    # Dedicated PostgreSQL database for Matrix Synapse
    # Port: 5433 (to avoid conflict with main postgres on 5432)

  matrix-synapse:
    # Matrix Synapse homeserver (ISMS communications backbone)
    # Port: 8008 (HTTP), 8448 (Federation - currently disabled)
    # Depends on: matrix-postgres

  matrix-element:
    # Element web client for Matrix
    # Port: 8888
    # Depends on: matrix-synapse
```

**Network**: All services connected via `ami-isms-network` bridge network for isolation.

**Volumes**:
- `matrix_synapse_data`: Synapse homeserver data (signing keys, media, logs)
- `matrix_postgres_data`: PostgreSQL database data

**Configuration Mounts**:
- `./streams/config/matrix:/config:ro`: Synapse homeserver.yaml (read-only)
- `./streams/config/matrix/element-config.json:/app/config.json:ro`: Element client config (read-only)

### 2. Service Manifest

**File**: `scripts/services.yaml`

Three service definitions added:

```yaml
services:
  matrix-postgres:
    summary: PostgreSQL database dedicated to Matrix Synapse homeserver.
    compose:
      file: docker-compose.services.yml
      service: matrix-postgres
    module: streams
    tags:
      - security:internal-only
      - data:postgres
      - streams:matrix

  matrix-synapse:
    summary: Matrix Synapse homeserver for ISMS secure communications.
    compose:
      file: docker-compose.services.yml
      service: matrix-synapse
    module: streams
    depends_on:
      - matrix-postgres
    tags:
      - security:internal-only
      - streams:matrix
      - streams:messaging

  matrix-element:
    summary: Element web client for Matrix ISMS communications.
    compose:
      file: docker-compose.services.yml
      service: matrix-element
    module: streams
    depends_on:
      - matrix-synapse
    tags:
      - security:internal-only
      - streams:matrix
      - streams:ui
```

### 3. Service Profiles

**File**: `scripts/services.yaml`

Two new profiles for Matrix services:

```yaml
profiles:
  isms:
    description: ISMS communications stack (Matrix Synapse + Element + PostgreSQL).
    services:
      - matrix-postgres
      - matrix-synapse
      - matrix-element

  compliance:
    description: Compliance module infrastructure (ISMS + data backends).
    services:
      - data-postgres
      - data-redis
      - matrix-postgres
      - matrix-synapse
      - matrix-element
```

**Profile Usage**:
- `isms`: Launches only Matrix stack (for ISMS-focused development)
- `compliance`: Launches Matrix + data backends (for full compliance backend development)

## Launcher Integration

### Using Docker Compose Directly

```bash
# Start ISMS profile
docker-compose -f docker-compose.services.yml --profile isms up -d

# Start individual services
docker-compose -f docker-compose.services.yml up -d matrix-postgres matrix-synapse matrix-element

# Stop ISMS services
docker-compose -f docker-compose.services.yml --profile isms down

# View logs
docker-compose -f docker-compose.services.yml logs -f matrix-synapse
```

### Using Nodes Launcher (When Implemented)

**Note**: The nodes launcher is currently specified in `nodes/SPEC-LAUNCHER.md` but not yet implemented. When implemented, the following commands will be available:

```bash
# Start ISMS profile
python nodes/scripts/launch_services.py start --profile isms

# Start compliance profile (includes data backends)
python nodes/scripts/launch_services.py start --profile compliance

# Check status
python nodes/scripts/launch_services.py status --profile isms

# Stop ISMS services
python nodes/scripts/launch_services.py stop --profile isms

# Restart specific service
python nodes/scripts/launch_services.py restart matrix-synapse

# View logs
python nodes/scripts/launch_services.py logs matrix-synapse --follow
```

### Using Nodes Launcher MCP Server (Future)

When the launcher MCP server is implemented (`nodes/backend/mcp/launcher/launcher_server.py`), Matrix services will be controllable via MCP tools:

```python
# Start ISMS stack
result = mcp_client.call_tool("launcher.start_profile", {
    "profile": "isms"
})

# Check service status
status = mcp_client.call_tool("launcher.service_status", {
    "service_id": "matrix-synapse"
})

# Stop services
mcp_client.call_tool("launcher.stop_profile", {
    "profile": "isms"
})
```

## Dependency Graph

```
matrix-element
    ↓ depends_on
matrix-synapse
    ↓ depends_on
matrix-postgres
```

**Startup Order**:
1. `matrix-postgres` starts first (database)
2. `matrix-synapse` starts after postgres is healthy
3. `matrix-element` starts after synapse is running

**Health Checks**:
- `matrix-postgres`: `pg_isready` check (interval: 10s, retries: 30)
- `matrix-synapse`: HTTP `/health` endpoint check (interval: 30s, retries: 5, start_period: 60s)
- `matrix-element`: No health check (static web assets)

## Environment Configuration

### Default Environment

**File**: `compliance/default.env` (to be created)

The compliance module should ship a `default.env` with Matrix defaults:

```bash
# Matrix Synapse
MATRIX_SERVER_NAME=matrix.openami.local
MATRIX_HTTP_PORT=8008
MATRIX_FEDERATION_PORT=8448
MATRIX_NO_TLS=true
MATRIX_ENABLE_REGISTRATION=false

# Matrix PostgreSQL
MATRIX_POSTGRES_DB=synapse
MATRIX_POSTGRES_USER=synapse
MATRIX_POSTGRES_PASSWORD=synapse_dev_password
MATRIX_POSTGRES_PORT=5433

# Element Web
MATRIX_ELEMENT_PORT=8888
```

### User Overrides

Users can override defaults in `.env` or `.env.local`:

```bash
# Production settings in .env
MATRIX_SERVER_NAME=matrix.production.openami.org
MATRIX_POSTGRES_PASSWORD=production_secure_password_from_vault
MATRIX_NO_TLS=false  # Enable TLS in production
```

### Profile-Specific Overrides

**File**: `scripts/env/isms.yaml` (future)

When the launcher supports profile-specific environment overrides:

```yaml
# scripts/env/isms.yaml
shared:
  LOG_LEVEL: debug

modules:
  compliance:
    MATRIX_ENABLE_METRICS: "true"
    MATRIX_METRICS_PORT: "9000"

services:
  matrix-synapse:
    SYNAPSE_LOG_LEVEL: INFO
  matrix-postgres:
    POSTGRES_MAX_CONNECTIONS: "100"
```

## Service Lifecycle

### Startup

1. **Launcher** loads `scripts/services.yaml`
2. **Profile resolution** expands `isms` profile to service list
3. **Dependency sort** orders services topologically
4. **Docker Compose adapter** starts services in order:
   - `matrix-postgres` (waits for health check)
   - `matrix-synapse` (waits for postgres healthy + synapse /health)
   - `matrix-element` (starts immediately)
5. **State tracking** updates `.runtime/launcher/state.json`

### Monitoring

**Launcher** (when implemented) will:
- Poll health endpoints (Synapse: `http://localhost:8008/health`)
- Capture logs to `.runtime/launcher/logs/matrix-synapse.log`
- Track service state (STARTING → RUNNING → HEALTHY)
- Restart on failure if `restart_policy: on-failure`

### Shutdown

1. **Launcher** receives stop command
2. **Dependency order** reversed for graceful shutdown:
   - `matrix-element` stops first
   - `matrix-synapse` stops second
   - `matrix-postgres` stops last
3. **SIGTERM** sent, then SIGKILL after timeout
4. **State update** marks services as STOPPED

## Integration with Compliance Backend

### Matrix Bridge MCP Server

**File**: `compliance/backend/mcp/matrix_bridge_server.py` (to be implemented)

The Matrix Bridge MCP server will integrate with the launcher to:

1. **Check Matrix availability** before creating incident rooms:
   ```python
   status = await launcher_client.get_service_status("matrix-synapse")
   if status.state != "RUNNING":
       await launcher_client.start_service("matrix-synapse")
   ```

2. **Monitor Matrix health** and restart if needed:
   ```python
   if not await matrix_client.is_healthy():
       await launcher_client.restart_service("matrix-synapse")
   ```

3. **Coordinate startup** with compliance backend:
   ```python
   # Ensure Matrix is running before compliance backend starts
   await launcher_client.start_profile("isms")
   await launcher_client.wait_for_healthy("matrix-synapse")
   # Now start compliance backend
   ```

### Compliance Backend Service Definition

When compliance backend MCP server is implemented, it should be added to `scripts/services.yaml`:

```yaml
services:
  compliance-backend:
    summary: Compliance backend MCP server with Matrix integration.
    type: mcp
    module: streams
    command: "uv run python -m compliance.backend.mcp.compliance_server"
    working_dir: "{repo_root}/compliance"
    depends_on:
      - matrix-synapse  # Requires Matrix for incident response
      - data-postgres   # Requires data backend
      - data-redis
    env_files:
      - compliance/default.env
    health:
      type: tcp
      port: 3000
      timeout: 5s
    restart: on-failure
    tags:
      - security:internal-only
      - compliance:backend
      - isms:integration
```

## Testing

### Integration Tests

**File**: `nodes/tests/launcher/test_matrix_integration.py` (to be created)

```python
async def test_isms_profile_startup():
    """Test ISMS profile starts all Matrix services in correct order."""
    launcher = ServiceLauncher()

    # Start ISMS profile
    await launcher.start_profile("isms")

    # Verify startup order
    assert launcher.get_service_state("matrix-postgres") == "RUNNING"
    assert launcher.get_service_state("matrix-synapse") == "RUNNING"
    assert launcher.get_service_state("matrix-element") == "RUNNING"

    # Verify health
    synapse_health = await launcher.check_health("matrix-synapse")
    assert synapse_health.healthy

    # Cleanup
    await launcher.stop_profile("isms")

async def test_matrix_dependency_handling():
    """Test Matrix services respect dependency chain."""
    launcher = ServiceLauncher()

    # Stop postgres (should cascade stop to synapse + element)
    await launcher.stop_service("matrix-postgres")

    assert launcher.get_service_state("matrix-synapse") == "STOPPED"
    assert launcher.get_service_state("matrix-element") == "STOPPED"

async def test_matrix_restart_on_failure():
    """Test Matrix services restart on failure."""
    launcher = ServiceLauncher()

    # Kill synapse container
    await launcher.kill_service("matrix-synapse")

    # Wait for restart
    await asyncio.sleep(10)

    # Verify restarted
    assert launcher.get_service_state("matrix-synapse") == "RUNNING"
```

## Monitoring & Observability

### Launcher State

**File**: `.runtime/launcher/state.json`

Example state after ISMS profile started:

```json
{
  "profiles": {
    "isms": {
      "started_at": "2025-10-02T20:00:00Z",
      "services": ["matrix-postgres", "matrix-synapse", "matrix-element"]
    }
  },
  "services": {
    "matrix-postgres": {
      "state": "RUNNING",
      "pid": null,
      "container_id": "abc123...",
      "started_at": "2025-10-02T20:00:05Z",
      "health": {
        "last_check": "2025-10-02T20:05:00Z",
        "healthy": true
      }
    },
    "matrix-synapse": {
      "state": "RUNNING",
      "container_id": "def456...",
      "started_at": "2025-10-02T20:00:35Z",
      "health": {
        "last_check": "2025-10-02T20:05:00Z",
        "healthy": true,
        "endpoint": "http://localhost:8008/health"
      }
    },
    "matrix-element": {
      "state": "RUNNING",
      "container_id": "ghi789...",
      "started_at": "2025-10-02T20:01:05Z"
    }
  }
}
```

### Logs

Logs will be captured to:
- `.runtime/launcher/logs/matrix-postgres.log`
- `.runtime/launcher/logs/matrix-synapse.log`
- `.runtime/launcher/logs/matrix-element.log`

### Metrics

When Matrix metrics are enabled (`MATRIX_ENABLE_METRICS=true`):
- Synapse metrics available at `http://localhost:9000/metrics` (Prometheus format)
- Launcher can scrape metrics for health monitoring
- PostgreSQL metrics available via `pg_stat_*` tables

## Future Enhancements

### Dynamic Service Discovery

Matrix Bridge could discover Matrix services via launcher API:

```python
# Instead of hardcoded localhost:8008
synapse_url = await launcher_client.get_service_endpoint("matrix-synapse", "http")
# Returns: http://localhost:8008

element_url = await launcher_client.get_service_endpoint("matrix-element", "http")
# Returns: http://localhost:8888
```

### Health-Based Alerting

Launcher could post Matrix health alerts to monitoring room:

```python
class MatrixHealthMonitor:
    async def on_health_failure(self, service_id: str):
        if service_id == "matrix-synapse":
            await matrix_client.post_message(
                room_id="#security-monitoring",
                message=f"⚠️ Matrix Synapse unhealthy! Attempting restart..."
            )
```

### Auto-Scaling

For production deployments, launcher could auto-scale Matrix workers:

```yaml
services:
  matrix-synapse:
    scale:
      min: 1
      max: 5
      metric: cpu_percent
      threshold: 80
```

## References

- [Launcher Specification](../../../launcher/SPEC-LAUNCHER.md)
- [Matrix Configuration](./README.md)
- [ISMS-Matrix Integration Plan](../../../compliance/docs/research/ISMS-MATRIX-INTEGRATION-PLAN.md)
- [Compliance Backend Spec](../../../compliance/docs/research/COMPLIANCE_BACKEND_SPEC.md)
- [Docker Compose Services](../../../docker-compose.services.yml)
- [Service Manifest](../../../scripts/services.yaml)
