# PyGuardian v3 - FastAPI Endpoints Specification

from fastapi import APIRouter, Depends, Query, Path, Body, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from enum import Enum

# Authentication and Authorization
security = HTTPBearer()

# Router definitions
alerts_router = APIRouter(prefix="/api/alerts", tags=["alerts"])
incidents_router = APIRouter(prefix="/api/incidents", tags=["incidents"])
flows_router = APIRouter(prefix="/api/flows", tags=["flows"])
enrich_router = APIRouter(prefix="/api/enrich", tags=["enrichment"])
rules_router = APIRouter(prefix="/api/rules", tags=["rules"])
users_router = APIRouter(prefix="/api/users", tags=["users"])
dashboard_router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])
threat_intel_router = APIRouter(prefix="/api/threat-intel", tags=["threat-intel"])

# Request/Response Models
class AlertResponse(BaseModel):
    alert_id: str
    timestamp: datetime
    rule_id: str
    rule_name: str
    severity: str
    status: str
    source_events: List[str]
    description: str
    mitre_attack: Dict[str, List[str]]
    risk_score: float
    affected_assets: List[str]
    indicators: Dict[str, List[str]]
    context: Dict[str, Any]
    assigned_to: Optional[str]
    created_by: str
    tags: List[str]

class IncidentResponse(BaseModel):
    incident_id: str
    title: str
    description: str
    status: str
    priority: str
    severity: str
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]
    assigned_to: Optional[str]
    created_by: str
    source_alerts: List[str]
    mitre_attack: Dict[str, List[str]]
    risk_score: float
    affected_assets: List[str]
    indicators: Dict[str, List[str]]
    timeline: List[Dict[str, Any]]
    playbooks: List[Dict[str, Any]]
    tags: List[str]
    notes: List[Dict[str, Any]]

class FlowResponse(BaseModel):
    event_id: str
    timestamp: datetime
    collector_id: str
    source_ip: str
    dest_ip: str
    source_port: int
    dest_port: int
    protocol: int
    bytes_sent: int
    bytes_received: int
    packets_sent: int
    packets_received: int
    duration: int
    tcp_flags: int
    tos: int
    enrichment: Dict[str, Any]
    raw_data: Dict[str, Any]

class EnrichmentRequest(BaseModel):
    indicators: List[str]
    types: List[str] = Field(..., description="Types: ip, domain, hash, url")

class EnrichmentResponse(BaseModel):
    results: Dict[str, Dict[str, Any]]

class RuleResponse(BaseModel):
    rule_id: str
    name: str
    description: str
    enabled: bool
    severity: str
    category: str
    conditions: List[Dict[str, Any]]
    aggregation: Dict[str, Any]
    mitre_attack: Dict[str, List[str]]
    actions: List[Dict[str, Any]]
    tags: List[str]
    created_by: str
    created_at: datetime
    updated_at: datetime

class DashboardKPIs(BaseModel):
    active_alerts: int
    high_risk_incidents: int
    events_today: int
    assets_monitored: int
    threats_blocked: int
    false_positives: int

class PaginatedResponse(BaseModel):
    data: List[Any]
    total: int
    page: int
    per_page: int
    total_pages: int

# Query Parameters
class AlertFilters(BaseModel):
    status: Optional[List[str]] = None
    severity: Optional[List[str]] = None
    assigned_to: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    tags: Optional[List[str]] = None
    search: Optional[str] = None

class FlowFilters(BaseModel):
    source_ip: Optional[str] = None
    dest_ip: Optional[str] = None
    source_port: Optional[int] = None
    dest_port: Optional[int] = None
    protocol: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    country: Optional[str] = None
    min_bytes: Optional[int] = None
    max_bytes: Optional[int] = None

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Implement JWT token validation
    # Return user object or raise HTTPException
    pass

# ALERTS ENDPOINTS

