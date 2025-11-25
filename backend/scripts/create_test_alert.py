"""
Test alert oluşturma script'i
Ev kullanıcıları için örnek alert'ler oluşturur
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import User, Alert

def create_test_alerts():
    """Create test alerts for all users"""
    db = SessionLocal()
    
    try:
        # Get all users
        users = db.query(User).all()
        
        if not users:
            print("No users found. Please create a user account first.")
            return
        
        # Sample alerts
        test_alerts = [
            {
                "title": "Suspicious Port Scan Detected",
                "description": "Multiple connection attempts detected on port 22 (SSH) from external IP 203.0.113.45",
                "severity": "high",
                "source_ip": "203.0.113.45",
                "dest_ip": "192.168.1.100",
                "dest_port": 22,
                "protocol": "TCP",
                "risk_score": 75.5
            },
            {
                "title": "Unusual Outbound Traffic",
                "description": "Large amount of data transferred to unknown external IP 198.51.100.42",
                "severity": "medium",
                "source_ip": "192.168.1.50",
                "dest_ip": "198.51.100.42",
                "dest_port": 443,
                "protocol": "TCP",
                "risk_score": 60.0
            },
            {
                "title": "Potential Malware Communication",
                "description": "Connection to known malicious domain detected: malware.example.com",
                "severity": "critical",
                "source_ip": "192.168.1.75",
                "dest_ip": "203.0.113.100",
                "dest_port": 80,
                "protocol": "TCP",
                "risk_score": 90.0
            },
            {
                "title": "Brute Force Attempt",
                "description": "Multiple failed login attempts detected on port 3389 (RDP)",
                "severity": "high",
                "source_ip": "203.0.113.200",
                "dest_ip": "192.168.1.25",
                "dest_port": 3389,
                "protocol": "TCP",
                "risk_score": 80.0
            },
            {
                "title": "Unusual DNS Query Pattern",
                "description": "Unusual DNS query pattern detected, possible data exfiltration attempt",
                "severity": "medium",
                "source_ip": "192.168.1.100",
                "dest_ip": "8.8.8.8",
                "dest_port": 53,
                "protocol": "UDP",
                "risk_score": 55.0
            }
        ]
        
        # Create alerts for each user
        for user in users:
            print(f"Creating test alerts for user: {user.email}")
            
            for alert_data in test_alerts:
                alert = Alert(
                    user_id=user.id,
                    title=alert_data["title"],
                    description=alert_data["description"],
                    severity=alert_data["severity"],
                    status="new",
                    source_ip=alert_data["source_ip"],
                    dest_ip=alert_data["dest_ip"],
                    dest_port=alert_data["dest_port"],
                    protocol=alert_data["protocol"],
                    risk_score=alert_data["risk_score"]
                )
                db.add(alert)
            
            db.commit()
            print(f"Created {len(test_alerts)} test alerts for {user.email}")
        
        print("\nTest alerts created successfully!")
        
    except Exception as e:
        print(f"Error creating test alerts: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_alerts()

