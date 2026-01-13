"""Application routes"""
import logging
from flask import Blueprint, render_template, request, url_for
from concurrent.futures import ThreadPoolExecutor
from app.data_fetchers import wild_apricot, skedda
from app.processors import normalizer, merger, filter as filter_module, organizer
from app.utils import query_parser, qrcode_gen
from app.config import Config

logger = logging.getLogger(__name__)
bp = Blueprint('content_manager', __name__)

# Thread pool for parallel data fetching
executor = ThreadPoolExecutor(max_workers=2)


def fetch_all_data():
    """Fetch data from both sources in parallel"""
    try:
        # Fetch in parallel
        future_wa = executor.submit(wild_apricot.fetch_wild_apricot_events)
        future_sk = executor.submit(skedda.fetch_skedda_reservations)
        
        events = future_wa.result(timeout=Config.FETCH_TIMEOUT)
        reservations = future_sk.result(timeout=Config.FETCH_TIMEOUT)
        
        return events, reservations
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return [], []


@bp.route('/')
@bp.route('/events')
def master_page():
    """Master page with links and QR codes"""
    # Fetch data to show summary
    events, reservations = fetch_all_data()
    
    # Generate QR codes for common views
    base_url = request.url_root.rstrip('/')
    qr_codes = {
        'today_kiosk': qrcode_gen.generate_qr_code(f"{base_url}/display?range=today&format=kiosk"),
        'this_week_desktop': qrcode_gen.generate_qr_code(f"{base_url}/display?range=this-week&format=desktop"),
        'all_mobile': qrcode_gen.generate_qr_code(f"{base_url}/display?format=mobile"),
    }
    
    return render_template('master.html', 
                         events_count=len(events),
                         reservations_count=len(reservations),
                         qr_codes=qr_codes,
                         base_url=base_url)


@bp.route('/display')
def display():
    """Main display page with filtering"""
    # Parse query parameters
    params = query_parser.parse_query_params(request.args)
    
    # Fetch data
    events_raw, reservations_raw = fetch_all_data()
    
    # Normalize data
    events = [normalizer.normalize_event(e) for e in events_raw]
    reservations = [normalizer.normalize_reservation(r) for r in reservations_raw]
    
    # Merge
    all_items = merger.merge_events_and_reservations(events, reservations)
    
    # Apply filters
    # Source filter
    filtered = filter_module.filter_by_source(all_items, params['source'])
    
    # Location filter
    if params['location']:
        filtered = filter_module.filter_by_location(filtered, params['location'])
    
    # Date filter
    filtered = filter_module.filter_by_date_range(
        filtered,
        start_date=params['start'],
        end_date=params['end'],
        date_range=params['range'],
        specific_date=params['date']
    )
    
    # Filter past events
    if params['filter_past']:
        filtered = filter_module.filter_past_events(filtered, filter_past=True)
    
    # Organize by date
    organized = organizer.organize_by_date(filtered)
    
    # Generate QR code for current view
    current_url = request.url
    qr_code = qrcode_gen.generate_qr_code(current_url)
    
    # Select template based on format
    template_map = {
        'kiosk': 'kiosk.html',
        'mobile': 'mobile.html',
        'desktop': 'desktop.html',
        'print': 'print.html'
    }
    template = template_map.get(params['format'], 'desktop.html')
    
    return render_template(template,
                         items_by_date=organized,
                         params=params,
                         qr_code=qr_code,
                         current_url=current_url,
                         base_url=request.url_root.rstrip('/'))


@bp.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('error.html', 
                         error_code=404,
                         error_message="Page not found"), 404


@bp.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal error: {error}")
    return render_template('error.html',
                         error_code=500,
                         error_message="Internal server error"), 500