@alerts_router.get("/", response_model=PaginatedResponse)
async def get_alerts(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=1000),
    status: Optional[List[str]] = Query(None),
    severity: Optional[List[str]] = Query(None),
    assigned_to: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    tags: Optional[List[str]] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("timestamp"),
    sort_order: str = Query("desc"),
    current_user = Depends(get_current_user)
):
    """
    Get paginated list of alerts with filtering options
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 50, max: 1000)
    - status: Filter by alert status (new, investigating, resolved, false_positive)
    - severity: Filter by severity (low, medium, high, critical)
    - assigned_to: Filter by assigned user ID
    - date_from: Start date filter (ISO 8601)
    - date_to: End date filter (ISO 8601)
    - tags: Filter by tags
    - search: Search in description and rule name
    - sort_by: Sort field (timestamp, severity, risk_score)
    - sort_order: Sort direction (asc, desc)
    """
    pass

@alerts_router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: str = Path(..., description="Alert ID"),
    current_user = Depends(get_current_user)
):
    """
    Get specific alert by ID
    """
    pass

@alerts_router.patch("/{alert_id}/status")
async def update_alert_status(
    alert_id: str = Path(..., description="Alert ID"),
    status: str = Body(..., description="New status"),
    current_user = Depends(get_current_user)
):
    """
    Update alert status
    """
    pass

@alerts_router.patch("/{alert_id}/assign")
async def assign_alert(
    alert_id: str = Path(..., description="Alert ID"),
    user_id: str = Body(..., description="User ID to assign to"),
    current_user = Depends(get_current_user)
):
    """
    Assign alert to user
    """
    pass

@alerts_router.post("/{alert_id}/create-incident")
async def create_incident_from_alert(
    alert_id: str = Path(..., description="Alert ID"),
    priority: str = Body(..., description="Incident priority"),
    current_user = Depends(get_current_user)
):
    """
    Create incident from alert
    """
    pass

# INCIDENTS ENDPOINTS

@incidents_router.get("/", response_model=PaginatedResponse)
async def get_incidents(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=1000),
    status: Optional[List[str]] = Query(None),
    priority: Optional[List[str]] = Query(None),
    severity: Optional[List[str]] = Query(None),
    assigned_to: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    tags: Optional[List[str]] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    current_user = Depends(get_current_user)
):
    """
    Get paginated list of incidents with filtering options
    """
    pass

@incidents_router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident(
    incident_id: str = Path(..., description="Incident ID"),
    current_user = Depends(get_current_user)
):
    """
    Get specific incident by ID
    """
    pass

@incidents_router.post("/", response_model=IncidentResponse)
async def create_incident(
    title: str = Body(..., description="Incident title"),
    description: str = Body(..., description="Incident description"),
    priority: str = Body(..., description="Incident priority"),
    severity: str = Body(..., description="Incident severity"),
    source_alerts: Optional[List[str]] = Body(None, description="Source alert IDs"),
    tags: Optional[List[str]] = Body(None, description="Incident tags"),
    current_user = Depends(get_current_user)
):
    """
    Create new incident
    """
    pass

@incidents_router.patch("/{incident_id}")
async def update_incident(
    incident_id: str = Path(..., description="Incident ID"),
    updates: Dict[str, Any] = Body(..., description="Incident updates"),
    current_user = Depends(get_current_user)
):
    """
    Update incident
    """
    pass

@incidents_router.post("/{incident_id}/notes")
async def add_incident_note(
    incident_id: str = Path(..., description="Incident ID"),
    content: str = Body(..., description="Note content"),
    note_type: str = Body("note", description="Note type"),
    current_user = Depends(get_current_user)
):
    """
    Add note to incident
    """
    pass

@incidents_router.post("/{incident_id}/playbooks/{playbook_id}/run")
async def run_playbook(
    incident_id: str = Path(..., description="Incident ID"),
    playbook_id: str = Path(..., description="Playbook ID"),
    parameters: Optional[Dict[str, Any]] = Body(None, description="Playbook parameters"),
    current_user = Depends(get_current_user)
):
    """
    Run playbook on incident
    """
    pass

# FLOWS ENDPOINTS

