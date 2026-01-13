#!/bin/bash
# Script to configure Apache to listen on port 8000 and proxy to Flask app

set -e

echo "=== Configuring Apache for Port 8000 ==="

# Create VirtualHost configuration for port 8000
sudo tee /etc/apache2/sites-available/000-default-8000.conf > /dev/null <<'EOF'
<VirtualHost *:8000>
    ServerAdmin webmaster@localhost
    ServerName xibo.space.nova-labs.org

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    ProxyPreserveHost On
    RequestHeader set X-Forwarded-Proto expr=%{REQUEST_SCHEME}

    # Content Manager - proxy all requests to port 8000 Flask app
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
EOF

echo "✓ Created VirtualHost configuration"

# Enable the site
sudo a2ensite 000-default-8000.conf

echo "✓ Enabled site configuration"

# Test Apache configuration
echo "Testing Apache configuration..."
if sudo apache2ctl configtest; then
    echo "✓ Configuration test passed"
    
    # Reload Apache
    echo "Reloading Apache..."
    sudo systemctl reload apache2
    echo "✓ Apache reloaded"
    
    echo ""
    echo "=== Configuration Complete ==="
    echo "Apache is now listening on port 8000 and proxying to the Flask app."
    echo ""
    echo "Test with: curl http://xibo.space.nova-labs.org:8000/events"
else
    echo "✗ Configuration test failed. Please check the errors above."
    exit 1
fi


