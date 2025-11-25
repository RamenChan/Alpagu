"""
Database models for PyGuardian Home Edition
"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid


def generate_uuid():
    """Generate UUID string"""
    return str(uuid.uuid4())


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    alerts = relationship("Alert", back_populates="user")
    notification_settings = relationship("NotificationSettings", back_populates="user", uselist=False)


class Alert(Base):
    """Alert model for detected anomalies"""
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String, nullable=False)  # low, medium, high, critical
    status = Column(String, default="new")  # new, acknowledged, resolved, false_positive
    source_ip = Column(String, nullable=True)
    dest_ip = Column(String, nullable=True)
    source_port = Column(Integer, nullable=True)
    dest_port = Column(Integer, nullable=True)
    protocol = Column(String, nullable=True)
    risk_score = Column(Float, default=0.0)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="alerts")


class NotificationSettings(Base):
    """User notification settings"""
    __tablename__ = "notification_settings"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Email notifications
    email_enabled = Column(Boolean, default=True)
    email_address = Column(String, nullable=True)
    
    # Webhook notifications
    webhook_enabled = Column(Boolean, default=False)
    webhook_url = Column(String, nullable=True)
    
    # Notification preferences
    notify_on_critical = Column(Boolean, default=True)
    notify_on_high = Column(Boolean, default=True)
    notify_on_medium = Column(Boolean, default=False)
    notify_on_low = Column(Boolean, default=False)
    
    # Quiet hours (no notifications during these hours)
    quiet_hours_enabled = Column(Boolean, default=False)
    quiet_hours_start = Column(Integer, default=22)  # 22:00
    quiet_hours_end = Column(Integer, default=8)    # 08:00
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notification_settings")

