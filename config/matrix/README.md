# Matrix Homeserver Configuration

This directory contains configuration files for the Matrix Synapse homeserver and Element web client, providing real-time messaging and event streaming for the OpenAMI platform (part of the streams module).

## Quick Start

### 1. Start the ISMS Stack

Using docker-compose directly:
```bash
# Start Matrix stack (Matrix + PostgreSQL + Element)
docker-compose -f docker-compose.services.yml --profile matrix up -d

# Or start individual services
docker-compose -f docker-compose.services.yml up -d matrix-postgres matrix-synapse matrix-element
```

Using the nodes launcher (when implemented):
```bash
# Start Matrix profile
python nodes/scripts/launch_services.py start --profile matrix

# Or start streams-full profile (includes data backends)
python nodes/scripts/launch_services.py start --profile compliance
```

### 2. Access Services

- **Synapse Homeserver**: http://localhost:8008
- **Element Web Client**: http://localhost:8888
- **Matrix PostgreSQL**: localhost:5433

### 3. Initial Setup

On first run, Synapse will auto-generate configuration and signing keys in the volume:
```bash
# Check Synapse logs
docker logs ami-matrix-synapse

# Wait for "Synapse now listening on port 8008"
```

### 4. Create Admin User

```bash
# Register the first admin user (compliance bot)
docker exec -it ami-matrix-synapse register_new_matrix_user \
  -u compliance-bot \
  -p <secure-password> \
  -a \
  http://localhost:8008

# Register additional users
docker exec -it ami-matrix-synapse register_new_matrix_user \
  -u security-lead \
  -p <secure-password> \
  http://localhost:8008

docker exec -it ami-matrix-synapse register_new_matrix_user \
  -u compliance-manager \
  -p <secure-password> \
  http://localhost:8008

docker exec -it ami-matrix-synapse register_new_matrix_user \
  -u human-overseer \
  -p <secure-password> \
  http://localhost:8008
```

### 5. Create Initial Rooms

Access Element at http://localhost:8888 and create:

- **#security-team** - Security team coordination (Private, E2E encrypted)
- **#compliance-team** - Compliance team discussions (Private, E2E encrypted)
- **#human-oversight** - Human oversight approvals (Private, E2E encrypted)
- **#incident-response** - General incident coordination (Private, E2E encrypted)

**Room Settings to Configure**:
- Enable encryption (should be default)
- Set retention to 10 years (3650 days)
- Set room to invite-only
- Add room topic describing purpose

## Configuration Files

### homeserver.yaml

Main Synapse configuration enforcing ISMS requirements:

**Security Settings**:
- End-to-end encryption enabled by default
- Federation disabled (isolated homeserver)
- Registration disabled (admin provisioning only)
- Strong password policy (12+ chars, symbols, digits)

**Compliance Settings**:
- 10-year message retention (EU AI Act Article 12)
- PostgreSQL backend for auditability
- Local media retention: 3650 days
- Remote media purged after 90 days

**Rate Limiting**:
- Message rate: 10/sec, burst 20
- Login attempts: 0.17/sec, burst 3
- Room joins: 0.1/sec local, 0.01/sec remote

### element-config.json

Element web client configuration:

**Features**:
- Default server: http://localhost:8008
- Advanced encryption settings enabled
- Federation disabled by default
- Registration/password reset disabled (admin-only)
- Voice/video calls enabled (Jitsi integration)

**Branding**:
- "OpenAMI ISMS Element" branding
- Privacy/terms links to Element.io

## Environment Variables

Create `.env` in the root directory with Matrix settings:

```bash
# Matrix Synapse
MATRIX_SERVER_NAME=matrix.openami.local
MATRIX_HTTP_PORT=8008
MATRIX_FEDERATION_PORT=8448
MATRIX_NO_TLS=true
MATRIX_ENABLE_REGISTRATION=false
MATRIX_REPORT_STATS=no

# Matrix PostgreSQL
MATRIX_POSTGRES_DB=synapse
MATRIX_POSTGRES_USER=synapse
MATRIX_POSTGRES_PASSWORD=synapse_secure_password_change_me
MATRIX_POSTGRES_PORT=5433

# Element Web
MATRIX_ELEMENT_PORT=8888
```

