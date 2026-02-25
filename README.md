# Canary Scanners

A comprehensive Python tool for analyzing port scan incidents from Thinkst Canary honeypot devices. Provides detailed statistics, IP grouping, frequency analysis, and timeline tracking for security threat intelligence.

## Features

- 🎯 **Port Scan Filtering** - Automatically filters to show only port scan incidents
- 📊 **IP Grouping Analysis** - Groups scans by source IP with percentages
- 📈 **Frequency Analysis** - Monthly distribution with visual charts
- 🔍 **Repeat Offenders** - Identifies IPs with multiple scans
- ⏱️ **IP Timeline** - Detailed scan timeline for individual IPs
- 🔄 **Interactive** - Browse multiple IP timelines in one session
- ⚙️ **Auto-Configuration** - Loads credentials from `.env` file automatically

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
git clone https://github.com/pwhitlow/canaryscanners.git
cd canaryscanners
./setup.sh
```

Then edit `.env` with your credentials and run:
```bash
./canary_events.py
```

### Option 2: Manual Setup

```bash
# Clone repository
git clone https://github.com/pwhitlow/canaryscanners.git
cd canaryscanners

# Install dependencies
pip3 install -r requirements.txt

# Create .env file
cat > .env << 'EOF'
CANARY_CONSOLE_DOMAIN=your-console.canary.tools
CANARY_API_KEY=your-api-key-here
EOF

# Run
python3 canary_events.py
```

## Configuration

Create a `.env` file in the project directory:

```bash
# Your Canary console domain (with or without https://)
CANARY_CONSOLE_DOMAIN=1234abc.canary.tools

# Your API key from Canary console (Settings → API)
CANARY_API_KEY=your-api-key-here
```

The script automatically loads these credentials at startup.

## Usage

Run the script:
```bash
./canary_events.py
```

### Interactive Features

1. **Port Scan List** - Shows all port scans with IP and timestamp
2. **IP Grouping** - Displays source IPs ranked by scan frequency
3. **Frequency Analysis** - Shows scanning patterns over time
4. **Repeat Offenders** - Option to filter IPs with >1 scan
5. **IP Timeline** - Drill down into individual IP scanning patterns
   - View multiple timelines in one session
   - See first/last scan, duration, frequency
   - Time gap analysis (average, shortest, longest)
   - Chronological scan list

### Example Output

```
Found 74 port scan incidents:

Source IP          Timestamp
============================================================
172.24.22.240      2026-02-25 08:37:03
172.24.22.99       2026-02-23 13:06:36
...

PORT SCAN ANALYSIS - GROUPED BY SOURCE IP
============================================================
Source IP          Scan Count   Percentage
------------------------------------------------------------
172.24.21.62       19             25.7%
172.24.21.99       10             13.5%
...

FREQUENCY ANALYSIS
============================================================
Time Period: 2025-01-21 to 2026-02-25
Duration: 401 days
Average scans per day: 0.2

Monthly Distribution:
------------------------------------------------------------
2026-02:  11 █████
2026-01:  11 █████
...

Show repeat offenders (IPs with >1 scan)? (y/n): y

REPEAT OFFENDERS (Excluding Single-Scan IPs)
============================================================
Rank   Source IP          Scan Count
------------------------------------------------------------
1      172.24.21.62       19
2      172.24.21.99       10
...

Show timeline for a specific IP? (y/n): y

TIMELINE FOR 172.24.21.62
============================================================
First scan: 2025-11-20 21:19:14
Last scan:  2026-02-21 02:03:19
Duration:   92 days
Total scans: 19
Average frequency: 0.21 scans/day

Time between scans:
  Average: 122.9 hours
  Shortest: 11.8 hours
  Longest: 654.1 hours
...
```

## API Reference

Uses Thinkst Canary API v1:
- `/api/v1/incidents/all` - Retrieve incidents
- `/api/v1/devices/all` - List Canary devices

## Requirements

- Python 3.6+
- Dependencies: `requests`, `python-dotenv` (auto-installed via requirements.txt)

## Getting Your API Key

1. Log into your Canary console: `https://your-console.canary.tools`
2. Navigate to **Settings** → **API**
3. Generate or copy your API key
4. Add to `.env` file

## Deployment

See [DEPLOY.md](DEPLOY.md) for detailed deployment instructions including:
- Quick deployment steps
- Troubleshooting
- Security best practices

## Security Notes

- Never commit `.env` file (already in `.gitignore`)
- Regenerate API keys periodically
- API keys are loaded automatically from `.env` file

## License

MIT License - See LICENSE file for details

## Repository

https://github.com/pwhitlow/canaryscanners
