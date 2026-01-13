# Development Guide

## Setup Development Environment

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Local Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd content-manager
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
Create a `.env` file:
```bash
WILD_APRICOT_URL=https://wautils.nova-labs.org/api/digital_sign/events
SKEDDA_ICS_URL=http://localhost/bookings.ics
```

5. **Run development server**
```bash
python run.py
```

The application will be available at http://localhost:5000

## Project Structure

```
content-manager/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── config.py                # Configuration settings
│   ├── routes.py                # URL routes and views
│   ├── data_fetchers/           # External data retrieval
│   │   ├── __init__.py
│   │   ├── wild_apricot.py      # Wild Apricot API client
│   │   └── skedda.py            # Skedda iCal parser
│   ├── processors/              # Data processing pipeline
│   │   ├── __init__.py
│   │   ├── normalizer.py        # Data normalization
│   │   ├── filter.py            # Filtering logic
│   │   ├── organizer.py         # Data organization
│   │   └── merger.py            # Data merging
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   ├── query_parser.py      # Query parameter parsing
│   │   ├── text_cleaner.py      # Text cleaning utilities
│   │   └── qrcode_gen.py        # QR code generation
│   ├── static/                  # Static assets
│   │   ├── css/                 # Stylesheets
│   │   └── js/                  # JavaScript files
│   └── templates/               # HTML templates
│       ├── base.html
│       ├── master.html
│       ├── desktop.html
│       ├── kiosk.html
│       ├── mobile.html
│       ├── print.html
│       └── error.html
├── tests/                       # Test files
├── docs/                        # Documentation
├── docker/                      # Docker configuration
├── run.py                       # Development server entry point
├── wsgi.py                      # Production WSGI entry point
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
└── README.md                    # Project overview
```

## Coding Standards

### Python Style
- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints where appropriate

### Naming Conventions
- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private methods: `_leading_underscore`

### Documentation
- Use docstrings for all public functions and classes
- Include parameter types and return types
- Provide usage examples for complex functions

Example:
```python
def fetch_events(start_date: datetime, end_date: datetime) -> List[Dict]:
    """
    Fetch events from Wild Apricot API within date range.
    
    Args:
        start_date: Beginning of date range
        end_date: End of date range
        
    Returns:
        List of event dictionaries with normalized fields
        
    Example:
        >>> events = fetch_events(datetime(2026, 1, 1), datetime(2026, 1, 31))
        >>> len(events)
        42
    """
    pass
```

## Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_wild_apricot.py

# Run with coverage
python -m pytest --cov=app tests/
```

### Writing Tests
Place test files in the `tests/` directory:
```python
# tests/test_wild_apricot.py
import pytest
from app.data_fetchers.wild_apricot import fetch_wild_apricot_events

def test_fetch_events():
    events = fetch_wild_apricot_events()
    assert isinstance(events, list)
    assert len(events) > 0
    assert 'name' in events[0]
    assert 'start_date' in events[0]
```

## Debugging

### Enable Debug Mode
```python
# run.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Fetching events from API")
logger.info("Successfully fetched 42 events")
logger.error("Failed to parse date: %s", date_string)
```

### Common Issues

**Issue**: Import errors
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: Template not found
```bash
# Solution: Check template path and Flask template folder configuration
# Templates should be in app/templates/
```

**Issue**: Static files not loading
```bash
# Solution: Verify static folder configuration in __init__.py
# Static files should be in app/static/
```

## API Development

### Adding New Endpoints

1. Define route in `app/routes.py`:
```python
@app.route('/api/events')
def get_events():
    events = fetch_and_process_events()
    return jsonify(events)
```

2. Update documentation in `docs/API.md`

3. Add tests in `tests/test_routes.py`

### Query Parameters
Use `utils/query_parser.py` for consistent parameter handling:
```python
from app.utils.query_parser import parse_date_range

@app.route('/display')
def display():
    date_range = parse_date_range(request.args.get('range', 'this-week'))
    events = filter_by_date(events, date_range)
    return render_template('display.html', events=events)
```

## Data Processing Pipeline

### Adding New Data Source

1. Create fetcher in `app/data_fetchers/`:
```python
# app/data_fetchers/new_source.py
def fetch_new_source_events():
    """Fetch events from new source."""
    # Implement fetch logic
    return normalized_events
```

2. Update merger in `app/processors/merger.py`:
```python
from app.data_fetchers.new_source import fetch_new_source_events

def merge_all_events():
    wa_events = fetch_wild_apricot_events()
    skedda_events = fetch_skedda_events()
    new_events = fetch_new_source_events()
    return merge_events([wa_events, skedda_events, new_events])
```

3. Add configuration in `app/config.py`:
```python
NEW_SOURCE_URL = os.getenv('NEW_SOURCE_URL', 'https://...')
```

## Template Development

### Creating New Views

1. Create template in `app/templates/`:
```html
<!-- app/templates/new_view.html -->
{% extends "base.html" %}
{% block content %}
  <h1>New View</h1>
  {% for event in events %}
    <div class="event">{{ event.name }}</div>
  {% endfor %}
{% endblock %}
```

2. Add CSS in `app/static/css/`:
```css
/* app/static/css/new_view.css */
.event {
    padding: 1rem;
    margin: 0.5rem 0;
    border: 1px solid #ccc;
}
```

3. Create route:
```python
@app.route('/new-view')
def new_view():
    events = fetch_and_process_events()
    return render_template('new_view.html', events=events)
```

## Performance Optimization

### Caching
Consider implementing caching for expensive operations:
```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=1)
def fetch_cached_events(cache_key):
    """Cache events for 5 minutes."""
    return fetch_wild_apricot_events()

def get_events():
    # Cache key changes every 5 minutes
    cache_key = datetime.now().replace(second=0, microsecond=0) // timedelta(minutes=5)
    return fetch_cached_events(cache_key)
```

### Database Considerations
Currently, the app fetches data on-demand. For high traffic:
- Consider adding a database layer (SQLite, PostgreSQL)
- Implement background jobs to periodically fetch and cache data
- Use Redis for session/cache storage

## Contributing

1. Create a feature branch: `git checkout -b feature/new-feature`
2. Make changes and test thoroughly
3. Update documentation
4. Commit with descriptive messages
5. Push and create pull request

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Wild Apricot API](https://wautils.nova-labs.org/api/digital_sign/events)
