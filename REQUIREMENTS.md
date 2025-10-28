# Streams Module Requirements

## Overview

**Current Status**: The Streams module currently provides a production-ready Matrix homeserver for federated real-time messaging.

**Future Vision**: This document specifies requirements for distributed content delivery (CDN), peer-to-peer distribution, media streaming (live/VOD), real-time data pipelines, and remote desktop services.

**All specifications below are for PLANNED FUTURE DEVELOPMENT unless explicitly marked as "Current".**

---

## Current Implementation

### Matrix Homeserver ✅

**Operational Features:**
- Matrix Synapse homeserver deployment via Docker Compose
- Element web client for browser-based access
- PostgreSQL backend for message storage
- End-to-end encryption (E2EE) for private rooms
- Federation with global Matrix network
- WebSocket-based real-time messaging

**Configuration:**
- `config/matrix/homeserver.yaml` - Synapse configuration
- `config/matrix/element-config.json` - Element client configuration
- Complete documentation in `config/matrix/README.md`

---

## Planned Feature Specifications

All sections below describe FUTURE capabilities that are not yet implemented.

---

## 1. Distributed CDN Infrastructure (PLANNED)

### 1.1 Edge Node Architecture

#### Edge Server Requirements
- **HTTP/2 and HTTP/3 Support**: QUIC protocol for reduced latency
- **Reverse Proxy**: High-performance request routing with connection pooling
- **Cache Storage**: NVMe-backed storage with LRU eviction (4TB+ per node)
- **Memory Cache**: In-memory hot object cache (Redis-compatible, 64GB+ RAM)
- **Concurrent Connections**: 100K+ simultaneous connections per node
- **Request Throughput**: 100K requests/sec per node (small objects)
- **Bandwidth**: 10 Gbps sustained, 40 Gbps burst per node

#### Cache Management
- **Cache Policies**
  - TTL-based expiration (configurable per content type)
  - LRU eviction when storage reaches 90% capacity
  - Cache warming: pre-populate edge with popular content
  - Negative caching: cache 404s for 60 seconds
  - Vary header support for multi-device content

- **Cache Invalidation**
  - Purge by URL, URL pattern, or cache tag
  - Purge propagation to all edges in <2 seconds
  - Soft purge: mark stale but serve if origin unavailable
  - Programmatic purge API with authentication
  - Automatic invalidation on origin content update

- **Intelligent Prefetching**
  - Analyze access patterns to predict next requests
  - Pre-fetch related assets (manifest → segments)
  - User-agent based prefetching (mobile vs desktop)
  - Geographic prefetching based on traffic patterns

---

## 2. Peer-to-Peer Distribution (PLANNED)

### 2.1 DHT (Distributed Hash Table)

**Implementation**: Kademlia protocol

- **Routing Table**: 160-bit node IDs, k-buckets (k=20)
- **Replication Factor**: 3 replicas per key
- **Lookup Performance**: O(log N) hops, <10 hops for 1M nodes
- **Key Storage**: Content ID (CID) → Peer list mapping
- **Node Discovery**: Bootstrap nodes + peer exchange
- **NAT Traversal**: STUN/TURN for firewall penetration

### 2.2 Swarming Protocol

**Implementation**: BitTorrent-inspired

- **Chunk Size**: 256 KB pieces
- **Piece Selection**: Rarest-first algorithm
- **Tracker**: Centralized or DHT-based tracker
- **Peer Exchange**: PEX protocol for tracker-less operation
- **Upload Slots**: 10-20 upload slots per peer
- **Choking Algorithm**: Optimistic unchoke every 30 seconds

### 2.3 WebRTC Mesh Networking

- **Mesh Topology**: Hybrid star-mesh (hub nodes + peer connections)
- **Max Peers**: 20-50 per client (browser limitation)
- **Data Channels**: Reliable and unreliable modes
- **Signaling**: WebSocket-based SDP exchange
- **ICE**: Interactive Connectivity Establishment for NAT traversal
- **STUN/TURN**: Public STUN servers + self-hosted TURN

### 2.4 Distributed Consensus

**Raft Consensus** (for edge coordination)
- **Leader Election**: Bully algorithm, election timeout 1000ms
- **Log Replication**: Append-only logs with majority quorum
- **Cluster Size**: 3, 5, or 7 nodes (odd numbers for split-brain prevention)
- **Commit Index**: Track committed vs. uncommitted entries

**CRDTs** (Conflict-free Replicated Data Types)
- **State Sync**: Eventually consistent state across edges
- **Conflict Resolution**: Last-write-wins or merge semantics
- **Use Cases**: Cache metadata, peer lists, configuration

---

## 3. Media Streaming (PLANNED)

### 3.1 Live Streaming