**IMPORTANT**: Change `MATRIX_POSTGRES_PASSWORD` for production deployments!

## ISMS Integration

### Automated Incident Response

When a Layer 0 Axiom violation is detected:

1. **Incident Service** creates incident record
2. **Matrix Bridge** automatically creates dedicated room: `#incident-{id}`
3. **Stakeholders** invited based on severity:
   - CRITICAL: security-lead, human-overseer, cto, legal-counsel
   - HIGH: security-lead, compliance-manager
4. **Initial report** posted by compliance-bot
5. **Team coordination** occurs in encrypted room
6. **Evidence extraction** captures room transcript
7. **Room archived** with 10-year retention

### Human Oversight Approvals

When evolution step "Activate" requires approval:

1. **Evolution Service** posts to `#human-oversight` room
2. **Approval request** includes compliance check results, CST chains
3. **Human Overseer** reviews and responds
4. **Decision captured** as evidence (CST created)
5. **Pipeline proceeds** or blocks based on approval

### Evidence Collection

Compliance team discussions automatically tracked:

1. **Compliance team** mentions control ID in `#compliance-iso27001`
2. **Evidence Service** detects mention via webhook
3. **Message extracted** as evidence with timestamp, submitter
4. **Evidence linked** to control (e.g., ISO27001-9.4.3)
5. **Available in audit packet** for external auditors

## Maintenance

### Backup

```bash
# Backup PostgreSQL database
docker exec ami-matrix-postgres pg_dump -U synapse synapse > matrix_backup_$(date +%Y%m%d).sql

# Backup Synapse data volume
docker run --rm -v ami-matrix-synapse-data:/data -v $(pwd):/backup alpine \
  tar czf /backup/synapse_data_$(date +%Y%m%d).tar.gz /data

# Backup PostgreSQL data volume
docker run --rm -v ami-matrix-postgres-data:/data -v $(pwd):/backup alpine \
  tar czf /backup/matrix_postgres_$(date +%Y%m%d).tar.gz /data
```

### Restore

```bash
# Restore PostgreSQL database
cat matrix_backup_20251002.sql | docker exec -i ami-matrix-postgres psql -U synapse synapse

# Restore Synapse data volume
docker run --rm -v ami-matrix-synapse-data:/data -v $(pwd):/backup alpine \
  sh -c "cd /data && tar xzf /backup/synapse_data_20251002.tar.gz --strip 1"
```

### Monitoring

```bash
# Check service health
docker ps | grep matrix
docker logs ami-matrix-synapse --tail 100
docker logs ami-matrix-element --tail 100

# Check database
docker exec -it ami-matrix-postgres psql -U synapse -c "SELECT version();"
docker exec -it ami-matrix-postgres psql -U synapse -c "SELECT COUNT(*) FROM users;"

# Check Synapse health endpoint
curl http://localhost:8008/health
```

### Logs

```bash
# Synapse logs
docker logs ami-matrix-synapse -f

# PostgreSQL logs
docker logs ami-matrix-postgres -f

# Element logs
docker logs ami-matrix-element -f
```

### Upgrade

```bash
# Stop services
docker-compose -f docker-compose.services.yml --profile matrix down

# Pull latest images
docker-compose -f docker-compose.services.yml --profile matrix pull

# Start services
docker-compose -f docker-compose.services.yml --profile matrix up -d

# Check logs for migration
docker logs ami-matrix-synapse -f
```

## Troubleshooting

### Synapse won't start

**Check logs**:
```bash
docker logs ami-matrix-synapse
```

**Common issues**:
- Database not ready: Wait for `matrix-postgres` health check
- Config error: Check `homeserver.yaml` syntax
- Port conflict: Check `MATRIX_HTTP_PORT` not already in use

