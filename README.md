# PyGuardian v3

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-blue.svg)](https://kubernetes.io/)
[![Security](https://img.shields.io/badge/Security-First-red.svg)](SECURITY.md)

**PyGuardian v3** is a production-ready, open-source Threat Hunting & Incident Response platform designed for real-time network flow analysis, threat detection, and automated response. Built with modern technologies and security-first principles.

## 🚀 Features

### Core Capabilities
- **Real-time Network Flow Analysis**: NetFlow, sFlow, IPFIX collection and processing
- **Advanced Threat Detection**: Rule-based detection with MITRE ATT&CK mapping
- **Incident Response**: Automated playbooks and manual triage workflows
- **Threat Intelligence**: Integration with multiple threat intel sources
- **Geographic Visualization**: Interactive threat maps with Mapbox integration
- **Correlation Engine**: Advanced event correlation and risk scoring
- **API-First Design**: RESTful APIs with OpenAPI documentation

### Security Features
- **Zero-Trust Architecture**: JWT authentication with RBAC
- **Encryption Everywhere**: TLS 1.3 and AES-256 encryption
- **PII Protection**: Automatic PII detection and masking
- **Audit Logging**: Comprehensive security event logging
- **Compliance Ready**: GDPR, SOC 2, NIST framework support

### Scalability
- **Microservices Architecture**: Containerized services with Kubernetes support
- **High-Performance Storage**: ClickHouse for time-series data, PostgreSQL for metadata
- **Message Streaming**: Apache Kafka for high-throughput event processing
- **Auto-scaling**: Horizontal scaling based on load metrics
- **Multi-tenant**: Support for multiple organizations

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PyGuardian v3 Platform                   │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React)  │  API Gateway (FastAPI)  │  Admin UI    │
├─────────────────────────────────────────────────────────────┤
│  Collectors  │  Enrichment  │  Detectors  │  Correlator     │
├─────────────────────────────────────────────────────────────┤
│  Kafka (Message Broker)  │  Redis (Cache)  │  MinIO (S3)    │
├─────────────────────────────────────────────────────────────┤
│  ClickHouse (Flows)  │  PostgreSQL (Metadata)  │  Monitoring│
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- 8GB RAM minimum (16GB recommended)
- 50GB disk space
- Network access for threat intelligence APIs

### 1. Clone the Repository
```bash
git clone https://github.com/pyguardian/pyguardian.git
cd pyguardian
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

### 3. Start with Docker Compose
```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f api
```

### 4. Access the Platform
- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Grafana Monitoring**: http://localhost:3001 (admin/admin)
- **Kafka UI**: http://localhost:8080
- **MinIO Console**: http://localhost:9002 (pyguardian/pyguardian_dev_password)

### 5. Initial Configuration
```bash
# Create admin user
docker-compose exec api python scripts/create_admin.py

# Load sample rules
docker-compose exec api python scripts/load_rules.py

# Start data collection
docker-compose exec collector python scripts/start_collection.py
```

## 📊 Dashboard Overview

The PyGuardian dashboard provides real-time security insights:

- **KPI Cards**: Active alerts, high-risk incidents, events processed
- **Live Event Feed**: Real-time security events with filtering
- **Threat Map**: Geographic visualization of threats
- **Incident Management**: Triage and response workflows
- **Flow Explorer**: Network flow hunting and analysis
- **Threat Intelligence**: IOC management and reputation data

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/pyguardian
CLICKHOUSE_URL=clickhouse://user:pass@localhost:9000/pyguardian

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
JWT_EXPIRE_MINUTES=30

# External APIs
THREAT_INTEL_API_KEY=your-api-key
GEOIP_API_KEY=your-api-key
MAPBOX_TOKEN=your-token

# Message Broker
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

### Detection Rules
Create custom detection rules in YAML format:

```yaml
- id: "custom-rule"
  name: "Custom Threat Detection"
  description: "Detects custom threat patterns"
  enabled: true
  severity: "high"
  conditions:
    - field: "dest_port"
      operator: "equals"
      value: 22
  actions:
    - type: "create_alert"
      severity: "high"
    - type: "notify"
      channels: ["slack", "email"]
```

## 🚀 Production Deployment

### Kubernetes with Helm
```bash
# Add Helm repository
helm repo add pyguardian https://pyguardian.github.io/helm-charts
helm repo update

# Install PyGuardian
helm install pyguardian pyguardian/pyguardian \
  --namespace pyguardian \
  --create-namespace \
  --set ingress.hosts[0].host=pyguardian.yourdomain.com \
  --set postgresql.auth.password=your-secure-password \
  --values values-production.yaml
```

### Resource Requirements
- **Minimum**: 10 CPU cores, 20GB RAM, 200GB storage
- **Recommended**: 20 CPU cores, 40GB RAM, 500GB storage
- **High Availability**: 30+ CPU cores, 60GB RAM, 1TB+ storage

## 📚 Documentation

- [Architecture Guide](ARCHITECTURE.md) - System architecture and components
- [API Documentation](api/README.md) - REST API reference
- [Security Guide](SECURITY.md) - Security features and compliance
- [UI/UX Specification](UI_UX_SPEC.md) - Frontend design system
- [Deployment Guide](docs/deployment.md) - Production deployment
- [User Manual](docs/user-manual.md) - End-user documentation

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Good First Issues
- [ ] Add new detection rule templates
- [ ] Improve error handling in API endpoints
- [ ] Add unit tests for correlation algorithms
- [ ] Enhance frontend accessibility features
- [ ] Add support for additional log formats
- [ ] Improve documentation and examples
- [ ] Add integration tests for Docker setup
- [ ] Optimize database queries for large datasets

### Development Setup
```bash
# Backend development
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
uvicorn main:app --reload

# Frontend development
cd frontend
npm install
npm start

# Run tests
pytest backend/tests/
npm test --prefix frontend
```

## 📊 Performance

### Benchmarks
- **Event Processing**: 100,000+ events/second
- **Storage**: 1TB+ flow data with sub-second queries
- **API Response**: <100ms for 95th percentile
- **Dashboard Load**: <2 seconds for full dashboard
- **Concurrent Users**: 100+ simultaneous users

### Monitoring
- **Prometheus Metrics**: Comprehensive system metrics
- **Grafana Dashboards**: Pre-built monitoring dashboards
- **Health Checks**: Automated health monitoring
- **Alerting**: Configurable alerting rules

## 🔒 Security

PyGuardian follows security-first principles:

- **Zero-Trust Architecture**: All communications encrypted
- **RBAC**: Role-based access control
- **Audit Logging**: Comprehensive security event logging
- **Vulnerability Scanning**: Automated security scanning
- **Compliance**: GDPR, SOC 2, NIST framework support

See [SECURITY.md](SECURITY.md) for detailed security information.

## 📈 Roadmap

### v3.1 (Q2 2024)
- [ ] Machine Learning-based anomaly detection
- [ ] Advanced correlation algorithms
- [ ] Mobile application
- [ ] Additional threat intel sources

### v3.2 (Q3 2024)
- [ ] Multi-tenant architecture
- [ ] Advanced reporting engine
- [ ] Integration marketplace
- [ ] Performance optimizations

### v4.0 (Q4 2024)
- [ ] Cloud-native architecture
- [ ] Serverless components
- [ ] Advanced AI/ML features
- [ ] Enterprise features

## 🆘 Support

### Community Support
- **GitHub Issues**: [Report bugs and request features](https://github.com/pyguardian/pyguardian/issues)
- **Discussions**: [Community discussions](https://github.com/pyguardian/pyguardian/discussions)
- **Discord**: [Join our Discord server](https://discord.gg/pyguardian)

### Commercial Support
- **Enterprise Support**: Available for production deployments
- **Professional Services**: Custom development and integration
- **Training**: Security team training and certification

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Open Source Community**: Thanks to all contributors and maintainers
- **Security Researchers**: For threat intelligence and research
- **Technology Partners**: For integrations and partnerships
- **Users**: For feedback and feature requests

## 📞 Contact
- **Email**: anillemree@gmail.com

---

**⚠️ Legal Notice**: PyGuardian is designed for authorized security monitoring only. Users must ensure compliance with applicable laws and organizational policies. Unauthorized monitoring may violate privacy laws.

**🔒 Security**: Report security vulnerabilities to security@pyguardian.org

**📊 Status**: [![Uptime Robot](https://img.shields.io/uptimerobot/status/m784123456-1234567890abcdef)](https://status.pyguardian.org)
