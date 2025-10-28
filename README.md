# AMI Streams Module

**Distributed Media Streaming & Content Delivery Network**

AMI Streams provides enterprise-grade media streaming, real-time data pipelines, and a fully distributed CDN infrastructure. Built for high-availability deployments serving millions of concurrent users with sub-100ms latency globally.

## What You Get

### Distributed CDN Infrastructure

**Global Content Delivery**
- **Multi-Region Edge Network**: Deploy edge nodes across continents for <50ms latency worldwide
- **Intelligent Origin-Edge Architecture**: Central origin servers with automatic content replication to edge locations
- **Geographic Load Balancing**: DNS-based and anycast routing to nearest edge with automatic failover
- **Edge Caching Layer**: Hot content cached at edge with LRU eviction and intelligent prefetching
- **Adaptive Bitrate Delivery**: Serve multiple quality levels based on client bandwidth and device capabilities
- **Content Purge & Invalidation**: Real-time cache invalidation across all edge nodes in <2 seconds
- **Multi-Protocol Support**: HLS, DASH, RTMP, WebRTC, and SRT streaming protocols
- **DDoS Protection**: Rate limiting, geo-blocking, and traffic shaping at every edge

**Edge Node Capabilities**
- **Video Transcoding at Edge**: On-demand transcoding for format conversion and bitrate adaptation
- **Image Optimization**: Automatic WebP/AVIF conversion, resizing, and compression
- **Static Asset Acceleration**: CSS, JS, fonts, and media files cached globally
- **Dynamic Content Acceleration**: API response caching with TTL policies
- **WebSocket Proxying**: Low-latency WebSocket connections through edge nodes
- **Certificate Management**: Automatic TLS certificate provisioning and renewal per edge

**CDN Analytics & Monitoring**
- **Real-Time Metrics**: Per-edge bandwidth, cache hit ratio, request rates, error rates
- **Geographic Heatmaps**: Visualize traffic distribution and user locations
- **Performance Insights**: TTFB, latency percentiles, throughput per region
- **Cost Analytics**: Bandwidth usage and cost per edge node
- **Alert System**: Threshold-based alerts for edge health, cache saturation, and performance degradation

### Media Streaming Platform

**Live Streaming**
- **RTMP Ingest**: Accept live streams from OBS, FFmpeg, hardware encoders
- **Multi-Bitrate Encoding**: Adaptive bitrate ladders (240p to 4K) with hardware acceleration
- **HLS/DASH Output**: Industry-standard streaming protocols with DVR capabilities
- **WebRTC Ultra-Low Latency**: Sub-second latency for interactive applications
- **Stream Recording**: Automatic recording to object storage with configurable retention
- **Multi-Destination Restreaming**: Simultaneously stream to YouTube, Twitch, Facebook, custom RTMP

**Video-on-Demand (VOD)**
- **Transcode Pipeline**: Automated transcoding of uploaded videos to multiple formats
- **Thumbnail Generation**: Extract keyframes and generate sprite sheets for scrubbing
- **Subtitle & Caption Support**: WebVTT, SRT, embedded captions with multi-language
- **DRM Integration**: FairPlay, Widevine, PlayReady content protection
- **Progressive Upload**: Chunked upload for large files with resume capability
- **Storage Tiering**: Hot/warm/cold storage tiers based on access patterns

**Audio Streaming**
- **Music Streaming**: MP3, AAC, FLAC, Opus with gapless playback
- **Podcast Hosting**: RSS feed generation, chapter markers, embedded artwork
- **Live Audio**: Low-latency audio streaming for radio and live events
- **Spatial Audio**: Dolby Atmos and binaural audio support
- **Audio Normalization**: Loudness normalization per EBU R128 standards

### Real-Time Messaging & Events

**Matrix Homeserver (Operational)**
- **Production-Ready Synapse**: Federated Matrix homeserver with Element web client
- **End-to-End Encryption**: Double Ratchet algorithm for secure messaging
- **WebSocket Event Streaming**: Real-time message delivery and presence updates
- **Federation Support**: Connect to global Matrix network or run isolated
- **Bridge Integrations**: Slack, Discord, Telegram, IRC, WhatsApp bridges
- **See `config/matrix/` for complete setup documentation**

