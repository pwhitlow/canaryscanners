# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based utility for retrieving events and incidents from Thinkst Canary honeypot devices via their REST API. Thinkst Canary is a deception technology platform that deploys honeypots to detect network intrusions.

## Running the Script

```bash
# Install dependencies
pip install -r requirements.txt

# Set credentials (required)
export CANARY_CONSOLE_DOMAIN='your-console.canary.tools'
export CANARY_API_KEY='your-api-key-here'

# Run the main script
python canary_events.py
```

## Architecture

**Single Module Design**: The entire application is contained in `canary_events.py` with:
- `CanaryAPI` class: Handles all API communication with the Canary console
- Authentication via API token passed as query parameter
- Methods for retrieving incidents (all, unacknowledged) and devices

**API Structure**:
- Base URL: `https://{console_domain}/api/v1`
- Authentication: Query parameter `auth_token` added to all requests
- Response format: JSON with `result` field indicating success/failure

## Credentials

Credentials are loaded from environment variables (`CANARY_CONSOLE_DOMAIN` and `CANARY_API_KEY`). Never commit actual credentials. The `.env` file is gitignored.

## Thinkst Canary API Notes

- API version: v1
- All requests require `auth_token` query parameter
- Incidents contain: id, description, timestamp (unix), src_host, dst_host, node_id, acknowledged status
- API returns JSON with structure: `{"result": "success", "incidents": [...], ...}`
