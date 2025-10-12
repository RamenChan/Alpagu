# PyGuardian v3 - UI/UX Specification

## Design System

### Color Palette
```css
/* Primary Colors */
--primary-50: #eff6ff;
--primary-100: #dbeafe;
--primary-500: #3b82f6;
--primary-600: #2563eb;
--primary-700: #1d4ed8;
--primary-900: #1e3a8a;

/* Semantic Colors */
--success-50: #f0fdf4;
--success-500: #22c55e;
--success-600: #16a34a;

--warning-50: #fffbeb;
--warning-500: #f59e0b;
--warning-600: #d97706;

--error-50: #fef2f2;
--error-500: #ef4444;
--error-600: #dc2626;

--critical-50: #fef2f2;
--critical-500: #dc2626;
--critical-600: #b91c1c;

/* Neutral Colors */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-400: #9ca3af;
--gray-500: #6b7280;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-800: #1f2937;
--gray-900: #111827;

/* Dark Mode */
--dark-bg: #0f172a;
--dark-surface: #1e293b;
--dark-border: #334155;
```

### Typography
```css
/* Font Stack */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Headings */
h1: 2.25rem (36px) / font-weight: 700 / line-height: 1.2
h2: 1.875rem (30px) / font-weight: 600 / line-height: 1.3
h3: 1.5rem (24px) / font-weight: 600 / line-height: 1.4
h4: 1.25rem (20px) / font-weight: 500 / line-height: 1.5

/* Body Text */
body: 1rem (16px) / font-weight: 400 / line-height: 1.6
small: 0.875rem (14px) / font-weight: 400 / line-height: 1.5
caption: 0.75rem (12px) / font-weight: 400 / line-height: 1.4
```

### Spacing System
```css
/* Spacing Scale (Tailwind-based) */
--space-1: 0.25rem (4px)
--space-2: 0.5rem (8px)
--space-3: 0.75rem (12px)
--space-4: 1rem (16px)
--space-6: 1.5rem (24px)
--space-8: 2rem (32px)
--space-12: 3rem (48px)
--space-16: 4rem (64px)
```

## Page Specifications

### 1. Dashboard Page
**Purpose**: Central command center with real-time security overview

#### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ Header: Logo | Navigation | User Menu | Notifications       │
├─────────────────────────────────────────────────────────────┤
│ KPI Cards Row (4 columns)                                   │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐             │
│ │ Active  │ │ High    │ │ Events  │ │ Assets  │             │
│ │ Alerts  │ │ Risk    │ │ Today   │ │ Monitored│            │
│ │   12    │ │   3     │ │ 45,231  │ │   1,247 │             │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘             │
├─────────────────────────────────────────────────────────────┤
│ Main Content Area (2 columns)                               │
│ ┌─────────────────────┐ ┌─────────────────────────────────┐ │
│ │ Live Event Feed     │ │ Threat Map                      │ │
│ │ (60% width)         │ │ (40% width)                     │ │
│ │                     │ │                                 │ │
│ │ • Real-time events  │ │ • Interactive Mapbox            │ │
│ │ • Auto-refresh      │ │ • Geolocated threats            │ │
│ │ • Filter controls   │ │ • Zoom/pan controls             │ │
│ │ • Severity badges   │ │ • Country risk indicators       │ │
│ └─────────────────────┘ └─────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Bottom Row (3 columns)                                      │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │
│ │ Top Threats │ │ Recent      │ │ System      │             │
│ │ (MITRE)     │ │ Incidents   │ │ Health      │             │
│ │             │ │             │ │             │             │
│ │ • T1110     │ │ • SSH Brute │ │ • CPU: 45%  │             │
│ │ • T1021     │ │ • Port Scan │ │ • Memory: 67%│            │
│ │ • T1046     │ │ • Malware   │ │ • Disk: 23% │             │
│ └─────────────┘ └─────────────┘ └─────────────┘             │
└─────────────────────────────────────────────────────────────┘
```

#### Components & Interactions
- **KPI Cards**: Animated counters, color-coded by severity, click to drill down
- **Live Feed**: WebSocket updates, infinite scroll, severity filtering, search
- **Threat Map**: Real-time threat visualization, country risk overlay, incident markers
- **Top Threats**: MITRE ATT&CK technique breakdown with trend indicators
- **Recent Incidents**: Quick access to latest incidents with status badges
- **System Health**: Real-time metrics with alerting thresholds

#### Real-time Behaviors
- WebSocket connection for live updates
- Auto-refresh every 5 seconds for KPI cards
- Smooth animations for data changes
- Toast notifications for critical alerts
- Sound alerts for high-severity incidents

### 2. Incidents Page
**Purpose**: Incident management and triage interface

#### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ Page Header: Incidents | Filter Bar | Create Incident       │
├─────────────────────────────────────────────────────────────┤
│ Filter Panel (Collapsible)                                  │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Status: [All ▼] Priority: [All ▼] Severity: [All ▼]     │  │
│ │ Date Range: [Last 24h ▼] Assigned: [All ▼]              │  │
│ │ Search: [________________] [Apply] [Reset]              │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Incidents List (Table View)                                │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ ID │ Title │ Status │ Priority │ Severity │ Assigned │ │
│ │    │       │        │          │          │          │ │
│ │inc-│ SSH   │ [New]  │ [High]   │ [High]   │ John D.  │ │
│ │001 │ Brute │        │          │          │          │ │
│ │    │ Force │        │          │          │          │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Incident Detail Panel (Slide-out)                          │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Incident Details                                        │ │
│ │ ┌─────────────────┐ ┌─────────────────────────────────┐ │ │
│ │ │ Basic Info      │ │ Timeline                        │ │ │
│ │ │ • ID: inc-001   │ │ • Created: 2h ago               │ │ │
│ │ │ • Status: New   │ │ • Last Update: 1h ago           │ │ │
│ │ │ • Priority: High│ │ • Assigned: 30m ago             │ │ │
│ │ │ • Severity: High│ │                                 │ │ │
│ │ └─────────────────┘ └─────────────────────────────────┘ │ │
│ │                                                         │ │
│ │ MITRE ATT&CK Mapping                                    │ │
│ │ • T1110.001: Password Brute Force                       │ │
│ │ • T1021.004: SSH                                        │ │
│ │                                                         │ │
│ │ Affected Assets                                         │ │
│ │ • 192.168.1.100 (workstation-001)                      │ │
│ │                                                         │ │
│ │ Actions                                                 │ │
│ │ [Assign] [Escalate] [Resolve] [Add Note]               │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### Components & Interactions
- **Filter Panel**: Advanced filtering with saved filter presets
- **Incidents Table**: Sortable columns, bulk actions, status indicators
- **Detail Panel**: Slide-out panel with comprehensive incident information
- **Timeline**: Chronological event history with user actions
- **MITRE Mapping**: Interactive ATT&CK technique visualization
- **Asset List**: Clickable assets with drill-down capabilities
- **Action Buttons**: One-click incident management actions

#### Drill-down Behavior
- Click incident row → Open detail panel
- Click asset → Navigate to asset details
- Click MITRE technique → Show technique details
- Click timeline event → Show event details

### 3. Flow Explorer Page
**Purpose**: Network flow hunting and analysis interface

#### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ Page Header: Flow Explorer | Time Range | Export Options   │
├─────────────────────────────────────────────────────────────┤
│ Search & Filter Bar                                        │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Source IP: [________] Dest IP: [________] Port: [____] │ │
│ │ Protocol: [All ▼] Country: [All ▼] [Search] [Advanced] │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Flow Data Table (Virtualized)                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Time │ Source │ Dest │ Port │ Protocol │ Bytes │ Flags │ │
│ │      │        │      │      │          │       │       │ │
│ │10:30 │192.168.│203.0.│ 22   │ TCP      │ 3,072 │ SYN   │ │
│ │      │1.100   │113.45│      │          │       │       │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Flow Detail Panel (Bottom)                                 │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Flow Details                                            │ │
│ │ • Source: 192.168.1.100 (workstation-001)              │ │
│ │ • Destination: 203.0.113.45 (China, AS4134)            │ │
│ │ • Protocol: TCP/22 (SSH)                               │ │
│ │ • Duration: 30 seconds                                 │ │
│ │ • Data: 3,072 bytes sent, 6,144 bytes received         │ │
│ │                                                         │ │
│ │ Threat Intelligence                                     │ │
│ │ • Source Reputation: 85/100 (Legitimate)               │ │
│ │ • Dest Reputation: -45/100 (Malware, Botnet)           │ │
│ │                                                         │ │
│ │ Actions                                                 │ │
│ │ [Create Alert] [Block IP] [Export PCAP] [View Timeline]│ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### Components & Interactions
- **Search Bar**: Multi-field search with autocomplete
- **Filter Controls**: Advanced filtering with saved queries
- **Data Table**: Virtualized scrolling for large datasets
- **Detail Panel**: Expandable flow information
- **Threat Intel**: Integrated reputation and geolocation data
- **Action Buttons**: Quick response actions

#### Hunting Features
- **Time-based Analysis**: Timeline scrubbing and playback
- **Pattern Detection**: Automatic anomaly highlighting
- **Correlation**: Link related flows and events
- **Export**: PCAP, CSV, JSON export options

### 4. Threat Intel Page
**Purpose**: Threat intelligence management and visualization

#### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ Page Header: Threat Intelligence | Add Source | Sync Status│
├─────────────────────────────────────────────────────────────┤
│ Intel Sources Dashboard                                    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Source │ Status │ Last Update │ Records │ Actions      │ │
│ │        │        │             │         │              │ │
│ │ Abuse  │ [✓]    │ 2h ago      │ 1.2M    │ [Sync] [Edit]│ │
│ │ CH     │        │             │         │              │ │
│ │ Virus  │ [✓]    │ 1h ago      │ 850K    │ [Sync] [Edit]│ │
│ │ Total  │        │             │         │              │ │
│ │ MISP   │ [⚠]    │ 6h ago      │ 45K     │ [Sync] [Edit]│ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Threat Intelligence Data                                   │
│ ┌─────────────────────┐ ┌─────────────────────────────────┐ │
│ │ IP Reputation       │ │ Domain Reputation               │ │
│ │ (60% width)         │ │ (40% width)                     │ │
│ │                     │ │                                 │ │
│ │ • Top Malicious IPs │ │ • Suspicious Domains            │ │
│ │ • Geographic Dist.  │ │ • TLD Analysis                  │ │
│ │ • ASN Breakdown     │ │ • Registration Patterns         │ │
│ │ • Trend Analysis    │ │ • Subdomain Analysis            │ │
│ └─────────────────────┘ └─────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Threat Categories & IOCs                                   │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Category │ Count │ Last Seen │ Top Indicators           │ │
│ │           │       │           │                          │ │
│ │ Malware   │ 45K   │ 2h ago    │ • 203.0.113.45          │ │
│ │ Botnet    │ 23K   │ 1h ago    │ • malware.example.com   │ │
│ │ Phishing  │ 12K   │ 30m ago   │ • abc123def456          │ │
│ │ C2        │ 8K    │ 15m ago   │ • https://evil.com      │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### Components & Interactions
- **Source Management**: Add, edit, sync threat intel sources
- **Reputation Views**: IP and domain reputation with filtering
- **Category Analysis**: Threat category breakdown and trends
- **IOC Management**: Indicator of Compromise search and management
- **Sync Status**: Real-time sync status and error handling

### 5. Reports Page
**Purpose**: Security reporting and analytics

#### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ Page Header: Reports | Generate Report | Schedule Reports  │
├─────────────────────────────────────────────────────────────┤
│ Report Templates                                           │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Template │ Description │ Last Run │ Next Run │ Actions  │ │
│ │          │             │          │          │          │ │
│ │ Executive│ Monthly     │ 1d ago   │ 29d      │ [Run]    │ │
│ │ Summary  │ overview    │          │          │ [Edit]   │ │
│ │          │             │          │          │          │ │
│ │ Incident │ Detailed    │ 3h ago   │ 21h      │ [Run]    │ │
│ │ Analysis │ incident    │          │          │ [Edit]   │ │
│ │          │ report      │          │          │          │ │
│ │ Threat   │ Threat intel│ 6h ago   │ 18h      │ [Run]    │ │
│ │ Intel    │ summary     │          │          │ [Edit]   │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Report Builder (Modal)                                     │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Report Configuration                                    │ │
│ │ • Name: [________________]                              │ │
│ │ • Type: [Executive Summary ▼]                          │ │
│ │ • Period: [Last 30 days ▼]                             │ │
│ │ • Format: [PDF ▼] [Excel ▼] [HTML ▼]                   │ │
│ │ • Recipients: [________________]                        │ │
│ │                                                         │ │
│ │ Sections                                                │ │
│ │ ☑ Executive Summary                                     │ │
│ │ ☑ Incident Overview                                     │ │
│ │ ☑ Threat Landscape                                      │ │
│ │ ☑ Asset Risk Assessment                                 │ │
│ │ ☑ Compliance Status                                     │ │
│ │                                                         │ │
│ │ [Generate] [Save Template] [Cancel]                     │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### Components & Interactions
- **Template Gallery**: Pre-built report templates
- **Report Builder**: Drag-and-drop report creation
- **Scheduling**: Automated report generation and delivery
- **Export Options**: Multiple format support (PDF, Excel, HTML)
- **Distribution**: Email and webhook delivery options

### 6. Admin Page
**Purpose**: System administration and configuration

#### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ Page Header: Administration | System Status | Backup       │
├─────────────────────────────────────────────────────────────┤
│ Admin Navigation Tabs                                      │
│ [Users] [Roles] [Settings] [Integrations] [System] [Logs]  │
├─────────────────────────────────────────────────────────────┤
│ Active Tab Content                                         │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Users Management                                        │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ User │ Email │ Role │ Status │ Last Login │ Actions │ │ │
│ │ │      │       │      │        │            │         │ │ │
│ │ │ John │ john@ │ Admin│ Active │ 2h ago     │ [Edit]  │ │ │
│ │ │ Doe  │ co.com│      │        │            │ [Reset] │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ │                                                         │ │
│ │ [Add User] [Bulk Import] [Export Users]                 │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### Components & Interactions
- **User Management**: CRUD operations for users and roles
- **System Settings**: Global configuration management
- **Integration Setup**: External service configuration
- **System Monitoring**: Health checks and performance metrics
- **Audit Logs**: Security event logging and review

## Microinteractions & Accessibility

### Microinteractions
- **Hover Effects**: Subtle color transitions and shadow changes
- **Loading States**: Skeleton screens and progress indicators
- **Success Feedback**: Green checkmarks and success animations
- **Error Handling**: Red error states with helpful messages
- **Data Updates**: Smooth transitions for real-time data changes
- **Button States**: Clear pressed, hover, and disabled states

### Accessibility Features
- **Color Contrast**: WCAG AA compliant contrast ratios (4.5:1 minimum)
- **Keyboard Navigation**: Full keyboard support with visible focus indicators
- **Screen Reader**: ARIA labels and semantic HTML structure
- **High Contrast Mode**: Alternative color scheme for visual impairments
- **Font Scaling**: Support for browser font size adjustments
- **Reduced Motion**: Respects `prefers-reduced-motion` setting

### ARIA Implementation
```html
<!-- Example ARIA implementation -->
<div role="tablist" aria-label="Incident management tabs">
  <button role="tab" aria-selected="true" aria-controls="panel-1">
    Active Incidents
  </button>
  <div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
    <!-- Panel content -->
  </div>
</div>

<!-- Live region for dynamic updates -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  New incident created: SSH brute force attack
</div>
```

### Keyboard Navigation
- **Tab Order**: Logical tab sequence through interface
- **Shortcuts**: Common keyboard shortcuts (Ctrl+F for search, etc.)
- **Focus Management**: Proper focus handling in modals and panels
- **Skip Links**: Skip to main content for screen readers

## Responsive Design

### Breakpoints
```css
/* Mobile First Approach */
sm: 640px   /* Small devices */
md: 768px   /* Medium devices */
lg: 1024px  /* Large devices */
xl: 1280px  /* Extra large devices */
2xl: 1536px /* 2X large devices */
```

### Mobile Adaptations
- **Collapsible Navigation**: Hamburger menu for mobile
- **Stacked Layout**: Single column layout on small screens
- **Touch Targets**: Minimum 44px touch targets
- **Swipe Gestures**: Swipe to dismiss notifications
- **Pull to Refresh**: Native mobile refresh behavior

### Tablet Adaptations
- **Two-Column Layout**: Optimized for tablet screen sizes
- **Touch-Friendly**: Larger buttons and touch targets
- **Orientation Support**: Both portrait and landscape modes
- **Split View**: Side-by-side panels when space allows
