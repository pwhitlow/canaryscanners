# Canary Scanners

A Python script for retrieving events and incidents from Thinkst Canary honeypot devices via the Canary API.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your Canary credentials:
```bash
export CANARY_CONSOLE_DOMAIN='your-console.canary.tools'
export CANARY_API_KEY='your-api-key-here'
```

Alternatively, copy `.env.example` to `.env` and fill in your credentials.

## Usage

Run the script to fetch recent incidents:
```bash
python canary_events.py
```

## API Reference

The script uses the Thinkst Canary API v1. Key endpoints:
- `/incidents/all` - Retrieve all incidents
- `/incidents/unacknowledged` - Retrieve unacknowledged incidents
- `/devices/all` - List all Canary devices

## Authentication

The script requires:
- **Console Domain**: Your Canary console domain (e.g., `1234abc.canary.tools`)
- **API Key**: Generated from your Canary console under Settings → API

## Output

The script displays:
- Incident details (ID, description, timestamp, source/destination IPs)
- Count of unacknowledged incidents
- Number of active Canary devices
