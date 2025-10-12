// PyGuardian v3 - TypeScript Type Definitions

// Base types
export interface BaseEntity {
  id: string;
  created_at: string;
  updated_at: string;
}

// User and Authentication
export interface User extends BaseEntity {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  is_active: boolean;
  last_login?: string;
  avatar_url?: string;
}

export type UserRole = 'admin' | 'analyst' | 'viewer';

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// Event and Flow types
export interface FlowEvent extends BaseEntity {
  timestamp: string;
  collector_id: string;
  source_ip: string;
  dest_ip: string;
  source_port: number;
  dest_port: number;
  protocol: number;
  bytes_sent: number;
  bytes_received: number;
  packets_sent: number;
  packets_received: number;
  duration: number;
  tcp_flags: number;
  tos: number;
  enrichment: EnrichmentData;
  raw_data: Record<string, any>;
}

export interface EnrichmentData {
  source_asset: AssetInfo;
  dest_asset: AssetInfo;
  geolocation: GeolocationInfo;
  threat_intel: ThreatIntelInfo;
}

export interface AssetInfo {
  hostname?: string;
  os?: string;
  owner?: string;
  department?: string;
  criticality: 'low' | 'medium' | 'high' | 'critical' | 'unknown';
}

export interface GeolocationInfo {
  source: GeoInfo;
  dest: GeoInfo;
}

export interface GeoInfo {
  country: string;
  region: string;
  city: string;
  latitude: number;
  longitude: number;
  asn: string;
  organization: string;
}

export interface ThreatIntelInfo {
  source_reputation: ReputationInfo;
  dest_reputation: ReputationInfo;
}

export interface ReputationInfo {
  score: number;
  categories: string[];
  sources: string[];
  last_updated: string;
}

// Alert and Incident types
export interface Alert extends BaseEntity {
  timestamp: string;
  rule_id: string;
  rule_name: string;
  severity: Severity;
  status: AlertStatus;
  source_events: string[];
  description: string;
  mitre_attack: MitreAttackMapping;
  risk_score: number;
  affected_assets: string[];
  indicators: Indicators;
  context: Record<string, any>;
  assigned_to?: string;
  created_by: string;
  tags: string[];
}

export interface Incident extends BaseEntity {
  title: string;
  description: string;
  status: IncidentStatus;
  priority: Priority;
  severity: Severity;
  created_at: string;
  updated_at: string;
  resolved_at?: string;
  assigned_to?: string;
  created_by: string;
  source_alerts: string[];
  mitre_attack: MitreAttackMapping;
  risk_score: number;
  affected_assets: string[];
  indicators: Indicators;
  timeline: TimelineEvent[];
  playbooks: PlaybookExecution[];
  tags: string[];
  notes: IncidentNote[];
}

export type Severity = 'low' | 'medium' | 'high' | 'critical';
export type Priority = 'low' | 'medium' | 'high' | 'critical';
export type AlertStatus = 'new' | 'investigating' | 'resolved' | 'false_positive';
export type IncidentStatus = 'new' | 'investigating' | 'contained' | 'resolved' | 'closed';

export interface MitreAttackMapping {
  tactics: string[];
  techniques: string[];
  sub_techniques: string[];
}

export interface Indicators {
  ips: string[];
  domains: string[];
  hashes: string[];
  urls: string[];
}

export interface TimelineEvent {
  timestamp: string;
  event_type: string;
  description: string;
  user: string;
  metadata: Record<string, any>;
}

export interface PlaybookExecution {
  playbook_id: string;
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  started_at: string;
  completed_at?: string;
  steps: PlaybookStep[];
}

export interface PlaybookStep {
  step_id: string;
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  output?: string;
}

export interface IncidentNote {
  timestamp: string;
  user: string;
  content: string;
  type: 'note' | 'action' | 'observation';
}

// Threat Intelligence types
export interface ThreatIntelSource extends BaseEntity {
  name: string;
  type: 'ip' | 'domain' | 'hash' | 'url';
  status: 'active' | 'inactive' | 'error';
  last_sync: string;
  record_count: number;
  configuration: Record<string, any>;
}

export interface ThreatIntelRecord {
  indicator: string;
  type: 'ip' | 'domain' | 'hash' | 'url';
  reputation_score: number;
  categories: string[];
  sources: string[];
  first_seen: string;
  last_seen: string;
  metadata: Record<string, any>;
}

// Rule Engine types
export interface DetectionRule extends BaseEntity {
  name: string;
  description: string;
  enabled: boolean;
  severity: Severity;
  category: string;
  conditions: RuleCondition[];
  aggregation: RuleAggregation;
  mitre_attack: MitreAttackMapping;
  actions: RuleAction[];
  tags: string[];
  created_by: string;
}

export interface RuleCondition {
  field: string;
  operator: 'equals' | 'not_equals' | 'contains' | 'not_contains' | 'greater_than' | 'less_than' | 'in' | 'not_in';
  value: any;
}

export interface RuleAggregation {
  group_by: string[];
  time_window: string;
  threshold: {
    count?: number;
    unique_dest_ports?: number;
    total_bytes?: number;
    operator: 'greater_than' | 'less_than' | 'equals' | 'greater_than_or_equal' | 'less_than_or_equal';
  };
}

