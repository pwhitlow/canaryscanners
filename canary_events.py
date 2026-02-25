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
from collections import Counter
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class CanaryAPI:
    """Client for interacting with Thinkst Canary API"""

    def __init__(self, console_domain: str, api_key: str):
        """
        Initialize Canary API client

        Args:
            console_domain: Your Canary console domain (e.g., '1234abc.canary.tools')
            api_key: Your API authentication token
        """
        # Strip protocol if present (handle both http:// and https://)
        console_domain = console_domain.replace('https://', '').replace('http://', '').strip('/')

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


def is_port_scan(incident: Dict) -> bool:
    """Check if incident is a port scan"""
    incident_data = incident.get('description', {})
    incident_type = incident_data.get('description', '')
    return 'Port Scan' in incident_type


def format_incident(incident: Dict) -> str:
    """Format incident for display - simplified for port scans"""
    # The Canary API nests actual incident data inside 'description' field
    incident_data = incident.get('description', {})

    # Handle timestamp - API returns it as string
    timestamp_str = incident_data.get('created', '0')
    timestamp = datetime.fromtimestamp(int(timestamp_str))

    # Get source IP
    src_ip = incident_data.get('src_host', 'N/A')

    return f"{src_ip:<18} {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


def get_incident_ip(incident: Dict) -> str:
    """Extract source IP from incident"""
    incident_data = incident.get('description', {})
    return incident_data.get('src_host', 'Unknown')


def get_incident_timestamp(incident: Dict) -> datetime:
    """Extract timestamp from incident"""
    incident_data = incident.get('description', {})
    timestamp_str = incident_data.get('created', '0')
    return datetime.fromtimestamp(int(timestamp_str))


def analyze_by_ip(port_scans: List[Dict]) -> None:
    """Analyze and display port scans grouped by source IP"""
    # Count occurrences by IP
    ip_counter = Counter([get_incident_ip(inc) for inc in port_scans])

    print("\n" + "="*60)
    print("PORT SCAN ANALYSIS - GROUPED BY SOURCE IP")
    print("="*60)
    print(f"\n{'Source IP':<18} {'Scan Count':<12} {'Percentage'}")
    print("-"*60)

    total_scans = len(port_scans)
    for ip, count in ip_counter.most_common():
        percentage = (count / total_scans) * 100
        print(f"{ip:<18} {count:<12} {percentage:>6.1f}%")

    print(f"\nTotal unique IPs: {len(ip_counter)}")
    print(f"Total port scans: {total_scans}")


def analyze_frequency(port_scans: List[Dict]) -> None:
    """Analyze scanning frequency and patterns"""
    if not port_scans:
        return

    # Get all timestamps
    timestamps = [get_incident_timestamp(inc) for inc in port_scans]
    timestamps.sort()

    # Find date range
    earliest = timestamps[0]
    latest = timestamps[-1]
    days_span = (latest - earliest).days + 1

    # Count by month
    monthly_counts = Counter([ts.strftime('%Y-%m') for ts in timestamps])

    # Get top scanner
    ip_counter = Counter([get_incident_ip(inc) for inc in port_scans])
    top_scanner, top_count = ip_counter.most_common(1)[0]

    print("\n" + "="*60)
    print("FREQUENCY ANALYSIS")
    print("="*60)
    print(f"\nTime Period: {earliest.strftime('%Y-%m-%d')} to {latest.strftime('%Y-%m-%d')}")
    print(f"Duration: {days_span} days")
    print(f"Average scans per day: {len(port_scans) / days_span:.1f}")
    print(f"\nMost active scanner: {top_scanner} ({top_count} scans)")
    print(f"Top scanner percentage: {(top_count / len(port_scans)) * 100:.1f}%")

    print("\n" + "-"*60)
    print("Monthly Distribution:")
    print("-"*60)
    for month in sorted(monthly_counts.keys(), reverse=True):
        count = monthly_counts[month]
        bar = '█' * int(count / 2)
        print(f"{month}: {count:>3} {bar}")


def show_repeat_offenders(port_scans: List[Dict]) -> List[tuple]:
    """Display IPs with multiple scans (exclude single-scan IPs)

    Returns:
        List of (ip, count) tuples for repeat offenders
    """
    # Count occurrences by IP
    ip_counter = Counter([get_incident_ip(inc) for inc in port_scans])

    # Filter to only IPs with more than 1 scan
    repeat_offenders = [(ip, count) for ip, count in ip_counter.items() if count > 1]
    repeat_offenders.sort(key=lambda x: x[1], reverse=True)

    if not repeat_offenders:
        print("\nNo repeat offenders found (all IPs scanned only once).")
        return []

    print("\n" + "="*60)
    print("REPEAT OFFENDERS (Excluding Single-Scan IPs)")
    print("="*60)
    print(f"\n{'Rank':<6} {'Source IP':<18} {'Scan Count'}")
    print("-"*60)

    for rank, (ip, count) in enumerate(repeat_offenders, 1):
        print(f"{rank:<6} {ip:<18} {count}")

    print(f"\nTotal repeat offenders: {len(repeat_offenders)}")
    total_repeat_scans = sum(count for _, count in repeat_offenders)
    print(f"Total scans from repeat offenders: {total_repeat_scans}")
    print(f"Percentage of all scans: {(total_repeat_scans / len(port_scans)) * 100:.1f}%")

    return repeat_offenders


