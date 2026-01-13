"""Data filtering logic"""
import logging
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)

def filter_by_date_range(
    items: List[Dict],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    date_range: Optional[str] = None,
    specific_date: Optional[date] = None
) -> List[Dict]:
    """Filter items by date range"""
    if not items:
        return []
    
    # Determine date range
    today = date.today()
    
    if specific_date:
        start_date = specific_date
        end_date = specific_date
    elif date_range:
        if date_range == 'today':
            start_date = today
            end_date = today
        elif date_range == 'tomorrow':
            start_date = today + timedelta(days=1)
            end_date = start_date
        elif date_range == 'this-week':
            # Start of week (Monday)
            days_since_monday = today.weekday()
            start_date = today - timedelta(days=days_since_monday)
            end_date = start_date + timedelta(days=6)
        elif date_range == 'next-week':
            days_since_monday = today.weekday()
            start_date = today - timedelta(days=days_since_monday) + timedelta(days=7)
            end_date = start_date + timedelta(days=6)
        elif date_range == 'this-month':
            start_date = today.replace(day=1)
            end_date = (start_date + relativedelta(months=1)) - timedelta(days=1)
        elif date_range == 'next-month':
            start_date = (today.replace(day=1) + relativedelta(months=1))
            end_date = (start_date + relativedelta(months=1)) - timedelta(days=1)
        elif date_range == 'next-10-days':
            start_date = today
            end_date = today + timedelta(days=9)  # 9 days from today = 10 days total including today
    
    if not start_date and not end_date:
        return items  # No date filter
    
    filtered = []
    for item in items:
        item_date = get_item_date(item)
        if item_date:
            if start_date and end_date:
                if start_date <= item_date <= end_date:
                    filtered.append(item)
            elif start_date:
                if item_date >= start_date:
                    filtered.append(item)
            elif end_date:
                if item_date <= end_date:
                    filtered.append(item)
        else:
            # Include items without dates if no filter specified
            if not start_date and not end_date:
                filtered.append(item)
    
    return filtered


def filter_by_location(items: List[Dict], location: Optional[str]) -> List[Dict]:
    """Filter items by location/space (case-insensitive partial match)"""
    if not location or not items:
        return items
    
    location_lower = location.lower().strip()
    filtered = []
    
    for item in items:
        item_location = (item.get('location') or item.get('space') or '').lower()
        if location_lower in item_location:
            filtered.append(item)
    
    return filtered


def filter_by_source(items: List[Dict], source: str) -> List[Dict]:
    """Filter items by data source"""
    if source == 'all' or not source:
        return items
    
    return [item for item in items if item.get('source') == source]


def filter_past_events(items: List[Dict], filter_past: bool = True) -> List[Dict]:
    """Filter out past events/reservations"""
    if not filter_past or not items:
        return items
    
    today = date.today()
    filtered = []
    
    for item in items:
        item_date = get_item_date(item)
        if item_date:
            # Include if today or future
            if item_date >= today:
                filtered.append(item)
        else:
            # Include items without dates
            filtered.append(item)
    
    return filtered


def get_item_date(item: Dict) -> Optional[date]:
    """Extract date from item (start_date or start_datetime)"""
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