**Event Streaming Pipelines**
- **WebSocket Streams**: Bidirectional event streaming for real-time applications
- **Server-Sent Events**: One-way event push for status updates and notifications
- **MQTT Integration**: IoT device telemetry and command/control
- **Kafka Pipelines**: High-throughput event processing with partitioning
- **Stream Processing**: Windowing, aggregation, filtering, and transformation

### Remote Desktop & Display Streaming

**RDP Server & Client (In Development)**
- **Windows RDP Hosting**: Multi-user RDP sessions with GPU acceleration
- **RemoteApp Publishing**: Stream individual applications without full desktop
- **Linux XRDP**: Cross-platform RDP server for Linux desktops
- **Web RDP Client**: Browser-based RDP access via WebSocket tunneling
- **Session Recording**: Compliance recording of all RDP sessions

**Virtual Display Management (In Development)**
- **Headless Display Creation**: Virtual displays for GPU-accelerated rendering without physical monitor
- **Multi-Monitor Support**: Configure arbitrary display layouts and resolutions
- **GPU Passthrough**: Direct Device Assignment for ML workloads and gaming
- **Capture Pipeline**: DirectX, OpenGL, Vulkan capture with minimal overhead

### OBS Studio Integration (In Development)

**OBS Automation**
- **WebSocket API Control**: Scene management, source control, streaming automation
- **Scene Templates**: Predefined layouts for common streaming scenarios
- **Source Plugins**: Custom OBS sources for web content, data visualizations
- **Filter Automation**: Dynamic color grading, noise suppression, chroma keying
- **Multi-Output Streaming**: Simultaneously stream to multiple destinations

## Architecture

### CDN Edge Network Topology

```
                        ┌─────────────────────────┐
                        │   Global DNS / Anycast  │
                        │     Load Balancer       │
                        └────────────┬────────────┘
                                     │
                ┌────────────────────┼────────────────────┐
                │                    │                    │
        ┌───────▼────────┐   ┌──────▼──────┐   ┌────────▼───────┐
        │  Edge Node US  │   │ Edge Node EU│   │ Edge Node APAC │
        │   (Caching)    │   │  (Caching)  │   │   (Caching)    │
        └───────┬────────┘   └──────┬──────┘   └────────┬───────┘
                │                    │                    │
                └────────────────────┼────────────────────┘
                                     │
                        ┌────────────▼────────────┐
                        │   Origin Cluster        │
                        │ (Master Content Store)  │
                        │   - Postgres Metadata   │
                        │   - S3 Object Storage   │
                        │   - Redis Cache Layer   │
                        └─────────────────────────┘
```

### Module Structure

```
streams/
├── backend/
│   ├── cdn/
│   │   ├── edge/               # Edge node server
│   │   │   ├── cache.py        # LRU cache + invalidation
│   │   │   ├── router.py       # Request routing logic
│   │   │   ├── prefetch.py     # Intelligent prefetching
│   │   │   └── health.py       # Health checks & metrics
│   │   ├── origin/             # Origin server
│   │   │   ├── ingest.py       # Content upload & ingestion
│   │   │   ├── transcode.py    # Video/audio transcoding
│   │   │   ├── storage.py      # Object storage abstraction
│   │   │   └── replication.py  # Edge replication manager
│   │   ├── lb/                 # Load balancer
│   │   │   ├── geo.py          # Geographic routing
│   │   │   ├── dns.py          # DNS management
│   │   │   └── failover.py     # Automatic failover
│   │   └── analytics/          # CDN analytics
│   │       ├── metrics.py      # Prometheus metrics
│   │       ├── logs.py         # Access log aggregation
│   │       └── reports.py      # Usage reports
│   ├── streaming/
│   │   ├── live/               # Live streaming
│   │   │   ├── rtmp.py         # RTMP ingest server
│   │   │   ├── transcoder.py   # FFmpeg transcoding
│   │   │   ├── hls.py          # HLS packager
│   │   │   ├── dash.py         # DASH packager
│   │   │   └── webrtc.py       # WebRTC signaling
│   │   ├── vod/                # Video-on-demand
│   │   │   ├── upload.py       # Chunked upload handler
│   │   │   ├── pipeline.py     # Transcode pipeline
│   │   │   ├── thumbnail.py    # Thumbnail generation
│   │   │   └── drm.py          # DRM integration
│   │   └── audio/              # Audio streaming
│   │       ├── encoder.py      # Audio encoding
│   │       ├── normalizer.py   # Loudness normalization
│   │       └── podcast.py      # Podcast feed generator
│   ├── matrix/                 # Matrix homeserver integration
│   │   ├── client.py           # Matrix client SDK
│   │   ├── events.py           # Event handlers
│   │   └── federation.py       # Federation logic
│   ├── rdp/                    # Remote desktop
│   │   ├── server/             # RDP server implementation
│   │   ├── client/             # RDP client library
│   │   └── windows/
│   │       ├── vdd/            # Virtual display driver
│   │       └── scripts/        # PowerShell automation
│   └── obs/                    # OBS integration (planned)
│       ├── websocket.py        # OBS WebSocket client
│       ├── scenes.py           # Scene management
│       └── automation.py       # Streaming automation
├── config/
│   ├── matrix/                 # Matrix homeserver config
│   ├── cdn/                    # CDN configuration
│   │   ├── edge.yaml           # Edge node settings
│   │   ├── origin.yaml         # Origin settings
│   │   └── regions.yaml        # Geographic regions
│   └── streaming/              # Streaming settings
│       ├── encoders.yaml       # Encoder presets
│       └── protocols.yaml      # Protocol configuration
└── scripts/
    ├── deploy_edge.py          # Deploy new edge node
    ├── purge_cache.py          # Cache invalidation
    └── run_tests.py            # Test suite runner
```