**Solution**:
```bash
# Restart with fresh logs
docker-compose -f docker-compose.services.yml restart matrix-synapse
docker logs ami-matrix-synapse -f
```

### Can't connect to Element

**Check services**:
```bash
docker ps | grep matrix
```

**Check Element config**:
```bash
docker exec ami-matrix-element cat /app/config.json
```

**Common issues**:
- Synapse not running: Start with `docker-compose up -d matrix-synapse`
- Wrong homeserver URL in config: Update `element-config.json`
- Browser cache: Clear cache or use incognito mode

### Users can't join rooms

**Check room settings**:
- Ensure E2E encryption keys are backed up
- Verify user has proper invites
- Check room is not federation-blocked

**Admin commands**:
```bash
# List all rooms
docker exec -it ami-matrix-synapse \
  sqlite3 /data/homeserver.db "SELECT room_id, name FROM rooms;"

# Check room members
docker exec -it ami-matrix-synapse \
  sqlite3 /data/homeserver.db \
  "SELECT user_id FROM room_memberships WHERE room_id='!abc:matrix.openami.local';"
```

### Database performance issues

**Check connections**:
```bash
docker exec -it ami-matrix-postgres \
  psql -U synapse -c "SELECT COUNT(*) FROM pg_stat_activity;"
```

**Optimize**:
```bash
# Vacuum database
docker exec -it ami-matrix-postgres \
  psql -U synapse -c "VACUUM ANALYZE;"

# Reindex
docker exec -it ami-matrix-postgres \
  psql -U synapse synapse -c "REINDEX DATABASE synapse;"
```

## Security Considerations

### Production Deployment

For production deployment:

1. **Enable TLS**: Set `MATRIX_NO_TLS=false` and provide certificates
2. **Change passwords**: Update `MATRIX_POSTGRES_PASSWORD`
3. **Enable monitoring**: Configure Synapse metrics endpoint
4. **Backup regularly**: Schedule automated backups
5. **Review logs**: Set up log aggregation and alerting
6. **Update regularly**: Keep Synapse and Element updated
7. **Enable federation selectively**: Only for trusted external auditors
8. **Configure firewall**: Restrict access to internal network only

### Encryption

- All rooms are E2E encrypted by default
- Users must back up encryption keys (Element prompts on first use)
- Recovery key should be stored securely (password manager)
- Room admins should verify device fingerprints

### Access Control

- Registration disabled (admin provisioning only)
- Room creation restricted to registered users
- Rooms are invite-only by default
- Guest access disabled

## Compliance

### ISO/IEC 27001:2022

- **Clause 7.4** (Communication): ✅ Secure channels for ISMS
- **Clause 16.1** (Incident Management): ✅ Incident-specific rooms
- **Annex A.5.24/A.5.26** (Incident Response): ✅ Coordination via Matrix

### EU AI Act

- **Article 12** (Logging): ✅ 10-year message retention
- **Article 26** (Human Oversight): ✅ Approval workflow via Matrix

### GDPR

- **Lawful basis**: Legitimate interest (ISMS operation)
- **Data minimization**: Only security/compliance team members
- **Storage limitation**: 10 years justified by regulatory requirements
- **Encryption**: E2E encryption protects personal data
- **Right to erasure**: Contact admin for data deletion (pseudonymization)

## References

- [Matrix Specification](https://spec.matrix.org/)
- [Synapse Documentation](https://matrix-org.github.io/synapse/latest/)
- [Element Documentation](https://element.io/help)
- [ISMS-Matrix Integration Plan](../../../compliance/docs/research/ISMS-MATRIX-INTEGRATION-PLAN.md)
- [Compliance Backend Spec](../../../compliance/docs/research/COMPLIANCE_BACKEND_SPEC.md)

## Support

- **Issues**: Report at https://github.com/Independent-AI-Labs/OpenAMI/issues
- **Security**: security@independentailabs.com
- **Compliance**: compliance@independentailabs.com
