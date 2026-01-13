"""Data merging logic"""
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def merge_events_and_reservations(
    events: List[Dict],
    reservations: List[Dict]
) -> List[Dict]:
    """Merge events and reservations into a single list"""
    merged = []
    
    # Add all events
    merged.extend(events)
    
    # Add all reservations
    merged.extend(reservations)
    
    logger.info(f"Merged {len(events)} events and {len(reservations)} reservations into {len(merged)} items")
    
    return merged

