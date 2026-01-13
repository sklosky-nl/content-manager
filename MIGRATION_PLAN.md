# Migration Plan: Development to Production

## Recommended Production Location

**Standard Linux locations:**
- `/opt/content-manager/` - Recommended for third-party applications
- `/srv/content-manager/` - Alternative for service-specific data
- `/var/www/content-manager/` - If treating as web content

**Recommendation: `/opt/content-manager/`**

## Files and Directories to Move

### 1. Complete Application Directory
```bash
# Source
/home/sklosky/content-manager/

# Destination
/opt/content-manager/
```

**Includes:**
- `app/` - All application code
- `requirements.txt` - Python dependencies
- `wsgi.py` - WSGI entry point
- `run.py` - Development server (optional, can be removed in production)
- `README.md` - Documentation
- `docker/` - Docker files (if using)
- `tests/` - Test files (optional)

### 2. Configuration Files
- `content-manager.service` - Systemd service file (needs path updates)
- `SETUP_SERVICE.md` - Setup instructions (optional)
- `SLACK_MESSAGE.md` - Slack message (optional)

## Required Changes After Migration

### 1. Update Systemd Service File

**File:** `/etc/systemd/system/content-manager.service`

**Changes needed:**
```ini
[Service]
# OLD:
WorkingDirectory=/home/sklosky/content-manager
ExecStart=/usr/bin/python3 -m gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 30 --access-logfile - --error-logfile - wsgi:app

# NEW:
WorkingDirectory=/opt/content-manager
ExecStart=/usr/bin/python3 -m gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 30 --access-logfile - --error-logfile - wsgi:app
```

### 2. Update File Permissions

```bash
# Set ownership (adjust user/group as needed)
sudo chown -R www-data:www-data /opt/content-manager
# OR if running as specific user:
sudo chown -R content-manager:content-manager /opt/content-manager

# Set directory permissions
sudo chmod 755 /opt/content-manager
sudo chmod -R 644 /opt/content-manager/app/**/*.py
sudo chmod 755 /opt/content-manager/app
sudo chmod 755 /opt/content-manager/app/*/

# Make scripts executable
sudo chmod +x /opt/content-manager/wsgi.py
```

### 3. Update Python Environment

**Option A: System-wide installation**
```bash
cd /opt/content-manager
sudo pip3 install -r requirements.txt
```

**Option B: Virtual environment (recommended)**
```bash
cd /opt/content-manager
sudo python3 -m venv venv
sudo venv/bin/pip install -r requirements.txt
```

**Then update service file:**
```ini
[Service]
Environment="PATH=/opt/content-manager/venv/bin:/usr/bin:/usr/local/bin"
ExecStart=/opt/content-manager/venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 30 --access-logfile - --error-logfile - wsgi:app
```

### 4. Update Apache Configuration (if using reverse proxy)

If Apache is configured to proxy to the application, check:
- `/etc/apache2/sites-enabled/*.conf`
- Look for `ProxyPass` directives pointing to `http://localhost:8000`
- These typically don't need changes unless paths changed

### 5. Update Environment Variables (if any)

Check for any environment variables set in:
- `/etc/environment`
- `/etc/systemd/system/content-manager.service` (Environment= lines)
- Shell profiles (`.bashrc`, `.profile`)

### 6. Update Log Locations (if using file logging)

If logs are written to specific paths, update:
- Service file `--access-logfile` and `--error-logfile` paths
- Or use journald (current setup uses `-` for stdout/stderr)

## Migration Steps

### Step 1: Prepare Production Location
```bash
# Create directory
sudo mkdir -p /opt/content-manager

# Set ownership (adjust user as needed)
sudo chown sklosky:sklosky /opt/content-manager
```

### Step 2: Copy Files
```bash
# Copy entire directory
sudo cp -r /home/sklosky/content-manager/* /opt/content-manager/

# OR use rsync for better control
sudo rsync -av /home/sklosky/content-manager/ /opt/content-manager/
```

### Step 3: Update Service File
```bash
# Edit the service file
sudo nano /etc/systemd/system/content-manager.service

# Update WorkingDirectory and any paths
# Then reload
sudo systemctl daemon-reload
```

### Step 4: Set Up Python Environment
```bash
cd /opt/content-manager

# Option A: Virtual environment (recommended)
sudo python3 -m venv venv
sudo venv/bin/pip install -r requirements.txt

# Option B: System-wide
sudo pip3 install -r requirements.txt
```

### Step 5: Set Permissions
```bash
# Adjust ownership
sudo chown -R www-data:www-data /opt/content-manager
# OR
sudo chown -R content-manager:content-manager /opt/content-manager

# Set permissions
sudo find /opt/content-manager -type d -exec chmod 755 {} \;
sudo find /opt/content-manager -type f -exec chmod 644 {} \;
sudo chmod +x /opt/content-manager/wsgi.py
```

### Step 6: Test and Restart
```bash
# Test the service file syntax
sudo systemctl daemon-reload

# Start the service
sudo systemctl start content-manager.service

# Check status
sudo systemctl status content-manager.service

# Check logs
sudo journalctl -u content-manager.service -f
```

### Step 7: Verify Application
```bash
# Test the endpoint
curl http://localhost:8000/

# Check from external URL
curl http://xibo.space.nova-lab.org:8000/events
```

## Security Considerations

1. **File Permissions:**
   - Application files should not be world-writable
   - Use appropriate user/group ownership
   - Consider using a dedicated user (e.g., `content-manager`)

2. **Python Environment:**
   - Virtual environment is more secure than system-wide install
   - Keeps dependencies isolated

3. **Service User:**
   - Consider creating dedicated user: `sudo useradd -r -s /bin/false content-manager`
   - Run service as this user instead of root or your personal account

4. **Logs:**
   - Ensure log files have appropriate permissions
   - Consider log rotation

## Rollback Plan

If something goes wrong:
```bash
# Stop the service
sudo systemctl stop content-manager.service

# Revert service file
sudo cp /home/sklosky/content-manager/content-manager.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start content-manager.service
```

## Checklist

- [ ] Create production directory (`/opt/content-manager`)
- [ ] Copy all application files
- [ ] Update systemd service file paths
- [ ] Set up Python environment (venv or system-wide)
- [ ] Set correct file permissions and ownership
- [ ] Update any hardcoded paths in code (if any)
- [ ] Test service starts correctly
- [ ] Verify application responds on port 8000
- [ ] Test external URL access
- [ ] Update documentation with new paths
- [ ] Remove or archive old development location (optional)

## Notes

- The application code itself doesn't have hardcoded paths (good!)
- Only the systemd service file needs path updates
- Apache reverse proxy config likely doesn't need changes
- Consider backing up before migration
- Test thoroughly before removing old location

