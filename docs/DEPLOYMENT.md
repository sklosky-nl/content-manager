# Deployment Guide

## Overview
This guide covers deploying the content-manager application to the Nova Labs xibo server.

## Server Details
- **Host**: xibo.space.nova-labs.org (192.168.203.160)
- **User**: sklosky
- **App Location**: /home/sklosky/content-manager
- **Service**: systemd service named "content-manager.service"
- **Port**: 8000 (gunicorn)
- **Web Server**: Apache on ports 80/443 (reverse proxy)

## Deployment Steps

### 1. Backup Current Version
```bash
ssh sklosky@xibo.space.nova-labs.org
cd /home/sklosky
tar -czf content-manager-backup-$(date +%Y%m%d-%H%M%S).tar.gz content-manager/
```

### 2. Upload New Files
```bash
# From your local machine
scp <local-file> sklosky@xibo.space.nova-labs.org:/home/sklosky/content-manager/<target-path>
```

### 3. Update Files on Server
```bash
ssh sklosky@xibo.space.nova-labs.org
cd /home/sklosky/content-manager

# Backup existing files
cp app/config.py app/config.py.backup
cp app/data_fetchers/wild_apricot.py app/data_fetchers/wild_apricot.py.backup

# Move new files into place
mv app/config.py.new app/config.py
mv app/data_fetchers/wild_apricot.py.new app/data_fetchers/wild_apricot.py

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete
```

### 4. Restart Service
```bash
sudo systemctl restart content-manager
sudo systemctl status content-manager
```

### 5. Verify Deployment
```bash
# Check logs
sudo journalctl -u content-manager -n 50 -f

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/display?range=this-month
```

### 6. Rollback (if needed)
```bash
cd /home/sklosky/content-manager
mv app/config.py.backup app/config.py
mv app/data_fetchers/wild_apricot.py.backup app/data_fetchers/wild_apricot.py
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
sudo systemctl restart content-manager
```

## Service Management

### Check Status
```bash
sudo systemctl status content-manager
```

### View Logs
```bash
sudo journalctl -u content-manager -n 100
sudo journalctl -u content-manager -f  # follow logs
```

### Restart Service
```bash
sudo systemctl restart content-manager
```

### Service Configuration
The service runs using gunicorn:
```
/usr/bin/python3 -m gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 30 --access-logfile - --error-logfile - wsgi:app
```

## Configuration

### Environment Variables
Set in `/etc/systemd/system/content-manager.service` or in `.env` file:
- `WILD_APRICOT_URL`: URL for Wild Apricot events feed (default: https://wautils.nova-labs.org/api/digital_sign/events)
- `SKEDDA_ICS_URL`: URL for Skedda iCal feed

### Apache Configuration
The Apache server proxies requests to the gunicorn application on port 8000.
See `apache-content-manager-config.conf` for configuration details.

## Troubleshooting

### Check if service is running
```bash
ps aux | grep gunicorn
```

### Check port 8000
```bash
sudo lsof -i :8000
sudo netstat -tlnp | grep 8000
```

### Common Issues
1. **Service won't start**: Check logs with `journalctl -u content-manager -n 50`
2. **Import errors**: Clear Python cache and restart
3. **Permission errors**: Verify file ownership and permissions
4. **Port conflicts**: Check if another process is using port 8000
