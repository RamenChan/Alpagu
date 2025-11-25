// User and Authentication
export interface User {
  id: string;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login?: string;
}

// Alert types
export interface Alert {
  id: string;
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  status: 'new' | 'acknowledged' | 'resolved' | 'false_positive';
  source_ip?: string;
  dest_ip?: string;
  source_port?: number;
  dest_port?: number;
  protocol?: string;
  risk_score: number;
  created_at: string;
  updated_at: string;
  acknowledged_at?: string;
  resolved_at?: string;
}

// Dashboard types
export interface DashboardKPIs {
  total_alerts: number;
  new_alerts: number;
  critical_alerts: number;
  high_alerts: number;
  alerts_today: number;
  alerts_this_week: number;
}

// Notification settings
export interface NotificationSettings {
  id: string;
  email_enabled: boolean;
  email_address?: string;
  webhook_enabled: boolean;
  webhook_url?: string;
  notify_on_critical: boolean;
  notify_on_high: boolean;
  notify_on_medium: boolean;
  notify_on_low: boolean;
  quiet_hours_enabled: boolean;
  quiet_hours_start: number;
  quiet_hours_end: number;
}
