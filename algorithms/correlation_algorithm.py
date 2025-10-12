# PyGuardian v3 - Correlation and Incident Scoring Algorithm
# Pseudo-code for risk scoring and MITRE ATT&CK mapping

from __future__ import annotations

from typing import List
from dataclasses import dataclass
from datetime import datetime

class CorrelationEngine:
    """
    Advanced correlation engine for threat detection and incident scoring
    """
    
    def __init__(self):
        self.mitre_attack_db = {}
        self.threat_intel_sources = {}
        self.asset_criticality_weights = {
            'critical': 1.0,
            'high': 0.8,
            'medium': 0.6,
            'low': 0.4,
            'unknown': 0.2
        }
    
    def compute_risk_score(self, events: List[Event], alerts: List[Alert]) -> float:
        """
        Compute comprehensive risk score (0-100) based on multiple factors
        
        Args:
            events: List of correlated events
            alerts: List of related alerts
            
        Returns:
            Risk score between 0-100
        """
        
        # Base score from threat intelligence
        threat_score = self._calculate_threat_intelligence_score(events)
        
        # Asset criticality impact
        asset_score = self._calculate_asset_criticality_score(events)
        
        # Temporal correlation factor
        temporal_score = self._calculate_temporal_correlation_score(events)
        
        # Volume and frequency analysis
        volume_score = self._calculate_volume_frequency_score(events)
        
        # MITRE ATT&CK technique severity
        mitre_score = self._calculate_mitre_attack_score(alerts)
        
        # Geographic risk factor
        geo_score = self._calculate_geographic_risk_score(events)
        
        # Combine scores with weighted average
        weights = {
            'threat': 0.25,
            'asset': 0.20,
            'temporal': 0.15,
            'volume': 0.15,
            'mitre': 0.15,
            'geo': 0.10
        }
        
        risk_score = (
            threat_score * weights['threat'] +
            asset_score * weights['asset'] +
            temporal_score * weights['temporal'] +
            volume_score * weights['volume'] +
            mitre_score * weights['mitre'] +
            geo_score * weights['geo']
        )
        
        # Apply confidence factor based on data quality
        confidence_factor = self._calculate_confidence_factor(events)
        final_score = risk_score * confidence_factor
        
        return min(100.0, max(0.0, final_score))
    
    def _calculate_threat_intelligence_score(self, events: List[Event]) -> float:
        """Calculate score based on threat intelligence reputation"""
        total_score = 0.0
        event_count = 0
        
        for event in events:
            # Source IP reputation
            source_reputation = event.enrichment.threat_intel.source_reputation
            if source_reputation:
                # Convert reputation score (-100 to 100) to risk score (0-100)
                source_risk = max(0, (100 - source_reputation.score) / 2)
                total_score += source_risk
                event_count += 1
            
            # Destination IP reputation
            dest_reputation = event.enrichment.threat_intel.dest_reputation
            if dest_reputation:
                dest_risk = max(0, (100 - dest_reputation.score) / 2)
                total_score += dest_risk
                event_count += 1
        
        return total_score / max(1, event_count)
    
    def _calculate_asset_criticality_score(self, events: List[Event]) -> float:
        """Calculate score based on affected asset criticality"""
        max_criticality_score = 0.0
        
        for event in events:
            # Source asset criticality
            source_criticality = event.enrichment.source_asset.criticality
            if source_criticality:
                source_score = self.asset_criticality_weights.get(source_criticality, 0.2)
                max_criticality_score = max(max_criticality_score, source_score)
            
            # Destination asset criticality
            dest_criticality = event.enrichment.dest_asset.criticality
            if dest_criticality:
                dest_score = self.asset_criticality_weights.get(dest_criticality, 0.2)
                max_criticality_score = max(max_criticality_score, dest_score)
        
        return max_criticality_score * 100
    
    def _calculate_temporal_correlation_score(self, events: List[Event]) -> float:
        """Calculate score based on temporal correlation patterns"""
        if len(events) < 2:
            return 0.0
        
        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda x: x.timestamp)
        
        # Calculate time intervals between events
        intervals = []
        for i in range(1, len(sorted_events)):
            interval = (sorted_events[i].timestamp - sorted_events[i-1].timestamp).total_seconds()
            intervals.append(interval)
        
        # Analyze burst patterns (short intervals indicate coordinated attack)
        burst_score = 0.0
        for interval in intervals:
            if interval < 60:  # Less than 1 minute
                burst_score += 20
            elif interval < 300:  # Less than 5 minutes
                burst_score += 10
            elif interval < 1800:  # Less than 30 minutes
                burst_score += 5
        
        # Normalize based on number of events
        return min(100.0, burst_score / len(events))
    
    def _calculate_volume_frequency_score(self, events: List[Event]) -> float:
        """Calculate score based on data volume and frequency"""
        total_bytes = sum(event.bytes_sent + event.bytes_received for event in events)
        total_packets = sum(event.packets_sent + event.packets_received for event in events)
        
        # Volume-based scoring
        volume_score = 0.0
        if total_bytes > 100 * 1024 * 1024:  # > 100MB
            volume_score += 30
        elif total_bytes > 10 * 1024 * 1024:  # > 10MB
            volume_score += 20
        elif total_bytes > 1024 * 1024:  # > 1MB
            volume_score += 10
        
        # Frequency-based scoring
        frequency_score = 0.0
        if len(events) > 1000:
            frequency_score += 30
        elif len(events) > 100:
            frequency_score += 20
        elif len(events) > 10:
            frequency_score += 10
        
        return min(100.0, volume_score + frequency_score)
    
    def _calculate_mitre_attack_score(self, alerts: List[Alert]) -> float:
        """Calculate score based on MITRE ATT&CK technique severity"""
        if not alerts:
            return 0.0
        
        total_score = 0.0
        technique_counts = {}
        
        for alert in alerts:
            for technique in alert.mitre_attack.techniques:
                technique_counts[technique] = technique_counts.get(technique, 0) + 1
        
        # MITRE ATT&CK technique severity weights
        technique_weights = {
            'T1055': 90,  # Process Injection
            'T1059': 85,  # Command and Scripting Interpreter
            'T1071': 80,  # Application Layer Protocol
            'T1110': 75,  # Brute Force
            'T1021': 70,  # Remote Services
            'T1046': 60,  # Network Service Scanning
            'T1041': 85,  # Exfiltration Over C2 Channel
            'T1074': 80,  # Data Staged
            'T1001': 75,  # Data Obfuscation
            'T1071.004': 70,  # DNS
            'T1110.001': 75,  # Password Brute Force
            'T1021.004': 70,  # SSH
        }
        
        for technique, count in technique_counts.items():
            weight = technique_weights.get(technique, 50)  # Default weight
            total_score += weight * min(count, 5)  # Cap at 5 occurrences
        
        return min(100.0, total_score / len(alerts))
    
    def _calculate_geographic_risk_score(self, events: List[Event]) -> float:
        """Calculate score based on geographic risk factors"""
        high_risk_countries = {
            'China': 80,
            'Russia': 75,
            'North Korea': 90,
            'Iran': 70,
            'Unknown': 60
        }
        
        max_geo_score = 0.0
        
        for event in events:
            source_country = event.enrichment.geolocation.source.country
            dest_country = event.enrichment.geolocation.dest.country
            
            source_score = high_risk_countries.get(source_country, 20)
            dest_score = high_risk_countries.get(dest_country, 20)
            
            max_geo_score = max(max_geo_score, source_score, dest_score)
        
        return max_geo_score
    
    def _calculate_confidence_factor(self, events: List[Event]) -> float:
        """Calculate confidence factor based on data quality"""
        if not events:
            return 0.0
        
        quality_indicators = 0
        total_indicators = 0
        
        for event in events:
            # Check for complete enrichment data
            if event.enrichment.threat_intel.source_reputation:
                quality_indicators += 1
            total_indicators += 1
            
            if event.enrichment.threat_intel.dest_reputation:
                quality_indicators += 1
            total_indicators += 1
            
            if event.enrichment.geolocation.source.country:
                quality_indicators += 1
            total_indicators += 1
            
            if event.enrichment.geolocation.dest.country:
                quality_indicators += 1
            total_indicators += 1
        
        return quality_indicators / max(1, total_indicators)
    
    def map_to_mitre_attack(self, events: List[Event], alerts: List[Alert]) -> MitreAttackMapping:
        """
        Map events and alerts to MITRE ATT&CK framework
        
        Returns:
            MitreAttackMapping object with tactics, techniques, and sub-techniques
        """
        tactics = set()
        techniques = set()
        sub_techniques = set()
        
        # Map based on alert MITRE data
        for alert in alerts:
            tactics.update(alert.mitre_attack.tactics)
            techniques.update(alert.mitre_attack.techniques)
            sub_techniques.update(alert.mitre_attack.sub_techniques)
        
        # Additional mapping based on event patterns
        for event in events:
            # Port-based technique mapping
            if event.dest_port == 22:
                techniques.add('T1021.004')  # SSH
                tactics.add('TA0007')  # Lateral Movement
            elif event.dest_port == 3389:
                techniques.add('T1021.001')  # Remote Desktop Protocol
                tactics.add('TA0007')  # Lateral Movement
            elif event.dest_port == 53:
                techniques.add('T1071.004')  # DNS
                tactics.add('TA0011')  # Command and Control
            
            # Protocol-based technique mapping
            if event.protocol == 6:  # TCP
                if event.tcp_flags & 0x02:  # SYN flag
                    techniques.add('T1046')  # Network Service Scanning
                    tactics.add('TA0043')  # Reconnaissance
            
            # Volume-based technique mapping
            if event.bytes_sent > 10 * 1024 * 1024:  # > 10MB
                techniques.add('T1041')  # Exfiltration Over C2 Channel
                tactics.add('TA0010')  # Exfiltration
        
        return MitreAttackMapping(
            tactics=list(tactics),
            techniques=list(techniques),
            sub_techniques=list(sub_techniques)
        )
    
    def correlate_events(self, events: List[Event], time_window: int = 3600) -> List[CorrelationGroup]:
        """
        Correlate events into groups based on similarity and temporal proximity
        
        Args:
            events: List of events to correlate
            time_window: Time window in seconds for correlation
            
        Returns:
            List of correlation groups
        """
        if len(events) < 2:
            return []
        
        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda x: x.timestamp)
        
        correlation_groups = []
        current_group = [sorted_events[0]]
        
        for i in range(1, len(sorted_events)):
            current_event = sorted_events[i]
            last_event = sorted_events[i-1]
            
            # Check temporal proximity
            time_diff = (current_event.timestamp - last_event.timestamp).total_seconds()
            
            if time_diff <= time_window:
                # Check similarity
                similarity_score = self._calculate_event_similarity(current_event, last_event)
                
                if similarity_score > 0.7:  # 70% similarity threshold
                    current_group.append(current_event)
                else:
                    # Start new group
                    if len(current_group) > 1:
                        correlation_groups.append(CorrelationGroup(
                            events=current_group,
                            correlation_score=self._calculate_group_correlation_score(current_group)
                        ))
                    current_group = [current_event]
            else:
                # Time window exceeded, start new group
                if len(current_group) > 1:
                    correlation_groups.append(CorrelationGroup(
                        events=current_group,
                        correlation_score=self._calculate_group_correlation_score(current_group)
                    ))
                current_group = [current_event]
        
        # Add final group if it has multiple events
        if len(current_group) > 1:
            correlation_groups.append(CorrelationGroup(
                events=current_group,
                correlation_score=self._calculate_group_correlation_score(current_group)
            ))
        
        return correlation_groups
    
    def _calculate_event_similarity(self, event1: Event, event2: Event) -> float:
        """Calculate similarity score between two events (0-1)"""
        similarity_score = 0.0
        total_factors = 0
        
        # IP similarity
        if event1.source_ip == event2.source_ip:
            similarity_score += 0.3
        if event1.dest_ip == event2.dest_ip:
            similarity_score += 0.3
        total_factors += 0.6
        
        # Port similarity
        if event1.dest_port == event2.dest_port:
            similarity_score += 0.2
        total_factors += 0.2
        
        # Protocol similarity
        if event1.protocol == event2.protocol:
            similarity_score += 0.1
        total_factors += 0.1
        
        # Asset similarity
        if (event1.enrichment.source_asset.hostname == 
            event2.enrichment.source_asset.hostname):
            similarity_score += 0.1
        total_factors += 0.1
        
        return similarity_score / max(1, total_factors)
    
    def _calculate_group_correlation_score(self, events: List[Event]) -> float:
        """Calculate correlation score for a group of events (0-1)"""
        if len(events) < 2:
            return 0.0
        
        total_similarity = 0.0
        comparisons = 0
        
        for i in range(len(events)):
            for j in range(i + 1, len(events)):
                similarity = self._calculate_event_similarity(events[i], events[j])
                total_similarity += similarity
                comparisons += 1
        
        return total_similarity / max(1, comparisons)


# Data classes for correlation results
@dataclass
class MitreAttackMapping:
    tactics: List[str]
    techniques: List[str]
    sub_techniques: List[str]

@dataclass
class CorrelationGroup:
    events: List[Event]
    correlation_score: float

@dataclass
class Event:
    event_id: str
    timestamp: datetime
    source_ip: str
    dest_ip: str
    source_port: int
    dest_port: int
    protocol: int
    bytes_sent: int
    bytes_received: int
    packets_sent: int
    packets_received: int
    tcp_flags: int
    enrichment: EnrichmentData

@dataclass
class Alert:
    alert_id: str
    timestamp: datetime
    mitre_attack: MitreAttackMapping

@dataclass
class EnrichmentData:
    source_asset: AssetInfo
    dest_asset: AssetInfo
    geolocation: GeolocationInfo
    threat_intel: ThreatIntelInfo

@dataclass
class AssetInfo:
    hostname: str
    criticality: str

@dataclass
class GeolocationInfo:
    source: GeoInfo
    dest: GeoInfo

@dataclass
class GeoInfo:
    country: str

@dataclass
class ThreatIntelInfo:
    source_reputation: ReputationInfo
    dest_reputation: ReputationInfo

@dataclass
class ReputationInfo:
    score: int
