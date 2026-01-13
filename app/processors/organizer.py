"""Data organization and sorting"""
import logging
from datetime import date, datetime
from typing import List, Dict
from collections import defaultdict

logger = logging.getLogger(__name__)

def organize_by_date(items: List[Dict]) -> Dict[date, List[Dict]]:
    """Organize items by date"""
    organized = defaultdict(list)
    
    for item in items:
        item_date = get_item_date(item)
        if item_date:
            organized[item_date].append(item)
        else:
            # Items without dates go into a special key
            organized[None].append(item)
    
    # Sort items within each date by start time
    for date_key in organized:
        organized[date_key] = sort_by_time(organized[date_key])
    
    return dict(organized)


def sort_by_time(items: List[Dict]) -> List[Dict]:
    """Sort items by start time"""
    def get_sort_key(item):
        # Try start_datetime first
        if item.get('start_datetime'):
            dt = item['start_datetime']
            if isinstance(dt, datetime):
                # Ensure datetime is naive (no timezone) for comparison
                if hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
                    dt = dt.replace(tzinfo=None)
                return dt
            elif isinstance(dt, date):
                return dt
        # Try start_time string
        if item.get('start_time'):
            try:
                # Parse time like "07:00 PM"
                time_str = item['start_time']
                return datetime.strptime(time_str, '%I:%M %p').time()
            except:
                pass
        # Fallback to title
        return item.get('title', '')
    
    return sorted(items, key=get_sort_key)


def get_item_date(item: Dict) -> date:
    """Extract date from item"""
    # Try start_datetime first
    if item.get('start_datetime'):
        dt = item['start_datetime']
        if isinstance(dt, datetime):
            return dt.date()
        elif isinstance(dt, date):
            return dt
    
    # Try start_date string
    if item.get('start_date'):
        date_str = item['start_date']
        try:
            if isinstance(date_str, date):
                return date_str
            elif '/' in date_str:
                # MM/DD/YYYY format
                return datetime.strptime(date_str, '%m/%d/%Y').date()
            else:
                # YYYY-MM-DD format
                return datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            pass
    
    return None

