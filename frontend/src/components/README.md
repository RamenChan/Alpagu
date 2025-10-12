# PyGuardian v3 - React Component Scaffold

## Top 12 Core Components

### 1. TopKPI Component
**Purpose**: Display key performance indicators on dashboard

```typescript
interface TopKPIProps {
  kpis: DashboardKPIs;
  isLoading?: boolean;
  onKpiClick?: (kpi: string) => void;
}

// Example usage:
<TopKPI 
  kpis={{
    active_alerts: 12,
    high_risk_incidents: 3,
    events_today: 45231,
    assets_monitored: 1247
  }}
  onKpiClick={(kpi) => navigateToDetail(kpi)}
/>
```

**Features**:
- Animated counters with smooth transitions
- Color-coded severity indicators
- Click handlers for drill-down navigation
- Loading skeleton states
- Responsive grid layout

### 2. LiveFeed Component
**Purpose**: Real-time event stream with filtering

```typescript
interface LiveFeedProps {
  events: LiveEvent[];
  isLoading?: boolean;
  onEventClick?: (event: LiveEvent) => void;
  onFilterChange?: (filters: FilterOptions) => void;
}

// Example usage:
<LiveFeed 
  events={liveEvents}
  onEventClick={(event) => showEventDetails(event)}
  onFilterChange={(filters) => updateFilters(filters)}
/>
```

**Features**:
- WebSocket integration for real-time updates
- Infinite scroll with virtualization
- Severity-based filtering
- Search functionality
- Auto-refresh controls
- Event type indicators

### 3. ThreatMap Component
**Purpose**: Interactive geographic threat visualization

```typescript
interface ThreatMapProps {
  data: ThreatMapData[];
  isLoading?: boolean;
  onMarkerClick?: (data: ThreatMapData) => void;
  onRegionClick?: (country: string) => void;
}

// Example usage:
<ThreatMap 
  data={threatMapData}
  onMarkerClick={(data) => showThreatDetails(data)}
  onRegionClick={(country) => filterByCountry(country)}
/>
```

**Features**:
- Mapbox GL JS integration
- Real-time threat markers
- Country risk overlays
- Zoom and pan controls
- Clustering for high-density areas
- Custom threat icons

### 4. IncidentCard Component
**Purpose**: Individual incident display with actions

```typescript
interface IncidentCardProps {
  incident: Incident;
  onStatusChange?: (incidentId: string, status: IncidentStatus) => void;
  onAssign?: (incidentId: string, userId: string) => void;
  onPriorityChange?: (incidentId: string, priority: Priority) => void;
  onClick?: (incident: Incident) => void;
}

// Example usage:
<IncidentCard 
  incident={incident}
  onStatusChange={(id, status) => updateIncidentStatus(id, status)}
  onAssign={(id, userId) => assignIncident(id, userId)}
  onClick={(incident) => openIncidentDetails(incident)}
/>
```

**Features**:
- Status badges with color coding
- Priority indicators
- Quick action buttons
- MITRE ATT&CK technique display
- Risk score visualization
- Asset information

### 5. TriagePanel Component
**Purpose**: Incident triage and management interface

```typescript
interface TriagePanelProps {
  incident: Incident;
  onUpdate?: (incident: Partial<Incident>) => void;
  onAddNote?: (incidentId: string, note: string) => void;
  onRunPlaybook?: (incidentId: string, playbookId: string) => void;
  onClose?: () => void;
}

// Example usage:
<TriagePanel 
  incident={selectedIncident}
  onUpdate={(updates) => updateIncident(updates)}
  onAddNote={(id, note) => addIncidentNote(id, note)}
  onRunPlaybook={(id, playbookId) => executePlaybook(id, playbookId)}
  onClose={() => closePanel()}
/>
```

**Features**:
- Slide-out panel design
- Timeline visualization
- Note management
- Playbook execution
- Asset correlation
- MITRE mapping display

### 6. FlowFilter Component
**Purpose**: Advanced filtering for flow data

```typescript
interface FlowFilterProps {
  filters: FilterOptions;
  onFilterChange: (filters: FilterOptions) => void;
  onReset: () => void;
  availableFilters: string[];
}

// Example usage:
<FlowFilter 
  filters={currentFilters}
  onFilterChange={(filters) => setFilters(filters)}
  onReset={() => resetFilters()}
  availableFilters={['source_ip', 'dest_ip', 'port', 'protocol']}
/>
```

**Features**:
- Multi-field filtering
- Saved filter presets
- Date range picker
- Autocomplete suggestions
- Filter validation
- Export filtered results

### 7. CorrelationGraph Component
**Purpose**: Network correlation visualization

```typescript
interface CorrelationGraphProps {
  data: {
    nodes: GraphNode[];
    edges: GraphEdge[];
  };
  onNodeClick?: (node: GraphNode) => void;
  onEdgeClick?: (edge: GraphEdge) => void;
  layout?: 'force' | 'hierarchical' | 'circular';
}

// Example usage:
<CorrelationGraph 
  data={correlationData}
  onNodeClick={(node) => showNodeDetails(node)}
  onEdgeClick={(edge) => showEdgeDetails(edge)}
  layout="force"
/>
```

