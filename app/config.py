"""Configuration management for Content Manager"""
import os
from typing import Optional

class Config:
    """Application configuration"""
    
    # Data source URLs
    WILD_APRICOT_URL: str = os.getenv(
        'WILD_APRICOT_URL',
        'https://wautils.nova-labs.org/api/digital_sign/events'
    )
    
    SKEDDA_ICAL_URL: str = os.getenv(
        'SKEDDA_ICAL_URL',
        'https://novalabs.skedda.com/ical?k=6uXn10Wdzz_QolZkWb4IduCRE8QKY2M1&i=774516'
    )
    
    # Timeout settings (seconds)
    FETCH_TIMEOUT: int = int(os.getenv('FETCH_TIMEOUT', '10'))
    
    # Default settings
    DEFAULT_FORMAT: str = 'desktop'
    DEFAULT_SOURCE: str = 'all'
    DEFAULT_DATE_RANGE: str = 'this-week'
    
    # Filter past events by default
    FILTER_PAST_EVENTS: bool = os.getenv('FILTER_PAST_EVENTS', 'true').lower() == 'true'
    
    # QR code settings
    QR_CODE_ERROR_CORRECTION: str = 'M'  # Medium error correction
    QR_CODE_SIZE: int = 10
    QR_CODE_BORDER: int = 4
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Application settings
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG: bool = os.getenv('DEBUG', 'false').lower() == 'true'