#### RTMP Ingest
- **Protocol**: RTMP/RTMPS (port 1935/443)
- **Concurrent Streams**: 1000+ per server
- **Authentication**: Stream keys or JWT tokens
- **Failover**: Primary + backup ingest endpoints

#### Transcoding
- **Hardware Acceleration**: NVIDIA NVENC, Intel QSV, AMD AMF
- **Bitrate Ladder**: 240p (400kbps) to 4K (16Mbps)
- **Codecs**: H.264 (primary), HEVC (optional)
- **GOP**: 2-second keyframe interval
- **Latency**: <50ms per segment

#### HLS/DASH Output
- **Segment Duration**: 2-6 seconds
- **Manifest Update**: Real-time for live streams
- **DVR Window**: Configurable (1-4 hours)
- **Format**: fMP4 (fragmented MP4) or MPEG-TS

#### WebRTC
- **Latency**: <500ms glass-to-glass
- **Codecs**: VP8, VP9, H.264
- **Audio**: Opus 48kHz
- **Architecture**: SFU (Selective Forwarding Unit)

### 3.2 Video-on-Demand (PLANNED)

- **Upload**: Chunked upload with resume (TUS protocol)
- **Transcoding**: Parallel transcoding of multiple qualities
- **Formats**: MP4, HLS, DASH, WebM
- **Thumbnails**: Extract keyframes, generate sprite sheets
- **Subtitles**: WebVTT, SRT, embedded captions

---

## 4. Edge Computing (PLANNED)

### 4.1 Edge Functions

- **Runtime**: V8 isolates for JavaScript/WASM
- **Languages**: JavaScript, TypeScript, WASM, Python (limited)
- **Cold Start**: <5ms for V8 isolates
- **Execution Time**: Max 50ms per request
- **Memory Limit**: 128MB per function

### 4.2 Use Cases

- **Request Modification**: Headers, body, routing
- **Authentication**: JWT validation, OAuth checks
- **A/B Testing**: Route to variants based on rules
- **Personalization**: User-specific content generation
- **Edge ML**: Inference using WASM-based ML models

---

## 5. Content-Addressed Storage (PLANNED)

### 5.1 IPFS-Style CID

- **Hash Function**: SHA-256 for content addressing
- **CID Format**: Base58 or Base32 encoded multihash
- **Deduplication**: Identical content → same CID
- **Immutability**: Content never changes for a given CID

### 5.2 Merkle DAG

- **Tree Structure**: Directed acyclic graph
- **Links**: CID references to child nodes
- **Versioning**: New version → new root CID
- **Delta Updates**: Only changed nodes need re-upload

---

## 6. Security Requirements (PLANNED)

### 6.1 Transport Security
- TLS 1.3 mandatory for all external connections
- Certificate auto-renewal via Let's Encrypt (ACME)
- HSTS header with max-age=31536000

### 6.2 Content Protection
- **Signed URLs**: HMAC-SHA256 with expiration
- **DRM**: FairPlay, Widevine, PlayReady
- **Geographic Restrictions**: IP geolocation enforcement
- **Hotlink Protection**: Referer validation

### 6.3 DDoS Mitigation
- **Rate Limiting**: 1K req/min for anon, 10K for auth
- **Challenge-Response**: CAPTCHA for suspicious traffic
- **IP Blocklisting**: Automatic and manual blocklists
- **Traffic Shaping**: QoS for different content types

---

## 7. Performance Targets (PLANNED)

### 7.1 CDN Performance

| Metric | Target | Maximum |
|--------|--------|---------|
| Edge Latency (cache hit) | <50ms P99 | <100ms P99.9 |
| Cache Hit Ratio | >95% | >90% (worst case) |
| Origin Offload | >90% | >80% (worst case) |
| Throughput per Edge | 10 Gbps sustained | 40 Gbps burst |
| Concurrent Connections | 100K per edge | 200K per edge |

### 7.2 P2P Performance

| Metric | Target |
|--------|--------|
| Origin Offload (popular content) | 60-90% |
| Peer Discovery (DHT) | <500ms |
| Mesh Formation (20 peers) | <2 seconds |
| DHT Routing (1M nodes) | <100ms |
| Swarm Piece Availability | >95% (>50 peers) |

### 7.3 Streaming Performance

| Metric | Target |
|--------|--------|
| RTMP Ingest Latency | <50ms |
| Transcode Latency (HW) | <50ms per segment |
| HLS End-to-End | 6-12 seconds |
| DASH End-to-End | 4-8 seconds |
| WebRTC End-to-End | <500ms |

---

## 8. Resource Requirements (PLANNED)

### 8.1 Edge Node