**Features**:
- D3.js or Cytoscape.js integration
- Interactive node/edge selection
- Multiple layout algorithms
- Zoom and pan controls
- Node clustering
- Edge weight visualization

### 8. RuleEditor Component
**Purpose**: Detection rule creation and editing

```typescript
interface RuleEditorProps {
  rule?: DetectionRule;
  onSave?: (rule: DetectionRule) => void;
  onCancel?: () => void;
  onTest?: (rule: DetectionRule) => void;
}

// Example usage:
<RuleEditor 
  rule={editingRule}
  onSave={(rule) => saveRule(rule)}
  onCancel={() => cancelEditing()}
  onTest={(rule) => testRule(rule)}
/>
```

**Features**:
- Visual rule builder
- Condition editor
- Action configuration
- Rule validation
- Test mode
- MITRE mapping

### 9. PlaybookRunner Component
**Purpose**: Automated playbook execution interface

```typescript
interface PlaybookRunnerProps {
  playbook: PlaybookExecution;
  onStepComplete?: (stepId: string, output: string) => void;
  onPlaybookComplete?: (playbookId: string) => void;
  onError?: (error: string) => void;
}

// Example usage:
<PlaybookRunner 
  playbook={runningPlaybook}
  onStepComplete={(stepId, output) => updateStepStatus(stepId, output)}
  onPlaybookComplete={(id) => handlePlaybookComplete(id)}
  onError={(error) => showError(error)}
/>
```

**Features**:
- Step-by-step execution
- Real-time progress updates
- Output capture
- Error handling
- Manual intervention points
- Rollback capabilities

### 10. AlertTimeline Component
**Purpose**: Chronological alert visualization

```typescript
interface AlertTimelineProps {
  alerts: Alert[];
  onAlertClick?: (alert: Alert) => void;
  onStatusChange?: (alertId: string, status: AlertStatus) => void;
  timeRange?: {
    start: string;
    end: string;
  };
}

// Example usage:
<AlertTimeline 
  alerts={timelineAlerts}
  onAlertClick={(alert) => showAlertDetails(alert)}
  onStatusChange={(id, status) => updateAlertStatus(id, status)}
  timeRange={{ start: '2024-01-15T00:00:00Z', end: '2024-01-15T23:59:59Z' }}
/>
```

**Features**:
- Timeline visualization
- Alert clustering
- Status management
- Time range filtering
- Severity indicators
- Correlation highlighting

### 11. Login Component
**Purpose**: User authentication interface

```typescript
interface LoginProps {
  onLogin: (credentials: { email: string; password: string }) => void;
  isLoading?: boolean;
  error?: string;
}

// Example usage:
<Login 
  onLogin={(credentials) => authenticateUser(credentials)}
  isLoading={isAuthenticating}
  error={authError}
/>
```

**Features**:
- Form validation
- Loading states
- Error handling
- Remember me option
- Password reset link
- OAuth integration

### 12. Settings Component
**Purpose**: User preferences and system configuration

```typescript
interface SettingsProps {
  user: User;
  onUpdate?: (user: Partial<User>) => void;
  onPasswordChange?: (oldPassword: string, newPassword: string) => void;
  onPreferencesChange?: (preferences: Record<string, any>) => void;
}

// Example usage:
<Settings 
  user={currentUser}
  onUpdate={(updates) => updateUser(updates)}
  onPasswordChange={(old, new) => changePassword(old, new)}
  onPreferencesChange={(prefs) => updatePreferences(prefs)}
/>
```

**Features**:
- Profile management
- Password change
- Notification preferences
- Theme selection
- Dashboard customization
- API key management

## Component Architecture

### State Management
- **Redux Toolkit**: Global state management
- **React Query**: Server state and caching
- **Zustand**: Local component state

### Styling
- **Tailwind CSS**: Utility-first styling
- **Headless UI**: Accessible component primitives
- **Framer Motion**: Animations and transitions

### Testing
- **Jest**: Unit testing
- **React Testing Library**: Component testing
- **Cypress**: End-to-end testing

### Performance
- **React.memo**: Memoization for expensive components
- **useMemo/useCallback**: Hook optimization
- **Virtual scrolling**: Large list performance
- **Code splitting**: Lazy loading

## Component Guidelines

### 1. Accessibility
- Use semantic HTML elements
- Implement ARIA labels and roles
- Ensure keyboard navigation
- Maintain color contrast ratios
- Support screen readers

### 2. Responsive Design
- Mobile-first approach
- Flexible layouts
- Touch-friendly interactions
- Adaptive typography
- Progressive enhancement

### 3. Error Handling
- Graceful error boundaries
- User-friendly error messages
- Retry mechanisms
- Fallback UI states
- Error logging

### 4. Performance
- Lazy loading
- Memoization
- Virtual scrolling
- Debounced inputs
- Optimized re-renders

### 5. Testing
- Unit tests for logic
- Integration tests for workflows
- Visual regression tests
- Accessibility tests
- Performance tests
