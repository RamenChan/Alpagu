"""
Alerts endpoints for home users
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..main import get_current_user
from ..database import get_db
from ..models import User, Alert

router = APIRouter()


class AlertResponse(BaseModel):
    id: str
    title: str
    description: str
    severity: str
    status: str
    source_ip: Optional[str]
    dest_ip: Optional[str]
    source_port: Optional[int]
    dest_port: Optional[int]
    protocol: Optional[str]
    risk_score: float
    created_at: datetime
    updated_at: datetime
    acknowledged_at: Optional[datetime]
    resolved_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class AlertUpdateRequest(BaseModel):
    status: Optional[str] = None


class PaginatedAlertsResponse(BaseModel):
    data: List[AlertResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


@router.get("/", response_model=PaginatedAlertsResponse)
async def get_alerts(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's alerts with pagination"""
    query = db.query(Alert).filter(Alert.user_id == current_user.id)
    
    # Apply filters
    if status:
        query = query.filter(Alert.status == status)
    if severity:
        query = query.filter(Alert.severity == severity)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    alerts = query.order_by(desc(Alert.created_at)).offset((page - 1) * per_page).limit(per_page).all()
    
    total_pages = (total + per_page - 1) // per_page
    
    return {
        "data": alerts,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages
    }


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific alert by ID"""
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return alert


@router.patch("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: str,
    request: AlertUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update alert status"""
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    if request.status:
        valid_statuses = ["new", "acknowledged", "resolved", "false_positive"]
        if request.status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        
        alert.status = request.status
        
        if request.status == "acknowledged":
            alert.acknowledged_at = datetime.utcnow()
        elif request.status == "resolved":
            alert.resolved_at = datetime.utcnow()
    
    db.commit()
    db.refresh(alert)
    return alert


@router.get("/stats/summary")
async def get_alert_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get alert statistics for current user"""
    total = db.query(Alert).filter(Alert.user_id == current_user.id).count()
    new_count = db.query(Alert).filter(
        Alert.user_id == current_user.id,
        Alert.status == "new"
    ).count()
    critical_count = db.query(Alert).filter(
        Alert.user_id == current_user.id,
        Alert.severity == "critical"
    ).count()
    high_count = db.query(Alert).filter(
        Alert.user_id == current_user.id,
        Alert.severity == "high"
    ).count()
    
    return {
        "total": total,
        "new": new_count,
        "critical": critical_count,
        "high": high_count
    }

