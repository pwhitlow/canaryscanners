#!/usr/bin/env python3
"""
Thinkst Canary Event Retriever

Retrieves and displays events/incidents from Thinkst Canary API.
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Optional, Dict, List


class CanaryAPI:
    """Client for interacting with Thinkst Canary API"""

    def __init__(self, console_domain: str, api_key: str):
        """
        Initialize Canary API client

        Args:
            console_domain: Your Canary console domain (e.g., '1234abc.canary.tools')
            api_key: Your API authentication token
        """
        self.base_url = f"https://{console_domain}/api/v1"
        self.api_key = api_key
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make authenticated request to Canary API

        Args:
            endpoint: API endpoint (e.g., '/incidents/all')
            params: Optional query parameters

        Returns:
            JSON response as dictionary
        """
        if params is None:
            params = {}

        params['auth_token'] = self.api_key

        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}", file=sys.stderr)
            sys.exit(1)

    def get_all_incidents(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Retrieve all incidents

        Args:
            limit: Optional limit on number of incidents to retrieve

        Returns:
            List of incident dictionaries
        """
        params = {}
        if limit:
            params['limit'] = limit

        response = self._make_request('/incidents/all', params)

        if response.get('result') == 'success':
            return response.get('incidents', [])
        else:
            print(f"Error retrieving incidents: {response}", file=sys.stderr)
            return []

    def get_unacknowledged_incidents(self) -> List[Dict]:
        """
        Retrieve only unacknowledged incidents

        Returns:
            List of unacknowledged incident dictionaries
        """
        response = self._make_request('/incidents/unacknowledged')

        if response.get('result') == 'success':
            return response.get('incidents', [])
        else:
            print(f"Error retrieving unacknowledged incidents: {response}", file=sys.stderr)
            return []

    def get_devices(self) -> List[Dict]:
        """
        Retrieve all Canary devices

        Returns:
            List of device dictionaries
        """
        response = self._make_request('/devices/all')

        if response.get('result') == 'success':
            return response.get('devices', [])
        else:
            print(f"Error retrieving devices: {response}", file=sys.stderr)
            return []


def format_incident(incident: Dict) -> str:
    """Format incident for display"""
    # The Canary API nests actual incident data inside 'description' field
    incident_data = incident.get('description', {})

    # Handle timestamp - API returns it as string
    timestamp_str = incident_data.get('created', '0')
    timestamp = datetime.fromtimestamp(int(timestamp_str))

    # Convert acknowledged string to boolean
    acknowledged = incident_data.get('acknowledged', 'False') == 'True'

    return f"""
Incident ID: {incident.get('id')}
Type: {incident_data.get('description', 'N/A')}
Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
Source IP: {incident_data.get('src_host', 'N/A')}
Destination: {incident_data.get('dst_host', 'N/A')}
Device Name: {incident_data.get('name', 'N/A')}
Device ID: {incident_data.get('node_id', 'N/A')}
Flock: {incident_data.get('flock_name', 'N/A')}
Acknowledged: {acknowledged}
{"="*60}"""


def main():
    """Main execution function"""
    # Get credentials from environment variables
    console_domain = os.getenv('CANARY_CONSOLE_DOMAIN')
    api_key = os.getenv('CANARY_API_KEY')

    if not console_domain or not api_key:
        print("Error: Required environment variables not set", file=sys.stderr)
        print("Please set CANARY_CONSOLE_DOMAIN and CANARY_API_KEY", file=sys.stderr)
        print("\nExample:")
        print("  export CANARY_CONSOLE_DOMAIN='1234abc.canary.tools'")
        print("  export CANARY_API_KEY='your-api-key-here'")
        sys.exit(1)

    # Initialize API client
    api = CanaryAPI(console_domain, api_key)

    # Retrieve incidents
    print("Fetching incidents from Canary console...")
    print("="*60)

    incidents = api.get_all_incidents(limit=50)

    if not incidents:
        print("No incidents found.")
    else:
        print(f"\nFound {len(incidents)} incidents:\n")
        for incident in incidents:
            print(format_incident(incident))

    # Show unacknowledged count
    unack_incidents = api.get_unacknowledged_incidents()
    print(f"\n{len(unack_incidents)} unacknowledged incidents")

    # Show device count
    devices = api.get_devices()
    print(f"{len(devices)} active Canary devices")


if __name__ == '__main__':
    main()
