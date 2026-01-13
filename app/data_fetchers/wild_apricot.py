"""Wild Apricot JSON API data fetcher"""
import logging
import requests
from datetime import datetime
from typing import List, Dict, Optional
from app.config import Config

logger = logging.getLogger(__name__)

def fetch_wild_apricot_events() -> List[Dict]:
    """
    Fetch events from Wild Apricot JSON API.
    Returns list of event dictionaries.
    Handles missing fields gracefully.
    """
    try:
        response = requests.get(
            Config.WILD_APRICOT_URL,
            timeout=Config.FETCH_TIMEOUT,
            headers={'User-Agent': 'Content-Manager/1.0'}
        )
        response.raise_for_status()
        
        data = response.json()
        events = []
        
        # The API returns {"generated_at": "...", "events": [...]}
        if 'events' not in data:
            logger.warning("No 'events' key found in API response")
            return []
        
        for event_data in data['events']:
            try:
                event = parse_event_data(event_data)
                if event:
                    events.append(event)
            except Exception as e:
                logger.warning(f"Error parsing event: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(events)} events from Wild Apricot API")
        return events
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch Wild Apricot data: {e}")
        return []
    except ValueError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching Wild Apricot data: {e}")
        return []


def parse_event_data(event_data: Dict) -> Optional[Dict]:
    """Parse a single event from the JSON API"""
    try:
        # Extract basic information
        event = {
            'source': 'wild-apricot',
            'id': str(event_data.get('uid', '')),
            'event_id': str(event_data.get('uid', '')),
            'title': event_data.get('name', ''),
            'location': event_data.get('location', ''),
            'event_type': event_data.get('event_type', ''),
        }
        
        # Parse start date
        start_date_str = event_data.get('start_date')
        if start_date_str:
            try:
                # Parse ISO 8601 format: "2026-01-12T19:00:00.000-05:00"
                dt = datetime.fromisoformat(start_date_str)
                event['start_datetime'] = dt
                event['start_date'] = dt.strftime('%m/%d/%Y')
                event['start_time'] = dt.strftime('%I:%M %p')
            except Exception as e:
                logger.debug(f"Could not parse datetime '{start_date_str}': {e}")
                event['start_date'] = start_date_str
        
        # Extract registration information
        event['capacity'] = event_data.get('registrations_limit')
        event['confirmed_registrations'] = event_data.get('confirmed_registrations_count', 0)
        event['active_registrations'] = event_data.get('active_registrations_count', 0)
        event['pending_registrations'] = event_data.get('pending_registrations_count', 0)
        event['enrollment'] = event['active_registrations']
        
        # Determine access status based on registration counts and limits
        capacity = event['capacity']
        active = event['active_registrations']
        
        if capacity is not None and active >= capacity:
            event['access_status'] = 'Full'
        elif 'CANCELED' in event['title'].upper():
            event['access_status'] = 'Canceled'
        else:
            # Try to infer from event name/description
            title_upper = event['title'].upper()
            if 'MEMBERS' in title_upper or 'MEMBER' in title_upper:
                event['access_status'] = 'Members Only'
            else:
                event['access_status'] = 'Open'
        
        # Only return event if it has at least a title
        if event['title']:
            return event
        
        return None
        
    except Exception as e:
        logger.warning(f"Error parsing event data: {e}")
        return None
