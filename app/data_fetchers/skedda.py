"""Skedda iCal data fetcher"""
import logging
import requests
from icalendar import Calendar
from datetime import datetime
from typing import List, Dict, Optional
from app.config import Config
from app.utils.text_cleaner import clean_ical_text

logger = logging.getLogger(__name__)

def fetch_skedda_reservations() -> List[Dict]:
    """
    Fetch reservations from Skedda iCal feed.
    Returns list of reservation dictionaries.
    Handles missing fields gracefully.
    """
    try:
        response = requests.get(
            Config.SKEDDA_ICAL_URL,
            timeout=Config.FETCH_TIMEOUT,
            headers={'User-Agent': 'Content-Manager/1.0'}
        )
        response.raise_for_status()
        
        cal = Calendar.from_ical(response.text)
        reservations = []
        
        for component in cal.walk('VEVENT'):
            try:
                reservation = parse_vevent(component)
                if reservation:
                    reservations.append(reservation)
            except Exception as e:
                logger.warning(f"Error parsing VEVENT: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(reservations)} reservations from Skedda")
        return reservations
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch Skedda data: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching Skedda data: {e}")
        return []


def parse_vevent(component) -> Optional[Dict]:
    """Parse a VEVENT component from iCal"""
    try:
        reservation = {
            'source': 'skedda',
            'id': None,
            'title': None,
            'location': None,
            'space': None,
            'start_date': None,
            'start_time': None,
            'end_date': None,
            'end_time': None,
            'start_datetime': None,
            'end_datetime': None,
            'duration': None,
            'status': None,
            'reserved_by': None,
            'description': None
        }
        
        # Extract UID
        if 'UID' in component:
            reservation['id'] = str(component.get('UID'))
        
        # Extract SUMMARY (title)
        if 'SUMMARY' in component:
            reservation['title'] = clean_ical_text(component.get('SUMMARY'))
        
        # Extract DESCRIPTION
        if 'DESCRIPTION' in component:
            desc = clean_ical_text(component.get('DESCRIPTION'))
            reservation['description'] = desc
            # Try to extract space from description (format: "Spaces: Events Bay Lounge")
            if desc and 'Spaces:' in desc:
                try:
                    space = desc.split('Spaces:')[-1].strip()
                    reservation['space'] = space
                    reservation['location'] = space  # location and space are synonymous
                except:
                    pass
        
        # Extract RESOURCES (space/location)
        if 'RESOURCES' in component:
            space = clean_ical_text(component.get('RESOURCES'))
            if space:
                reservation['space'] = space
                reservation['location'] = space
        
        # Extract DTSTART
        if 'DTSTART' in component:
            dt_start = component.get('DTSTART').dt
            if isinstance(dt_start, datetime):
                reservation['start_datetime'] = dt_start
                reservation['start_date'] = dt_start.strftime('%Y-%m-%d')
                reservation['start_time'] = dt_start.strftime('%I:%M %p')
            elif hasattr(dt_start, 'date'):
                reservation['start_date'] = dt_start.date().strftime('%Y-%m-%d')
        
        # Extract DTEND
        if 'DTEND' in component:
            dt_end = component.get('DTEND').dt
            if isinstance(dt_end, datetime):
                reservation['end_datetime'] = dt_end
                reservation['end_date'] = dt_end.strftime('%Y-%m-%d')
                reservation['end_time'] = dt_end.strftime('%I:%M %p')
                # Calculate duration
                if reservation['start_datetime']:
                    duration = dt_end - reservation['start_datetime']
                    reservation['duration'] = int(duration.total_seconds() / 60)  # minutes
            elif hasattr(dt_end, 'date'):
                reservation['end_date'] = dt_end.date().strftime('%Y-%m-%d')
        
        # Extract STATUS
        if 'STATUS' in component:
            reservation['status'] = clean_ical_text(component.get('STATUS')) or 'CONFIRMED'
        
        # Only return reservation if it has at least a title or location
        if reservation['title'] or reservation['location']:
            return reservation
        
        return None
        
    except Exception as e:
        logger.warning(f"Error parsing VEVENT: {e}")
        return None