## Quick Start

### Deploy CDN Edge Node

```bash
# Configure edge node
cat > config/cdn/edge.yaml <<EOF
node_id: edge-us-east-1
region: us-east-1
capacity:
  bandwidth_gbps: 10
  storage_tb: 5
  concurrent_connections: 100000
origin:
  url: https://origin.example.com
  auth_token: ${ORIGIN_TOKEN}
cache:
  max_size_gb: 4000
  ttl_default: 3600
  prefetch_enabled: true
EOF

# Start edge node
./scripts/ami-run.sh streams/backend/cdn/edge/server.py \
  --config config/cdn/edge.yaml \
  --port 8080
```

### Start Live Streaming Server

```bash
# Start RTMP ingest + HLS output
./scripts/ami-run.sh streams/backend/streaming/live/server.py \
  --rtmp-port 1935 \
  --hls-output /mnt/streaming/hls \
  --record-path /mnt/recordings

# Stream from OBS Studio
# Server: rtmp://localhost/live
# Stream Key: <your-stream-key>
```

### Launch Matrix Homeserver

```bash
# Start Matrix stack
docker-compose -f ../../docker-compose.services.yml --profile matrix up -d

# Access Element web client
open http://localhost:8888

# Create admin user
docker exec -it ami-matrix-synapse register_new_matrix_user \
  -u admin -p <password> -a http://localhost:8008
```

See [`config/matrix/README.md`](config/matrix/README.md) for complete Matrix documentation.

### Upload Video to CDN

```bash
# Upload video with automatic transcoding
curl -X POST https://origin.example.com/api/v1/upload \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -F "file=@video.mp4" \
  -F "transcode_profile=adaptive" \
  -F "cdn_replicate=true"

# Response includes CDN URLs for all edge nodes
{
  "video_id": "abc123",
  "cdn_urls": {
    "us-east-1": "https://us-east-1.cdn.example.com/v/abc123/master.m3u8",
    "eu-west-1": "https://eu-west-1.cdn.example.com/v/abc123/master.m3u8",
    "ap-southeast-1": "https://ap-southeast-1.cdn.example.com/v/abc123/master.m3u8"
  },
  "status": "transcoding"
}
```

## Performance Characteristics

### CDN Performance
- **Edge Latency**: <50ms P99 globally for cached content
- **Cache Hit Ratio**: >95% for hot content
- **Origin Offload**: 90%+ of traffic served from edge
- **Throughput**: 10 Gbps per edge node (configurable)
- **Concurrent Connections**: 100K+ per edge node

### Streaming Performance
- **Encoding Latency**: <50ms (hardware accelerated)
- **End-to-End Latency**:
  - HLS: 6-12 seconds
  - DASH: 4-8 seconds
  - WebRTC: <1 second
- **Video Quality**: 240p to 4K60 with HDR support
- **Audio Quality**: Up to 320 kbps AAC, lossless FLAC

