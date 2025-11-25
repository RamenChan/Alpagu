"""
Dashboard endpoints for home users
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from pydantic import BaseModel
from datetime import datetime, timedelta
from main import get_current_user
from database import get_db
from models import User, Alert

router = APIRouter()


class DashboardKPIs(BaseModel):
    total_alerts: int
    new_alerts: int
    critical_alerts: int
    high_alerts: int
    alerts_today: int
    alerts_this_week: int


class RecentAlert(BaseModel):
    id: str
    title: str
    severity: str
    created_at: datetime


class DashboardResponse(BaseModel):
    kpis: DashboardKPIs
    recent_alerts: list[RecentAlert]


@router.get("/", response_model=DashboardResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard data for current user"""
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = now - timedelta(days=7)
    
    # Get KPIs
    total_alerts = db.query(Alert).filter(Alert.user_id == current_user.id).count()
    new_alerts = db.query(Alert).filter(
        and_(
            Alert.user_id == current_user.id,
            Alert.status == "new"
        )
    ).count()
    critical_alerts = db.query(Alert).filter(
        and_(
            Alert.user_id == current_user.id,
            Alert.severity == "critical"
        )
    ).count()
    high_alerts = db.query(Alert).filter(
        and_(
            Alert.user_id == current_user.id,
            Alert.severity == "high"
        )
    ).count()
    alerts_today = db.query(Alert).filter(
        and_(
            Alert.user_id == current_user.id,
            Alert.created_at >= today_start
        )
    ).count()
    alerts_this_week = db.query(Alert).filter(
        and_(
            Alert.user_id == current_user.id,
            Alert.created_at >= week_start
        )
    ).count()
    
    # Get recent alerts
    recent_alerts = db.query(Alert).filter(
        Alert.user_id == current_user.id
    ).order_by(Alert.created_at.desc()).limit(10).all()
    
    return {
        "kpis": {
            "total_alerts": total_alerts,
            "new_alerts": new_alerts,
            "critical_alerts": critical_alerts,
            "high_alerts": high_alerts,
            "alerts_today": alerts_today,
            "alerts_this_week": alerts_this_week
        },
        "recent_alerts": [
            {
                "id": alert.id,
                "title": alert.title,
                "severity": alert.severity,
                "created_at": alert.created_at
            }
            for alert in recent_alerts
        ]
    }