export interface RuleAction {
  type: 'create_alert' | 'notify' | 'create_incident' | 'run_script';
  severity?: Severity;
  channels?: string[];
  recipients?: string[];
  priority?: Priority;
  script?: string;
  parameters?: Record<string, any>;
  auto_assign?: boolean;
}

// Dashboard and Analytics types
export interface DashboardKPIs {
  active_alerts: number;
  high_risk_incidents: number;
  events_today: number;
  assets_monitored: number;
  threats_blocked: number;
  false_positives: number;
}

export interface ThreatMapData {
  source_ip: string;
  dest_ip: string;
  source_country: string;
  dest_country: string;
  source_lat: number;
  source_lng: number;
  dest_lat: number;
  dest_lng: number;
  severity: Severity;
  count: number;
  timestamp: string;
}

export interface LiveEvent {
  id: string;
  timestamp: string;
  type: 'flow' | 'alert' | 'incident';
  severity: Severity;
  source_ip: string;
  dest_ip: string;
  description: string;
  tags: string[];
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: 'success' | 'error';
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface ApiError {
  message: string;
  code: string;
  details?: Record<string, any>;
}

// Filter and Search types
export interface FilterOptions {
  status?: string[];
  severity?: Severity[];
  priority?: Priority[];
  date_range?: {
    start: string;
    end: string;
  };
  assigned_to?: string[];
  tags?: string[];
  search?: string;
}

export interface SortOptions {
  field: string;
  direction: 'asc' | 'desc';
}

export interface PaginationOptions {
  page: number;
  per_page: number;
}

// WebSocket types
export interface WebSocketMessage {
  type: 'event' | 'alert' | 'incident' | 'system_status';
  data: any;
  timestamp: string;
}

// Component Props types
export interface TopKPIProps {
  kpis: DashboardKPIs;
  isLoading?: boolean;
  onKpiClick?: (kpi: string) => void;
}

export interface LiveFeedProps {
  events: LiveEvent[];
  isLoading?: boolean;
  onEventClick?: (event: LiveEvent) => void;
  onFilterChange?: (filters: FilterOptions) => void;
}

export interface ThreatMapProps {
  data: ThreatMapData[];
  isLoading?: boolean;
  onMarkerClick?: (data: ThreatMapData) => void;
  onRegionClick?: (country: string) => void;
}

export interface IncidentCardProps {
  incident: Incident;
  onStatusChange?: (incidentId: string, status: IncidentStatus) => void;
  onAssign?: (incidentId: string, userId: string) => void;
  onPriorityChange?: (incidentId: string, priority: Priority) => void;
  onClick?: (incident: Incident) => void;
}

export interface TriagePanelProps {
  incident: Incident;
  onUpdate?: (incident: Partial<Incident>) => void;
  onAddNote?: (incidentId: string, note: string) => void;
  onRunPlaybook?: (incidentId: string, playbookId: string) => void;
  onClose?: () => void;
}

export interface FlowFilterProps {
  filters: FilterOptions;
  onFilterChange: (filters: FilterOptions) => void;
  onReset: () => void;
  availableFilters: string[];
}

export interface CorrelationGraphProps {
  data: {
    nodes: GraphNode[];
    edges: GraphEdge[];
  };
  onNodeClick?: (node: GraphNode) => void;
  onEdgeClick?: (edge: GraphEdge) => void;
  layout?: 'force' | 'hierarchical' | 'circular';
}

export interface GraphNode {
  id: string;
  label: string;
  type: 'ip' | 'domain' | 'asset' | 'user';
  severity?: Severity;
  metadata: Record<string, any>;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  weight: number;
  metadata: Record<string, any>;
}

export interface RuleEditorProps {
  rule?: DetectionRule;
  onSave?: (rule: DetectionRule) => void;
  onCancel?: () => void;
  onTest?: (rule: DetectionRule) => void;
}

export interface PlaybookRunnerProps {
  playbook: PlaybookExecution;
  onStepComplete?: (stepId: string, output: string) => void;
  onPlaybookComplete?: (playbookId: string) => void;
  onError?: (error: string) => void;
}

export interface AlertTimelineProps {
  alerts: Alert[];
  onAlertClick?: (alert: Alert) => void;
  onStatusChange?: (alertId: string, status: AlertStatus) => void;
  timeRange?: {
    start: string;
    end: string;
  };
}

export interface LoginProps {
  onLogin: (credentials: { email: string; password: string }) => void;
  isLoading?: boolean;
  error?: string;
}

export interface SettingsProps {
  user: User;
  onUpdate?: (user: Partial<User>) => void;
  onPasswordChange?: (oldPassword: string, newPassword: string) => void;
  onPreferencesChange?: (preferences: Record<string, any>) => void;
}

// Utility types
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

export type Theme = 'light' | 'dark' | 'auto';

export interface UserPreferences {
  theme: Theme;
  notifications: {
    email: boolean;
    browser: boolean;
    sound: boolean;
  };
  dashboard: {
    refresh_interval: number;
    default_time_range: string;
    show_live_feed: boolean;
    show_threat_map: boolean;
  };
  table: {
    page_size: number;
    default_sort: SortOptions;
  };
}
