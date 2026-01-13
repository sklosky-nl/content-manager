# Setting Up Content Manager as a System Service

## Option 1: System-wide Service (requires sudo)

1. Copy the service file:
   ```bash
   sudo cp /home/sklosky/content-manager/content-manager.service /etc/systemd/system/
   ```

2. Reload systemd:
   ```bash
   sudo systemctl daemon-reload
   ```

3. Enable the service (starts on boot):
   ```bash
   sudo systemctl enable content-manager.service
   ```

4. Start the service:
   ```bash
   sudo systemctl start content-manager.service
   ```

5. Check status:
   ```bash
   sudo systemctl status content-manager.service
   ```

6. View logs:
   ```bash
   sudo journalctl -u content-manager.service -f
   ```

## Option 2: User Service (no sudo required)

1. Create user systemd directory:
   ```bash
   mkdir -p ~/.config/systemd/user
   ```

2. Copy and modify the service file for user service:
   ```bash
   cp /home/sklosky/content-manager/content-manager.service ~/.config/systemd/user/
   ```

3. Edit the file to remove User/Group lines:
   ```bash
   nano ~/.config/systemd/user/content-manager.service
   ```
   Remove these lines:
   ```
   User=sklosky
   Group=sklosky
   ```

4. Reload user systemd:
   ```bash
   systemctl --user daemon-reload
   ```

5. Enable and start:
   ```bash
   systemctl --user enable content-manager.service
   systemctl --user start content-manager.service
   ```

6. Enable lingering (so service runs after logout):
   ```bash
   sudo loginctl enable-linger sklosky
   ```

7. Check status:
   ```bash
   systemctl --user status content-manager.service
   ```

## Stopping the Current Process

Before starting the service, stop the current running process:

```bash
# Find the process
ps aux | grep "content-manager/run.py"

# Kill it (replace PID with actual process ID)
kill <PID>
```

Or if it's running in a terminal, just press Ctrl+C.

## Service Management Commands

- **Start**: `sudo systemctl start content-manager.service` (or `systemctl --user start` for user service)
- **Stop**: `sudo systemctl stop content-manager.service`
- **Restart**: `sudo systemctl restart content-manager.service`
- **Status**: `sudo systemctl status content-manager.service`
- **Logs**: `sudo journalctl -u content-manager.service -f`