def show_ip_timeline(ip_address: str, port_scans: List[Dict]) -> None:
    """Display detailed timeline for a specific IP address"""
    # Filter scans for this IP
    ip_scans = [inc for inc in port_scans if get_incident_ip(inc) == ip_address]

    if not ip_scans:
        print(f"\nNo scans found for {ip_address}")
        return

    # Sort by timestamp
    ip_scans.sort(key=lambda x: get_incident_timestamp(x))

    # Get timestamps
    timestamps = [get_incident_timestamp(inc) for inc in ip_scans]

    print("\n" + "="*60)
    print(f"TIMELINE FOR {ip_address}")
    print("="*60)

    # Summary statistics
    first_scan = timestamps[0]
    last_scan = timestamps[-1]
    duration = (last_scan - first_scan).days

    print(f"\nFirst scan: {first_scan.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Last scan:  {last_scan.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration:   {duration} days")
    print(f"Total scans: {len(ip_scans)}")

    if duration > 0:
        print(f"Average frequency: {len(ip_scans) / duration:.2f} scans/day")

    # Calculate time gaps between scans
    if len(timestamps) > 1:
        gaps = [(timestamps[i+1] - timestamps[i]).total_seconds() / 3600 for i in range(len(timestamps)-1)]
        avg_gap = sum(gaps) / len(gaps)
        min_gap = min(gaps)
        max_gap = max(gaps)

        print(f"\nTime between scans:")
        print(f"  Average: {avg_gap:.1f} hours")
        print(f"  Shortest: {min_gap:.1f} hours")
        print(f"  Longest: {max_gap:.1f} hours")

    # Display timeline
    print("\n" + "-"*60)
    print("SCAN TIMELINE:")
    print("-"*60)
    print(f"{'#':<4} {'Date':<12} {'Time':<10} {'Days Since Previous'}")
    print("-"*60)

    for idx, (scan, ts) in enumerate(zip(ip_scans, timestamps), 1):
        days_since = ""
        if idx > 1:
            days_diff = (ts - timestamps[idx-2]).days
            days_since = f"{days_diff} days" if days_diff > 0 else "same day"

        print(f"{idx:<4} {ts.strftime('%Y-%m-%d'):<12} {ts.strftime('%H:%M:%S'):<10} {days_since}")

    print("-"*60)


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
    print("Fetching port scan incidents from Canary console...\n")

    incidents = api.get_all_incidents(limit=100)

    # Filter for port scans only
    port_scans = [inc for inc in incidents if is_port_scan(inc)]

    if not port_scans:
        print("No port scan incidents found.")
    else:
        print(f"Found {len(port_scans)} port scan incidents:\n")
        print(f"{'Source IP':<18} {'Timestamp'}")
        print("="*60)
        for incident in port_scans:
            print(format_incident(incident))

        # Display analysis
        analyze_by_ip(port_scans)
        analyze_frequency(port_scans)

        # Offer to show repeat offenders
        print("\n" + "="*60)
        response = input("\nShow repeat offenders (IPs with >1 scan)? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            repeat_offenders = show_repeat_offenders(port_scans)

            # Offer to show timeline for specific IP
            if repeat_offenders:
                print("\n" + "="*60)
                response = input("\nShow timeline for a specific IP? (y/n): ").strip().lower()
                if response in ['y', 'yes']:
                    # Display available IPs with numbers
                    print("\nSelect an IP address:")
                    for idx, (ip, count) in enumerate(repeat_offenders, 1):
                        print(f"  {idx}. {ip} ({count} scans)")

                    # Get user selection
                    try:
                        choice = input("\nEnter number (or IP address): ").strip()

                        # Try to parse as number first
                        if choice.isdigit():
                            idx = int(choice) - 1
                            if 0 <= idx < len(repeat_offenders):
                                selected_ip = repeat_offenders[idx][0]
                            else:
                                print(f"Invalid selection. Please choose 1-{len(repeat_offenders)}")
                                selected_ip = None
                        else:
                            # Treat as IP address
                            selected_ip = choice

                        if selected_ip:
                            show_ip_timeline(selected_ip, port_scans)

                    except (ValueError, IndexError):
                        print("Invalid input.")


if __name__ == '__main__':
    main()
