"""Data normalization for events and reservations"""
import logging
from datetime import datetime
from typing import Dict, Optional
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)

def normalize_event(event: Dict) -> Dict:
    """Normalize a Wild Apricot event"""
    normalized = {
        'source': event.get('source', 'wild-apricot'),
        'id': event.get('id') or event.get('event_id'),
        'title': event.get('title', 'Untitled Event'),
        'location': normalize_location(event.get('location')),
        'space': normalize_location(event.get('location')),  # location and space are synonymous
        'start_datetime': normalize_datetime(event),
        'end_datetime': None,  # Wild Apricot HTML doesn't provide end time
        'start_date': None,
        'start_time': None,
        'end_date': None,
        'end_time': None,
        'access_status': event.get('access_status', 'unknown'),
        'capacity': event.get('capacity'),
        'enrollment': event.get('enrollment'),
        'description': event.get('description')
    }
    
    # Extract date/time from start_datetime
    if normalized['start_datetime']:
        normalized['start_date'] = normalized['start_datetime'].strftime('%Y-%m-%d')
        normalized['start_time'] = normalized['start_datetime'].strftime('%I:%M %p')
    
    return normalized


def normalize_reservation(reservation: Dict) -> Dict:
    """Normalize a Skedda reservation"""
    # Convert timezone-aware datetimes to naive (remove timezone info)
    start_dt = reservation.get('start_datetime')
    if start_dt and hasattr(start_dt, 'tzinfo') and start_dt.tzinfo is not None:
        # Convert to naive datetime (local time)
        start_dt = start_dt.replace(tzinfo=None)
    
    end_dt = reservation.get('end_datetime')
    if end_dt and hasattr(end_dt, 'tzinfo') and end_dt.tzinfo is not None:
        # Convert to naive datetime (local time)
        end_dt = end_dt.replace(tzinfo=None)
    
    normalized = {
        'source': reservation.get('source', 'skedda'),
        'id': reservation.get('id'),
        'title': reservation.get('title', 'Reservation'),
        'location': normalize_location(reservation.get('location') or reservation.get('space')),
        'space': normalize_location(reservation.get('space') or reservation.get('location')),
        'start_datetime': start_dt,
        'end_datetime': end_dt,
        'start_date': reservation.get('start_date'),
        'start_time': reservation.get('start_time'),
        'end_date': reservation.get('end_date'),
        'end_time': reservation.get('end_time'),
        'duration': reservation.get('duration'),
        'status': reservation.get('status', 'CONFIRMED'),
        'description': reservation.get('description')
    }
    
    return normalized


def normalize_location(location: Optional[str]) -> Optional[str]:
    """Normalize location/space name (case-insensitive, trim whitespace)"""
    if not location:
        return None
    return location.strip()


def normalize_datetime(event: Dict) -> Optional[datetime]:
    """Normalize datetime from various formats"""
    # Try start_datetime first
    if event.get('start_datetime'):
        if isinstance(event['start_datetime'], datetime):
            return event['start_datetime']
    
    # Try parsing from date and time strings
    if event.get('start_date') and event.get('start_time'):
        try:
            date_str = f"{event['start_date']} {event['start_time']}"
            # Handle different date formats
            if '/' in event['start_date']:
                # Format: MM/DD/YYYY
                dt_str = date_str.replace('/', '-')
                # Try parsing
                try:
                    return date_parser.parse(date_str, fuzzy=True)
                except:
                    pass
            else:
                try:
                    return date_parser.parse(date_str, fuzzy=True)
                except:
                    pass
        except Exception as e:
            logger.debug(f"Could not parse datetime: {e}")
    
    # Try parsing just date
    if event.get('start_date'):
        try:
            if '/' in event['start_date']:
                # MM/DD/YYYY format
                return datetime.strptime(event['start_date'], '%m/%d/%Y')
            else:
                return date_parser.parse(event['start_date'])
        except:
            pass
    
    return None

