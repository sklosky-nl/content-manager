# Content Manager - Event and Reservation Display System

A web-based system that aggregates event information from Wild Apricot and reservation information from Skedda, displaying them in multiple formats optimized for different consumers, particularly Xibo kiosk displays.

## Features

- **Real-time Data Retrieval**: Fetches data from both sources on every request
- **Multiple Display Formats**: Kiosk, Mobile, Desktop, and Print formats
- **Flexible Filtering**: Filter by date, location, source, and more via URL query parameters
- **QR Code Generation**: Generate QR codes for direct page access
- **Graceful Error Handling**: Works even when data sources are unavailable or fields are missing
- **Browser Compatibility**: Designed for older browsers (IE11, Fire OS) and modern browsers

## Quick Start

### Production Deployment (Linux/Gunicorn)

The application runs natively on Linux using Gunicorn WSGI server:

```bash
# Install dependencies
cd /home/sklosky/content-manager
pip install -r requirements.txt

# Run with Gunicorn (production)
gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 30 wsgi:app

# Or use systemd service (recommended)
sudo systemctl start content-manager
```

The application will be available at `http://localhost:8000`

### Development Server

```bash
cd /home/sklosky/content-manager
pip install -r requirements.txt
python run.py
```

## Configuration

Configuration is managed through environment variables. See `.env.example` for available options.

Default test feed URLs:
- Wild Apricot: `http://localhost/events/test/wild-apricot.html`
- Skedda: `http://localhost/events/test/bookings.ics`

## Usage

### Master Page
- `/` - Master page with links and QR codes

### Display Pages
- `/display` - Main display page with filtering

### Query Parameters

**Date Filtering:**
- `?date=2025-12-15` - Specific date
- `?range=today` - Today's events
- `?range=this-week` - This week
- `?start=2025-12-01&end=2025-12-31` - Date range

**Location/Space Filtering:**
- `?location=Events Bay` or `?space=Events Bay` - Filter by location

**Source Filtering:**
- `?source=wild-apricot` - Wild Apricot only
- `?source=skedda` - Skedda only
- `?source=all` - All sources (default)

**Format Selection:**
- `?format=kiosk` - Kiosk format
- `?format=mobile` - Mobile format
- `?format=desktop` - Desktop format (default)
- `?format=print` - Print format

**Combined Examples:**
- `?range=today&format=kiosk&source=all`
- `?range=this-week&location=Events Bay&format=desktop`

## Architecture

- **Web Server**: Apache (reverse proxy on ports 80/443)
- **Application Server**: Gunicorn WSGI server (port 8000)
- **Framework**: Python Flask
- **Data Sources**: Wild Apricot JSON API and Skedda iCal
- **Deployment**: Native Linux with systemd service management

## Project Structure

```
content-manager/
├── app/
│   ├── data_fetchers/     # Data fetching modules
│   ├── processors/         # Data processing modules
│   ├── templates/          # HTML templates
│   ├── static/             # CSS, JS, images
│   ├── utils/              # Utility modules
│   └── config.py           # Configuration
├── requirements.txt        # Python dependencies
├── wsgi.py                 # WSGI entry point (Gunicorn)
├── run.py                  # Development server
└── content-manager.service # systemd service file
```

## Notes

- The system handles missing fields gracefully
- Data is fetched fresh on every request (no caching)
- Compatible with Xibo 3.1.2, Gen2 Firesticks, and Windows 7 browsers
- Apache is already configured to route `/events/*` to this application