@flows_router.get("/", response_model=PaginatedResponse)
async def get_flows(
    page: int = Query(1, ge=1),
    per_page: int = Query(100, ge=1, le=10000),
    source_ip: Optional[str] = Query(None, description="Source IP filter"),
    dest_ip: Optional[str] = Query(None, description="Destination IP filter"),
    source_port: Optional[int] = Query(None, description="Source port filter"),
    dest_port: Optional[int] = Query(None, description="Destination port filter"),
    protocol: Optional[int] = Query(None, description="Protocol filter (1=ICMP, 6=TCP, 17=UDP)"),
    date_from: Optional[datetime] = Query(None, description="Start date filter"),
    date_to: Optional[datetime] = Query(None, description="End date filter"),
    country: Optional[str] = Query(None, description="Country filter"),
    min_bytes: Optional[int] = Query(None, description="Minimum bytes filter"),
    max_bytes: Optional[int] = Query(None, description="Maximum bytes filter"),
    sort_by: str = Query("timestamp"),
    sort_order: str = Query("desc"),
    current_user = Depends(get_current_user)
):
    """
    Get paginated list of network flows with filtering options
    
    Example Response:
    {
        "data": [
            {
                "event_id": "550e8400-e29b-41d4-a716-446655440000",
                "timestamp": "2024-01-15T10:30:45.123Z",
                "collector_id": "netflow-collector-01",
                "source_ip": "192.168.1.100",
                "dest_ip": "203.0.113.45",
                "source_port": 45678,
                "dest_port": 22,
                "protocol": 6,
                "bytes_sent": 1024,
                "bytes_received": 2048,
                "packets_sent": 15,
                "packets_received": 12,
                "duration": 30,
                "tcp_flags": 18,
                "tos": 0,
                "enrichment": {
                    "source_asset": {
                        "hostname": "workstation-001",
                        "criticality": "medium"
                    },
                    "geolocation": {
                        "source": {"country": "United States"},
                        "dest": {"country": "China"}
                    },
                    "threat_intel": {
                        "dest_reputation": {
                            "score": -45,
                            "categories": ["malware", "botnet"]
                        }
                    }
                },
                "raw_data": {}
            }
        ],
        "total": 45231,
        "page": 1,
        "per_page": 100,
        "total_pages": 453
    }
    """
    pass

@flows_router.get("/{flow_id}", response_model=FlowResponse)
async def get_flow(
    flow_id: str = Path(..., description="Flow ID"),
    current_user = Depends(get_current_user)
):
    """
    Get specific flow by ID
    """
    pass

@flows_router.get("/stats/summary")
async def get_flow_stats(
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    group_by: str = Query("hour", description="Group by: hour, day, week"),
    current_user = Depends(get_current_user)
):
    """
    Get flow statistics summary
    """
    pass

@flows_router.get("/stats/top-ips")
async def get_top_ips(
    limit: int = Query(10, ge=1, le=100),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    current_user = Depends(get_current_user)
):
    """
    Get top IP addresses by flow count
    """
    pass

# ENRICHMENT ENDPOINTS

@enrich_router.post("/", response_model=EnrichmentResponse)
async def enrich_indicators(
    request: EnrichmentRequest,
    current_user = Depends(get_current_user)
):
    """
    Enrich indicators with threat intelligence
    
    Request Body:
    {
        "indicators": ["203.0.113.45", "malware.example.com"],
        "types": ["ip", "domain"]
    }
    
    Response:
    {
        "results": {
            "203.0.113.45": {
                "reputation_score": -45,
                "categories": ["malware", "botnet"],
                "sources": ["abuse_ch", "virustotal"],
                "last_updated": "2024-01-15T08:30:00Z"
            },
            "malware.example.com": {
                "reputation_score": -80,
                "categories": ["malware", "phishing"],
                "sources": ["virustotal", "phishtank"],
                "last_updated": "2024-01-15T09:15:00Z"
            }
        }
    }
    """
    pass

@enrich_router.get("/sources")
async def get_enrichment_sources(
    current_user = Depends(get_current_user)
):
    """
    Get available enrichment sources
    """
    pass

# RULES ENDPOINTS

@rules_router.get("/", response_model=List[RuleResponse])
async def get_rules(
    enabled: Optional[bool] = Query(None),
    category: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    current_user = Depends(get_current_user)
):
    """
    Get detection rules
    """
    pass

@rules_router.get("/{rule_id}", response_model=RuleResponse)
async def get_rule(
    rule_id: str = Path(..., description="Rule ID"),
    current_user = Depends(get_current_user)
):
    """
    Get specific rule by ID
    """
    pass

@rules_router.post("/", response_model=RuleResponse)
async def create_rule(
    rule: Dict[str, Any] = Body(..., description="Rule definition"),
    current_user = Depends(get_current_user)
):
    """
    Create new detection rule
    """
    pass

