"""Utility functions for cleaning text from iCal vText objects"""
from typing import Any, Optional

def clean_ical_text(value: Any) -> Optional[str]:
    """
    Clean text from iCal objects (vText, lists, etc.)
    Returns a clean string or None
    """
    if value is None:
        return None
    
    # Handle vText objects
    if hasattr(value, 'to_ical'):
        try:
            result = value.to_ical().decode('utf-8')
            result = result.strip() if result else None
        except:
            result = str(value).strip() if str(value) else None
    # Handle lists
    elif isinstance(value, list):
        # Join list items, cleaning each one
        cleaned_items = [clean_ical_text(item) for item in value if item]
        cleaned_items = [item for item in cleaned_items if item]
        if cleaned_items:
            result = ', '.join(cleaned_items)
        else:
            result = None
    else:
        # Regular string
        result = str(value).strip() if str(value) else None
    
    # Clean up iCal escape sequences
    if result:
        # Remove escaped commas and semicolons (iCal escaping)
        result = result.replace('\\,', ',')
        result = result.replace('\\;', ';')
        result = result.replace('\\n', ' ')
        result = result.replace('\\N', ' ')
        # Remove any remaining backslashes before common punctuation
        result = result.replace('\\', '')
        # Clean up multiple spaces
        result = ' '.join(result.split())
    
    return result if result else None

