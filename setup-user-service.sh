#!/bin/bash
# Setup content-manager as a user systemd service (no sudo required)

set -e

echo "Setting up content-manager as a user systemd service..."
echo ""

# Create user systemd directory
mkdir -p ~/.config/systemd/user
echo "✓ Created ~/.config/systemd/user directory"

# Copy service file
SERVICE_FILE="$HOME/.config/systemd/user/content-manager.service"
if [ -f "/home/sklosky/content-manager/content-manager.service" ]; then
    cp /home/sklosky/content-manager/content-manager.service "$SERVICE_FILE"
    echo "✓ Copied service file"
else
    echo "✗ Service file not found at /home/sklosky/content-manager/content-manager.service"
    exit 1
fi

# Remove User/Group lines from service file
sed -i '/^User=/d' "$SERVICE_FILE"
sed -i '/^Group=/d' "$SERVICE_FILE"
echo "✓ Removed User/Group lines (not needed for user service)"

# Enable lingering (requires sudo, but only once)
echo ""
echo "Enabling lingering (so service runs after logout)..."
if sudo loginctl enable-linger "$USER" 2>/dev/null; then
    echo "✓ Lingering enabled"
else
    echo "⚠ Warning: Could not enable lingering (may need to run manually):"
    echo "  sudo loginctl enable-linger $USER"
fi

# Reload systemd
echo ""
echo "Reloading systemd user daemon..."
systemctl --user daemon-reload
echo "✓ Systemd user daemon reloaded"

# Enable service
echo ""
echo "Enabling content-manager service..."
systemctl --user enable content-manager.service
echo "✓ Service enabled"

echo ""
echo "========================================="
echo "Setup complete!"
echo "========================================="
echo ""
echo "Service commands (no sudo needed):"
echo "  Start:   systemctl --user start content-manager.service"
echo "  Stop:    systemctl --user stop content-manager.service"
echo "  Restart: systemctl --user restart content-manager.service"
echo "  Status:  systemctl --user status content-manager.service"
echo "  Logs:    journalctl --user -u content-manager.service -f"
echo ""
echo "To start the service now, run:"
echo "  systemctl --user start content-manager.service"
echo ""


