# PyGuardian v3 - High-Level Architecture

## System Overview

PyGuardian v3 is a distributed threat hunting and incident response platform designed for real-time network flow analysis, threat detection, and automated response.

## Core Components

### 1. Data Collection Layer
- **Collectors**: Network flow collectors (NetFlow, sFlow, IPFIX), log collectors (Syslog, Filebeat), and custom integrations
- **Message Broker**: Apache Kafka for high-throughput event streaming
- **Protocol**: TLS 1.3 encrypted communication with mutual authentication

### 2. Processing Layer
- **Enrichment Service**: Threat intelligence lookup, geolocation, asset correlation
- **Detectors**: Real-time rule engine for pattern matching and anomaly detection
- **Correlator**: Event correlation and incident creation with MITRE ATT&CK mapping

### 3. Storage Layer
- **ClickHouse**: Time-series flow data with compression and fast aggregations
- **PostgreSQL**: Incident management, user data, configuration, audit logs
- **MinIO (S3-compatible)**: Artifact storage, PCAP files, screenshots

### 4. Application Layer
- **FastAPI Backend**: RESTful API with OpenAPI documentation
- **React Frontend**: TypeScript-based dashboard with real-time updates
- **WebSocket**: Live event streaming and notifications

### 5. Security & Observability
- **Authentication**: JWT tokens with OAuth2 integration
- **Authorization**: RBAC with fine-grained permissions
- **Monitoring**: Prometheus metrics, OpenTelemetry tracing
- **Logging**: Structured JSON logs with correlation IDs

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Message Broker | Apache Kafka + Zookeeper | Event streaming |
| Flow Storage | ClickHouse | Time-series data |
| Relational DB | PostgreSQL 15+ | Metadata, incidents |
| Object Storage | MinIO | Artifacts, files |
| Backend API | FastAPI + Python 3.11 | REST API |
| Frontend | React 18 + TypeScript | Web dashboard |
| Maps | Mapbox GL JS | Geographic visualization |
| Styling | Tailwind CSS | UI framework |
| Authentication | JWT + OAuth2 | Security |
| Monitoring | Prometheus + Grafana | Metrics |
| Tracing | OpenTelemetry | Distributed tracing |

## Data Flow Architecture

```
[Network Devices] → [Collectors] → [Kafka] → [Enrichment] → [Detectors] → [Correlator] → [Storage]
                                                                    ↓
[UI Dashboard] ← [FastAPI] ← [PostgreSQL] ← [Incident Creation] ← [Alert Generation]
```

### Detailed Flow:
1. **Collection**: Network flows collected via NetFlow/sFlow/IPFIX
2. **Ingestion**: Raw events published to Kafka topics
3. **Enrichment**: Threat intel lookup, geolocation, asset correlation
4. **Detection**: Rule engine processes enriched events
5. **Correlation**: Events correlated into incidents with risk scoring
6. **Storage**: Data persisted across ClickHouse, PostgreSQL, MinIO
7. **Presentation**: Real-time dashboard with WebSocket updates

## Deployment Options

### Development (Docker Compose)
- Single-node deployment with all services
- Local development with hot reloading
- Integrated testing environment

### Production (Kubernetes + Helm)
- Multi-node cluster deployment
- Auto-scaling based on load
- High availability with redundancy
- Resource quotas and limits

## Security Architecture

### Network Security
- TLS 1.3 for all inter-service communication
- Network segmentation with service mesh
- Firewall rules for service isolation

### Authentication & Authorization
- JWT tokens with short expiration
- OAuth2 integration (Google, Azure AD)
- RBAC with role-based permissions
- API key management for integrations

### Secrets Management
- Kubernetes secrets or HashiCorp Vault
- Encrypted at rest and in transit
- Rotation policies for credentials

## Scaling Recommendations

### Horizontal Scaling
- Kafka partitions for parallel processing
- ClickHouse sharding for large datasets
- Multiple API instances behind load balancer
- Stateless services for easy scaling

### Performance Optimization
- ClickHouse materialized views for common queries
- Redis caching for frequently accessed data
- Connection pooling for database access
- CDN for static assets

### Resource Requirements (Small Deployment)
- **Core Services**: 2 CPU, 4GB RAM
- **ClickHouse**: 4 CPU, 8GB RAM
- **Kafka**: 2 CPU, 4GB RAM
- **PostgreSQL**: 2 CPU, 4GB RAM
- **Total**: ~10 CPU, 20GB RAM minimum