@rules_router.patch("/{rule_id}")
async def update_rule(
    rule_id: str = Path(..., description="Rule ID"),
    updates: Dict[str, Any] = Body(..., description="Rule updates"),
    current_user = Depends(get_current_user)
):
    """
    Update detection rule
    """
    pass

@rules_router.delete("/{rule_id}")
async def delete_rule(
    rule_id: str = Path(..., description="Rule ID"),
    current_user = Depends(get_current_user)
):
    """
    Delete detection rule
    """
    pass

@rules_router.post("/{rule_id}/test")
async def test_rule(
    rule_id: str = Path(..., description="Rule ID"),
    test_data: Optional[Dict[str, Any]] = Body(None, description="Test data"),
    current_user = Depends(get_current_user)
):
    """
    Test detection rule with sample data
    """
    pass

# DASHBOARD ENDPOINTS

@dashboard_router.get("/kpis", response_model=DashboardKPIs)
async def get_dashboard_kpis(
    current_user = Depends(get_current_user)
):
    """
    Get dashboard KPIs
    
    Response:
    {
        "active_alerts": 12,
        "high_risk_incidents": 3,
        "events_today": 45231,
        "assets_monitored": 1247,
        "threats_blocked": 45,
        "false_positives": 8
    }
    """
    pass

@dashboard_router.get("/live-events")
async def get_live_events(
    limit: int = Query(50, ge=1, le=1000),
    severity: Optional[List[str]] = Query(None),
    current_user = Depends(get_current_user)
):
    """
    Get live events for dashboard feed
    """
    pass

@dashboard_router.get("/threat-map")
async def get_threat_map_data(
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    current_user = Depends(get_current_user)
):
    """
    Get threat map data for geographic visualization
    """
    pass

@dashboard_router.get("/top-threats")
async def get_top_threats(
    limit: int = Query(10, ge=1, le=50),
    period: str = Query("24h", description="Time period: 1h, 24h, 7d, 30d"),
    current_user = Depends(get_current_user)
):
    """
    Get top threats by MITRE ATT&CK technique
    """
    pass

# THREAT INTELLIGENCE ENDPOINTS

@threat_intel_router.get("/sources")
async def get_threat_intel_sources(
    current_user = Depends(get_current_user)
):
    """
    Get threat intelligence sources
    """
    pass

@threat_intel_router.get("/indicators")
async def get_threat_indicators(
    type: Optional[str] = Query(None, description="Indicator type: ip, domain, hash, url"),
    category: Optional[str] = Query(None, description="Threat category"),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_user)
):
    """
    Get threat intelligence indicators
    """
    pass

@threat_intel_router.post("/indicators")
async def add_threat_indicator(
    indicator: str = Body(..., description="Indicator value"),
    type: str = Body(..., description="Indicator type"),
    category: str = Body(..., description="Threat category"),
    reputation_score: int = Body(..., description="Reputation score (-100 to 100)"),
    sources: List[str] = Body(..., description="Source names"),
    current_user = Depends(get_current_user)
):
    """
    Add threat intelligence indicator
    """
    pass

# WEBSOCKET ENDPOINTS

@alerts_router.websocket("/ws")
async def websocket_alerts(websocket: WebSocket):
    """
    WebSocket endpoint for real-time alert updates
    """
    pass

@incidents_router.websocket("/ws")
async def websocket_incidents(websocket: WebSocket):
    """
    WebSocket endpoint for real-time incident updates
    """
    pass

@flows_router.websocket("/ws")
async def websocket_flows(websocket: WebSocket):
    """
    WebSocket endpoint for real-time flow updates
    """
    pass

# Error Handling Examples

class APIError(BaseModel):
    message: str
    code: str
    details: Optional[Dict[str, Any]] = None

# Common HTTP status codes and error responses:
# 200: Success
# 201: Created
# 400: Bad Request
# 401: Unauthorized
# 403: Forbidden
# 404: Not Found
# 422: Validation Error
# 500: Internal Server Error

# Example error response:
# {
#     "message": "Validation error",
#     "code": "VALIDATION_ERROR",
#     "details": {
#         "field": "email",
#         "error": "Invalid email format"
#     }
# }
