# Content Manager Repository Structure

## Overview
This directory contains a backup of the Nova Labs content-manager application from the xibo server, formatted for GitHub repository use.

## Backup Details
- **Source**: xibo.space.nova-labs.org:/home/sklosky/content-manager
- **Backup Date**: January 13, 2026
- **Backup File**: content-manager-backup-20260113-163313.tar.gz

## Directory Structure

```
content-manager/
├── .gitignore                              # Git ignore patterns
├── README.md                               # Project overview and quick start
├── requirements.txt                        # Python dependencies
├── run.py                                  # Development server entry point
├── wsgi.py                                 # Production WSGI entry point
│
├── app/                                    # Main application directory
│   ├── __init__.py                        # Flask app initialization
│   ├── config.py                          # Configuration settings
│   ├── routes.py                          # URL routes and views
│   │
│   ├── data_fetchers/                     # External data retrieval
│   │   ├── __init__.py
│   │   ├── wild_apricot.py               # Wild Apricot JSON API client
│   │   └── skedda.py                     # Skedda iCal parser
│   │
│   ├── processors/                        # Data processing pipeline
│   │   ├── __init__.py
│   │   ├── normalizer.py                 # Data normalization
│   │   ├── filter.py                     # Date/location filtering
│   │   ├── organizer.py                  # Data organization
│   │   └── merger.py                     # Multi-source data merging
│   │
│   ├── utils/                             # Utility functions
│   │   ├── __init__.py
│   │   ├── query_parser.py               # Query parameter parsing
│   │   ├── text_cleaner.py               # Text cleaning utilities
│   │   └── qrcode_gen.py                 # QR code generation
│   │
│   ├── static/                            # Static assets
│   │   ├── css/
│   │   │   ├── base.css                  # Base styles
│   │   │   ├── desktop.css               # Desktop view styles
│   │   │   ├── kiosk.css                 # Digital signage styles
│   │   │   ├── mobile.css                # Mobile view styles
│   │   │   └── print.css                 # Print styles
│   │   └── js/
│   │       └── main.js                   # Client-side JavaScript
│   │
│   └── templates/                         # HTML templates
│       ├── base.html                      # Base template
│       ├── master.html                    # Master page template
│       ├── desktop.html                   # Desktop display
│       ├── kiosk.html                     # Kiosk/digital signage
│       ├── mobile.html                    # Mobile display
│       ├── print.html                     # Print format
│       └── error.html                     # Error pages
│
├── docs/                                   # Documentation
│   ├── ARCHITECTURE.md                    # System architecture
│   ├── DEPLOYMENT.md                      # Deployment guide
│   └── DEVELOPMENT.md                     # Development guide
│
├── tests/                                  # Test files
│   └── (test files to be added)
│
└── deployment-scripts/                     # Server deployment scripts
    ├── content-manager.service            # systemd service file
    ├── setup-user-service.sh             # Service setup script
    ├── setup-passwordless-sudo.sh        # Sudo configuration
    ├── setup-global-passwordless-sudo.sh # Global sudo setup
    ├── setup-sudo-timeout.sh             # Sudo timeout config
    └── fix-port-8000.sh                  # Port conflict resolution

Additional Files:
├── MIGRATION_PLAN.md                      # Migration documentation
├── SETUP_SERVICE.md                       # Service setup guide
├── SLACK_MESSAGE.md                       # Team communication
└── SUDO_SETUP.md                          # Sudo configuration docs
```

## Key Components

### Application Core
- **Flask Application**: Web framework providing routing and templating
- **Data Fetchers**: Modules to retrieve data from Wild Apricot API and Skedda iCal
- **Processors**: Pipeline for normalizing, filtering, organizing, and merging event data
- **Templates**: Multiple view formats (desktop, kiosk, mobile, print)

### Data Sources
- **Wild Apricot**: JSON API at https://wautils.nova-labs.org/api/digital_sign/events
- **Skedda**: iCal format bookings

