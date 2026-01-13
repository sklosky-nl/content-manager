// Minimal JavaScript for compatibility
// Auto-refresh for kiosk mode
(function() {
    if (window.location.search.includes('format=kiosk')) {
        setTimeout(function() {
            window.location.reload();
        }, 300000); // 5 minutes
    }
})();

