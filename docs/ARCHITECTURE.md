# Content Manager Architecture

## Overview
The content-manager application aggregates event data from multiple sources (Wild Apricot events and Skedda reservations) and displays them in a unified calendar view for the Nova Labs digital signage system.

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     External Data Sources                    │
├─────────────────────────────────────────────────────────────┤
│  Wild Apricot Events API           Skedda Bookings (iCal)   │
│  https://wautils.nova-labs.org/    bookings.ics             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Fetchers                           │
├─────────────────────────────────────────────────────────────┤
│  wild_apricot.py                   skedda.py                │
│  - Fetch JSON events               - Parse iCal format       │
│  - Parse ISO 8601 dates            - Extract reservations    │
│  - Extract metadata                - Calculate durations     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Data Processors                          │
├─────────────────────────────────────────────────────────────┤
│  normalizer.py    │  filter.py    │  organizer.py           │
│  - Normalize      │  - Date range │  - Sort by date         │
│    event data     │    filtering  │  - Group events         │
│  - Standardize    │  - Status     │  - Calculate            │
│    fields         │    filtering  │    durations            │
├───────────────────┴───────────────┴─────────────────────────┤
│  merger.py                                                   │
│  - Combine Wild Apricot + Skedda data                       │
│  - Remove duplicates                                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                         Routes                               │
├─────────────────────────────────────────────────────────────┤
│  /                    - Health check / basic info           │
│  /display             - Main calendar display               │
│  /qr                  - Generate QR codes                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Templates                               │
├─────────────────────────────────────────────────────────────┤
│  desktop.html    │  kiosk.html    │  mobile.html            │
│  - Full layout   │  - Digital     │  - Responsive           │
│                  │    signage     │    mobile view          │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **Data Fetching**
   - Wild Apricot: GET request to JSON API, returns list of events with metadata
   - Skedda: Parse iCal file for room reservations

2. **Data Normalization**
   - Convert to common event format: `{uid, name, location, start_date, end_date, access_status, ...}`
   - Parse dates to datetime objects
   - Calculate event durations

3. **Data Filtering**
   - Apply date range filters (today, this-week, this-month, etc.)
   - Filter by event status (active, full, cancelled)

4. **Data Organization**
   - Sort events chronologically
   - Group by date or location
   - Calculate display metadata (time until start, capacity, etc.)

5. **Rendering**
   - Select template based on device type
   - Apply CSS styling
   - Generate HTML output

## Technology Stack

- **Framework**: Flask (Python web framework)
- **Server**: Gunicorn WSGI server
- **Web Server**: Apache (reverse proxy)
- **Service Management**: systemd
- **Dependencies**: See requirements.txt

## Configuration

Configuration is managed through `app/config.py`:
- Data source URLs
- Display settings
- Caching parameters

Environment variables can override defaults:
- `WILD_APRICOT_URL`
- `SKEDDA_ICS_URL`

## Event Data Model

### Wild Apricot Events
```json
{
  "uid": 12345,
  "name": "WW_S01: Yellow Tools - Woodshop Basic Sign-off",
  "location": "Wood Shop Main Zone",
  "start_date": "2026-01-15T18:00:00-05:00",
  "registrations_limit": 6,
  "active_registrations_count": 4,
  "access_status": "open|limited|full"
}
```

### Skedda Reservations
```json
{
  "uid": "booking-id",
  "name": "John Doe - Conference Room",
  "location": "Classroom 1",
  "start_date": "2026-01-15T14:00:00-05:00",
  "end_date": "2026-01-15T16:00:00-05:00"
}
```

## Display Views

### Desktop View
- Full calendar with all event details
- Multi-column layout
- Complete event descriptions

### Kiosk View (Digital Signage)
- Large text for readability at distance
- Auto-refresh capability
- Simplified event cards
- Focus on upcoming events

### Mobile View
- Responsive single-column layout
- Touch-friendly interface
- Compact event cards

## API Endpoints

### GET /
Returns basic info and health status

### GET /display
Query parameters:
- `range`: Date range filter (today, this-week, this-month, etc.)
- `view`: Display template (desktop, kiosk, mobile)
- `location`: Filter by location

### GET /qr
Generate QR code for portal links
Query parameters:
- `data`: URL or data to encode

## Utilities

### Query Parser (`utils/query_parser.py`)
- Parse and validate query parameters
- Handle date range calculations

### Text Cleaner (`utils/text_cleaner.py`)
- Sanitize event names and descriptions
- Remove HTML entities
- Format display text

### QR Code Generator (`utils/qrcode_gen.py`)
- Generate QR codes for portal links
- Return PNG images

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────┐
│  Apache HTTP Server (ports 80/443)                       │
│  - SSL termination                                        │
│  - Reverse proxy to gunicorn                             │
└──────────────────────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│  Gunicorn WSGI Server (port 8000)                        │
│  - 2 worker processes                                     │
│  - 30 second timeout                                      │
└──────────────────────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│  Content Manager Flask Application                       │
│  /home/sklosky/content-manager                           │
└──────────────────────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│  External Data Sources                                    │
│  - Wild Apricot API                                       │
│  - Skedda iCal feed                                       │
└──────────────────────────────────────────────────────────┘
```

## Security Considerations

- Service runs as unprivileged user (sklosky)
- No sensitive credentials in code (use environment variables)
- Apache handles SSL/TLS termination
- Rate limiting on external API calls
- Input validation on query parameters