- **Minimum**: 4 CPU cores, 8GB RAM, 500GB NVMe, 1 Gbps network
- **Recommended**: 16 CPU cores, 64GB RAM, 4TB NVMe, 10 Gbps network
- **Concurrent Streams**: 1000 streams per 8GB RAM

### 8.2 Origin Server

- **Minimum**: 16 CPU cores, 64GB RAM, 10TB HDD, 10 Gbps network
- **Recommended**: 64 CPU cores, 256GB RAM, 50TB SSD, 40 Gbps network
- **GPU**: NVIDIA RTX 4090 or Tesla T4 for transcoding

### 8.3 P2P Node

- **DHT Node**: 1 CPU core, 512MB RAM, minimal storage
- **Swarm Tracker**: 2 CPU cores, 2GB RAM, 10GB storage
- **Edge P2P**: Same as edge node + P2P overhead (20% CPU)

---

## 9. Development Phases

### Phase 1: Core Streaming (Q1 2026)
- RTMP ingest server
- FFmpeg transcoding pipeline
- HLS/DASH packager
- S3-compatible storage backend
- Basic edge caching

### Phase 2: Edge Distribution (Q2 2026)
- Edge-to-origin replication
- Geographic load balancing
- Cache invalidation protocol
- Health monitoring and auto-scaling

### Phase 3: P2P Distribution (Q3 2026)
- DHT implementation (Kademlia)
- Swarm tracker and protocol
- WebRTC mesh networking
- JavaScript P2P client library

### Phase 4: Advanced Features (Q4 2026)
- Raft consensus for edges
- Content-addressed storage
- Edge serverless functions
- Blockchain-based features

### Phase 5: Remote Desktop (Q1 2027)
- RDP server implementation
- Virtual display management
- OBS WebSocket integration

---

## 10. Testing Strategy (PLANNED)

### 10.1 Unit Tests
- Coverage target: >80% for core modules
- Use test doubles for external dependencies
- Fast execution: <10 seconds for full suite

### 10.2 Integration Tests
- End-to-end workflows (upload → transcode → serve)
- Docker Compose test environments
- Real protocol testing (RTMP, HLS, WebRTC)

### 10.3 Load Testing
- Tools: Locust, k6, Apache JMeter
- Scenarios: 100K req/sec edge load, 10K concurrent streams
- Metrics: P50/P95/P99 latency, error rate, throughput

### 10.4 Chaos Testing
- Random edge node failures
- Network partitions
- Origin overload scenarios

---

## 11. Monitoring & Observability (PLANNED)

### 11.1 Metrics
- **Prometheus**: Time-series metrics (15s scrape interval)
- **StatsD**: Application metrics (counters, gauges)
- **OpenTelemetry**: Distributed tracing (1% sample rate)

### 11.2 Logging
- **Structured Logs**: JSON format
- **Aggregation**: Loki or Elasticsearch
- **Retention**: 7 days hot, 90 days cold

### 11.3 Dashboards
- CDN: Global traffic map, request rate, bandwidth
- Streaming: Active streams, viewers, bitrate
- P2P: Swarm health, DHT routing, peer count
- Edge: Per-node metrics, cache hit ratio

---

## 12. API Specifications (PLANNED)

### 12.1 CDN API

```
POST   /api/v1/cdn/edge/register     # Register new edge node
POST   /api/v1/cdn/cache/purge       # Purge cache by URL/pattern
GET    /api/v1/cdn/analytics/traffic # Traffic statistics
GET    /api/v1/cdn/health            # Health check
```

### 12.2 Streaming API

```
POST   /api/v1/upload                # Upload video
GET    /api/v1/videos/:id            # Video metadata
POST   /api/v1/stream/start          # Start live stream
POST   /api/v1/stream/stop           # Stop live stream
POST   /api/v1/transcode             # Trigger transcoding
```

### 12.3 P2P API

```
GET    /api/v1/dht/lookup/:cid       # DHT content lookup
POST   /api/v1/swarm/announce        # Announce to swarm
GET    /api/v1/peers/:cid            # Get peer list for content
POST   /api/v1/ipfs/add              # Add content with CID
```

---

## 13. Implementation Notes

### Current Reality
- **Operational**: Matrix homeserver only
- **Configuration**: Docker Compose, Synapse, Element
- **Testing**: 1 basic smoke test

### Future Implementation
- All CDN, P2P, streaming, edge, and RDP features are SPECIFICATIONS ONLY
- No code exists for these features yet
- Roadmap targets Q1 2026 - Q1 2027 for phased implementation
- Performance targets are ASPIRATIONAL based on industry benchmarks

### Documentation Accuracy
- `README.md`: Clearly separates current vs. planned
- `REQUIREMENTS.md`: All marked as planned unless specified
- `config/matrix/`: Real, operational configuration

---

## License

MIT License - Copyright © 2025 Independent AI Labs