### Deployment
- **Production Server**: Gunicorn WSGI server on port 8000
- **Web Server**: Apache reverse proxy (ports 80/443)
- **Service Management**: systemd service (content-manager.service)
- **Operating System**: Linux (Ubuntu/Debian)

## File Descriptions

### Core Files
- `run.py` - Starts Flask development server
- `wsgi.py` - WSGI entry point for production (used by Gunicorn)
- `requirements.txt` - Python package dependencies
- `.gitignore` - Files/directories to exclude from Git

### Configuration
- `app/config.py` - Application configuration (URLs, settings)
- `content-manager.service` - systemd service definition

### Documentation
- `README.md` - Project overview and quick start
- `docs/ARCHITECTURE.md` - System design and component descriptions
- `docs/DEPLOYMENT.md` - Production deployment procedures
- `docs/DEVELOPMENT.md` - Development setup and guidelines

### Templates
All templates extend `base.html` and provide different views:
- `kiosk.html` - Large text for digital signage, auto-refresh
- `desktop.html` - Full-featured desktop browser view
- `mobile.html` - Responsive mobile-optimized layout
- `print.html` - Print-friendly format

### Scripts
- `setup-user-service.sh` - Install and configure systemd service
- `fix-port-8000.sh` - Resolve port conflicts
- Various sudo configuration scripts

## Setup for GitHub

### Ready for Repository
This directory is cleaned and ready to be pushed to GitHub:
- ✅ Python cache removed (`__pycache__`, `*.pyc`)
- ✅ macOS metadata removed (`.DS_Store`, `Icon` files)
- ✅ Deployment backup files removed (`.backup`, `.new` files)
- ✅ `.gitignore` present and configured
- ✅ Documentation organized in `docs/` directory
- ✅ README.md with quick start guide

### To Initialize Git Repository

```bash
cd /Users/steve.klosky/Downloads/Code/xibo/content-manager

# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Nova Labs Content Manager

- Flask application for event aggregation
- Wild Apricot JSON API integration
- Skedda iCal integration
- Multiple display formats (kiosk, desktop, mobile, print)
- Complete documentation and deployment scripts"

# Add remote repository (replace with actual URL)
git remote add origin https://github.com/nova-labs/content-manager.git

# Push to GitHub
git push -u origin main
```

### Recommended GitHub Settings
- **License**: Add appropriate license (MIT, GPL, etc.)
- **Branch Protection**: Enable for main branch
- **Issues**: Enable for bug tracking
- **Wiki**: Enable for extended documentation
- **Topics**: python, flask, event-management, digital-signage

## Production Server Sync

To sync changes back to the production server:

```bash
# SSH to server
ssh sklosky@xibo.space.nova-labs.org

# Pull changes from GitHub
cd /home/sklosky/content-manager
git pull origin main

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete

# Restart service
sudo systemctl restart content-manager
sudo systemctl status content-manager
```

## Notes

- The backup preserves the complete working application
- All sensitive data should be managed via environment variables
- The application is production-ready and currently deployed
- Test thoroughly before deploying changes to production

## Backup Information

**Original Backup Command:**
```bash
ssh sklosky@xibo.space.nova-labs.org "cd /home/sklosky && tar -czf content-manager-backup-20260113-163313.tar.gz content-manager/"
```

**Extraction Command:**
```bash
cd /Users/steve.klosky/Downloads/Code/xibo
scp sklosky@xibo.space.nova-labs.org:/home/sklosky/content-manager-backup-20260113-163313.tar.gz .
tar -xzf content-manager-backup-20260113-163313.tar.gz
```

## Next Steps

1. ✅ Backup created and extracted
2. ✅ Directory structure cleaned for GitHub
3. ✅ Documentation added
4. ⏳ Initialize Git repository
5. ⏳ Create GitHub repository
6. ⏳ Push to GitHub
7. ⏳ Configure GitHub settings
8. ⏳ Update production deployment to use Git workflow
