"""Query parameter parsing and validation"""
import logging
from datetime import datetime, date
from typing import Dict, Optional
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)

def parse_query_params(request_args: Dict) -> Dict:
    """Parse and validate query parameters"""
    params = {
        'date': None,
        'start': None,
        'end': None,
        'range': None,
        'location': None,
        'space': None,
        'source': 'all',
        'format': 'desktop',
        'filter_past': True
    }
    
    # Date parameter
    if 'date' in request_args:
        try:
            date_str = request_args['date']
            params['date'] = parse_date(date_str)
        except Exception as e:
            logger.warning(f"Invalid date parameter: {e}")
    
    # Start date
    if 'start' in request_args:
        try:
            params['start'] = parse_date(request_args['start'])
        except Exception as e:
            logger.warning(f"Invalid start date: {e}")
    
    # End date
    if 'end' in request_args:
        try:
            params['end'] = parse_date(request_args['end'])
        except Exception as e:
            logger.warning(f"Invalid end date: {e}")
    
    # Range parameter
    if 'range' in request_args:
        range_val = request_args['range'].lower()
        valid_ranges = ['today', 'tomorrow', 'this-week', 'next-week', 'this-month', 'next-month', 'next-10-days']
        if range_val in valid_ranges:
            params['range'] = range_val
    
    # Location/Space (synonymous)
    if 'location' in request_args:
        params['location'] = request_args['location'].strip()
        params['space'] = params['location']  # location and space are synonymous
    elif 'space' in request_args:
        params['space'] = request_args['space'].strip()
        params['location'] = params['space']
    
    # Source filter
    if 'source' in request_args:
        source_val = request_args['source'].lower()
        valid_sources = ['wild-apricot', 'skedda', 'all']
        if source_val in valid_sources:
            params['source'] = source_val
    
    # Format
    if 'format' in request_args:
        format_val = request_args['format'].lower()
        valid_formats = ['kiosk', 'mobile', 'desktop', 'print']
        if format_val in valid_formats:
            params['format'] = format_val
    
    return params


def parse_date(date_str: str) -> date:
    """Parse date string to date object"""
    try:
        # Try ISO format first (YYYY-MM-DD)
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        try:
            # Try MM/DD/YYYY
            return datetime.strptime(date_str, '%m/%d/%Y').date()
        except:
            # Try dateutil parser
            return date_parser.parse(date_str).date()

