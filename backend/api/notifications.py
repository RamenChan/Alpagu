"""
Notification settings and sending endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from main import get_current_user
from database import get_db
from models import User, NotificationSettings, Alert
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime


router = APIRouter()


class NotificationSettingsResponse(BaseModel):
    id: str
    email_enabled: bool
    email_address: Optional[str]
    webhook_enabled: bool
    webhook_url: Optional[str]
    notify_on_critical: bool
    notify_on_high: bool
    notify_on_medium: bool
    notify_on_low: bool
    quiet_hours_enabled: bool
    quiet_hours_start: int
    quiet_hours_end: int
    
    class Config:
        from_attributes = True


class NotificationSettingsUpdate(BaseModel):
    email_enabled: Optional[bool] = None
    email_address: Optional[EmailStr] = None
    webhook_enabled: Optional[bool] = None
    webhook_url: Optional[str] = None
    notify_on_critical: Optional[bool] = None
    notify_on_high: Optional[bool] = None
    notify_on_medium: Optional[bool] = None
    notify_on_low: Optional[bool] = None
    quiet_hours_enabled: Optional[bool] = None
    quiet_hours_start: Optional[int] = None
    quiet_hours_end: Optional[int] = None


@router.get("/settings", response_model=NotificationSettingsResponse)
async def get_notification_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user notification settings"""
    settings = db.query(NotificationSettings).filter(
        NotificationSettings.user_id == current_user.id
    ).first()
    
    if not settings:
        # Create default settings
        settings = NotificationSettings(
            user_id=current_user.id,
            email_enabled=True,
            email_address=current_user.email
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    return settings


@router.patch("/settings", response_model=NotificationSettingsResponse)
async def update_notification_settings(
    request: NotificationSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user notification settings"""
    settings = db.query(NotificationSettings).filter(
        NotificationSettings.user_id == current_user.id
    ).first()
    
    if not settings:
        settings = NotificationSettings(user_id=current_user.id)
        db.add(settings)
    
    # Update fields
    for field, value in request.dict(exclude_unset=True).items():
        setattr(settings, field, value)
    
    db.commit()
    db.refresh(settings)
    return settings


def send_email_notification(settings: NotificationSettings, alert: Alert):
    """Send email notification for alert"""
    if not settings.email_enabled or not settings.email_address:
        return
    
    # Check quiet hours
    if settings.quiet_hours_enabled:
        current_hour = datetime.utcnow().hour
        if settings.quiet_hours_start > settings.quiet_hours_end:
            # Quiet hours span midnight
            if current_hour >= settings.quiet_hours_start or current_hour < settings.quiet_hours_end:
                return
        else:
            if settings.quiet_hours_start <= current_hour < settings.quiet_hours_end:
                return
    
    # Check severity preferences
    if alert.severity == "critical" and not settings.notify_on_critical:
        return
    if alert.severity == "high" and not settings.notify_on_high:
        return
    if alert.severity == "medium" and not settings.notify_on_medium:
        return
    if alert.severity == "low" and not settings.notify_on_low:
        return
    
    # Send email (simplified - should use proper email service in production)
    try:
        # This is a placeholder - should use proper SMTP or email service
        # For production, use services like SendGrid, AWS SES, etc.
        msg = MIMEMultipart()
        msg['From'] = "noreply@pyguardian.local"
        msg['To'] = settings.email_address
        msg['Subject'] = f"PyGuardian Alert: {alert.title}"
        
        body = f"""
        New Security Alert Detected
        
        Title: {alert.title}
        Description: {alert.description}
        Severity: {alert.severity.upper()}
        Risk Score: {alert.risk_score}
        
        Source IP: {alert.source_ip or 'N/A'}
        Destination IP: {alert.dest_ip or 'N/A'}
        
        Please log in to your PyGuardian dashboard to view details.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Note: In production, configure proper SMTP settings
        # For now, this is a placeholder
        print(f"Would send email to {settings.email_address}: {alert.title}")
        
    except Exception as e:
        print(f"Error sending email notification: {e}")


def send_webhook_notification(settings: NotificationSettings, alert: Alert):
    """Send webhook notification for alert"""
    if not settings.webhook_enabled or not settings.webhook_url:
        return
    
    # Check quiet hours
    if settings.quiet_hours_enabled:
        current_hour = datetime.utcnow().hour
        if settings.quiet_hours_start > settings.quiet_hours_end:
            if current_hour >= settings.quiet_hours_start or current_hour < settings.quiet_hours_end:
                return
        else:
            if settings.quiet_hours_start <= current_hour < settings.quiet_hours_end:
                return
    
    # Check severity preferences
    if alert.severity == "critical" and not settings.notify_on_critical:
        return
    if alert.severity == "high" and not settings.notify_on_high:
        return
    if alert.severity == "medium" and not settings.notify_on_medium:
        return
    if alert.severity == "low" and not settings.notify_on_low:
        return
    
    # Send webhook
    try:
        payload = {
            "alert_id": alert.id,
            "title": alert.title,
            "description": alert.description,
            "severity": alert.severity,
            "risk_score": alert.risk_score,
            "source_ip": alert.source_ip,
            "dest_ip": alert.dest_ip,
            "created_at": alert.created_at.isoformat()
        }
        
        response = requests.post(
            settings.webhook_url,
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        
    except Exception as e:
        print(f"Error sending webhook notification: {e}")


def notify_user(user_id: str, alert: Alert, db: Session):
    """Notify user about new alert"""
    settings = db.query(NotificationSettings).filter(
        NotificationSettings.user_id == user_id
    ).first()
    
    if not settings:
        return
    
    # Send email notification
    send_email_notification(settings, alert)
    
    # Send webhook notification
    send_webhook_notification(settings, alert)