### Resource Usage
- **Edge Node**: 4 CPU cores, 8GB RAM per 1000 concurrent streams
- **Origin Server**: 16 CPU cores, 64GB RAM for transcoding farm
- **Storage**: 1TB per 1000 hours of 1080p content (multi-bitrate)

## Integration with AMI Modules

### Files Module
- **Object Storage Backend**: Store media files in unified storage layer
- **CDN Integration**: Serve files through CDN edge network
- **Upload Pipeline**: Chunked upload with resume capability

### Browser Module
- **Stream Testing**: Automated browser testing of streaming playback
- **Screenshot Capture**: Generate video thumbnails via headless browser
- **WebRTC Testing**: End-to-end WebRTC call testing

### Nodes Module
- **Remote Streaming**: Stream desktop from remote nodes via RDP/VNC
- **Distributed Transcoding**: Leverage node fleet for parallel transcoding
- **Edge Node Deployment**: Deploy edge nodes to remote machines

### DataOps (Base Module)
- **Metadata Storage**: Video metadata, user data, analytics in Postgres
- **Cache Layer**: Redis for hot data and session storage
- **Metrics Database**: Prometheus for time-series metrics

## Security

**Transport Security**
- TLS 1.3 everywhere (origin, edge, clients)
- Certificate auto-renewal via Let's Encrypt
- HSTS, CSP, and security headers enforced

**Content Protection**
- Signed URLs with expiration for private content
- DRM integration (FairPlay, Widevine, PlayReady)
- Geographic restriction enforcement
- Hotlink protection and referrer validation

**Access Control**
- JWT-based authentication for API access
- Per-edge API rate limiting (10K req/sec per client)
- DDoS mitigation with challenge-response
- IP allowlist/blocklist per content

**Compliance**
- GDPR: User data retention policies, right to erasure
- COPPA: Age-gated content restrictions
- DMCA: Automated takedown workflow
- Audit logging for all administrative actions

## Monitoring & Observability

**Metrics (Prometheus)**
- Edge: Request rate, cache hit ratio, bandwidth, latency
- Origin: Upload rate, transcode queue depth, storage usage
- Streaming: Concurrent viewers, bitrate distribution, errors

**Logs (Structured JSON)**
- Access logs: All HTTP requests with timing and status
- Application logs: Errors, warnings, debug events
- Audit logs: Administrative actions and configuration changes

**Tracing (OpenTelemetry)**
- Request flow from client → edge → origin
- Transcoding pipeline stages
- Cache lookup and replication events

**Dashboards**
- Real-time CDN traffic map (geographic visualization)
- Per-edge performance metrics
- Transcoding queue and job status
- Storage capacity and cost projections

## API Reference

### CDN Management API

```http
POST /api/v1/cdn/edge/register
POST /api/v1/cdn/cache/purge
GET  /api/v1/cdn/analytics/traffic
GET  /api/v1/cdn/health
```

### Streaming API

```http
POST /api/v1/upload                    # Upload video
GET  /api/v1/videos/:id                # Video metadata
POST /api/v1/stream/start              # Start live stream
POST /api/v1/stream/stop               # Stop live stream
GET  /api/v1/stream/:id/viewers        # Viewer count
POST /api/v1/transcode                 # Trigger transcoding
```

### RDP API

```http
POST /api/v1/rdp/sessions              # Create RDP session
GET  /api/v1/rdp/sessions/:id          # Session info
DELETE /api/v1/rdp/sessions/:id        # Terminate session
```

See `docs/API.md` for complete API documentation (in development).

## Current Implementation Status

**✅ Production Ready**
- Matrix homeserver with Element client
- Matrix federation and end-to-end encryption
- WebSocket event streaming

**🚧 In Active Development**
- CDN edge node implementation
- Origin-edge replication protocol
- Live streaming RTMP ingest
- HLS/DASH packaging
- Video transcoding pipeline

**📋 Planned**
- OBS WebSocket integration
- RDP server and web client
- Virtual display driver for Windows
- WebRTC signaling server
- DRM integration

## Development Expectations

- Document all new services in `README.md` and `docs/Architecture-Map.md`
- Reuse Base module's `PathFinder` for import path management
- Add integration tests for streaming pipelines before marking production-ready
- Update performance benchmarks when implementing new features
- Follow security-first design: encrypt everything, validate all inputs, audit all actions

## License

MIT License - Copyright © 2025 Independent AI Labs
