# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python-based security intelligence tool for analyzing port scan incidents from Thinkst Canary honeypot devices. Provides comprehensive statistics, IP grouping, frequency analysis, and timeline tracking for threat analysis.

## Running the Script

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with credentials
cat > .env << 'EOF'
CANARY_CONSOLE_DOMAIN=your-console.canary.tools
CANARY_API_KEY=your-api-key-here
EOF

# Run (credentials auto-load from .env)
python3 canary_events.py
```

## Architecture

### Single Module Design

All functionality in `canary_events.py`:

**Core Classes:**
- `CanaryAPI` - API client for Canary console
  - Handles authentication (API token as query parameter)
  - Methods: `get_all_incidents()`, `get_unacknowledged_incidents()`, `get_devices()`
  - Automatically strips protocol from console domain

**Analysis Functions:**
- `is_port_scan()` - Filters port scan incidents
- `format_incident()` - Simplified IP + timestamp display
- `get_incident_ip()` - Extracts source IP from nested incident structure
- `get_incident_timestamp()` - Extracts and converts timestamp
- `analyze_by_ip()` - Groups scans by source IP with percentages
- `analyze_frequency()` - Monthly distribution and time-based analysis
- `show_repeat_offenders()` - Displays IPs with >1 scan, returns list
- `show_ip_timeline()` - Detailed timeline for individual IP

**Interactive Flow:**
1. Fetch incidents (limit: 100)
2. Filter for port scans only
3. Display chronological list
4. Show IP grouping analysis
5. Show frequency analysis
6. Prompt to view repeat offenders
7. Loop: prompt to view individual IP timelines
   - User can view multiple timelines
   - Exit loop by answering 'n'

### Data Structure Notes

Canary API returns incidents with nested structure:
```python
{
  'id': 'incident:hostportscan:...',
  'description': {  # Nested dict containing actual data
    'created': '1772030223',  # String timestamp
    'description': 'Host Port Scan',
    'src_host': '172.24.22.240',
    'dst_host': '172.24.18.216',
    'node_id': '000000003524fc36',
    'acknowledged': 'True',  # String boolean
    'name': 'conf-room-macmini',
    'flock_name': 'Default Flock',
    ...
  }
}
```

Must access nested `description` dict for all incident details.

## API Details

**Base URL**: `https://{console_domain}/api/v1`
- Console domain can include or omit `https://` prefix (script handles both)
- Authentication: `auth_token` query parameter on all requests
- Response format: JSON with `result: "success"` or `result: "error"`

**Endpoints Used:**
- `/incidents/all?limit=100` - Retrieve recent incidents
- `/devices/all` - List all Canary devices (shown in initial version, not current)

## Credentials

**Loading**: Uses `python-dotenv` to auto-load `.env` file at startup
**Format**: Plain key=value pairs (no quotes, no export)
```
CANARY_CONSOLE_DOMAIN=1234abc.canary.tools
CANARY_API_KEY=abc123...
```

Never commit `.env` (gitignored). Use `.env.example` for template.

## Key Implementation Details

**Domain Handling**: Script strips `https://` or `http://` prefix from console domain before constructing URLs to handle both input formats.

**Timestamp Conversion**: API returns timestamps as strings; convert to int before passing to `datetime.fromtimestamp()`.

**Boolean Conversion**: API returns booleans as strings ('True'/'False'); compare with `== 'True'`.

**Port Scan Detection**: Check if `'Port Scan'` substring exists in `incident['description']['description']` field.

**Interactive Loops**: Timeline selection uses `while True` loop with `break` on 'n' response.

## Testing

Test with real API credentials in `.env`:
```bash
python3 canary_events.py
```

Interactive responses can be automated for testing:
```bash
echo -e "y\ny\n1\ny\n2\nn" | python3 canary_events.py
```

## Dependencies

- `requests>=2.31.0` - HTTP client for API calls
- `python-dotenv>=1.0.0` - Auto-load .env files

## Common Development Tasks

**Add new analysis function**: Follow pattern of existing functions that take `port_scans: List[Dict]` parameter.

**Modify incident filtering**: Update `is_port_scan()` function logic.

**Change display format**: Update `format_incident()` return string.

**Add new API endpoint**: Add method to `CanaryAPI` class following existing pattern with `_make_request()`.

## File Structure

```
.
├── canary_events.py      # Main script (all functionality)
├── requirements.txt      # Python dependencies
├── setup.sh             # Automated setup script
├── .env.example         # Credentials template
├── .gitignore           # Protects .env file
├── README.md            # User documentation
├── DEPLOY.md            # Deployment guide
└── CLAUDE.md            # This file
```

## Thinkst Canary Context

Thinkst Canary is a honeypot/deception platform for detecting network intrusions. Common incident types:
- **Host Port Scan** - Single device port scanning
- **Consolidated Network Port Scan** - Broader network scanning
- **Canary Disconnected** - Device connectivity issues (filtered out by script)

Port scans indicate reconnaissance activity and potential threats.
