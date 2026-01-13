# Streamlining Sudo Commands for Cursor Workflows

## Problem
Sudo commands require password prompts, which interrupt automated Cursor workflows.

## Solutions

### Option 1: Passwordless Sudo for Specific Commands (Recommended)

Configure sudo to allow specific commands without a password prompt.

**Step 1: Create a sudoers configuration file**

```bash
sudo visudo -f /etc/sudoers.d/content-manager
```

**Step 2: Add these lines (adjust username if different):**

```
# Allow passwordless sudo for content-manager service management
sklosky ALL=(ALL) NOPASSWD: /bin/systemctl start content-manager.service
sklosky ALL=(ALL) NOPASSWD: /bin/systemctl stop content-manager.service
sklosky ALL=(ALL) NOPASSWD: /bin/systemctl restart content-manager.service
sklosky ALL=(ALL) NOPASSWD: /bin/systemctl status content-manager.service
sklosky ALL=(ALL) NOPASSWD: /bin/systemctl enable content-manager.service
sklosky ALL=(ALL) NOPASSWD: /bin/systemctl disable content-manager.service
sklosky ALL=(ALL) NOPASSWD: /bin/systemctl daemon-reload
sklosky ALL=(ALL) NOPASSWD: /usr/bin/journalctl -u content-manager.service*
sklosky ALL=(ALL) NOPASSWD: /bin/cp /home/sklosky/content-manager/content-manager.service /etc/systemd/system/
```

**Step 3: Test it:**

```bash
sudo -n systemctl status content-manager.service
```

If it works without a password, you're all set!

### Option 2: User Systemd Service (No Sudo Required)

Use systemd user services which don't require sudo at all.

**Step 1: Create user systemd directory**

```bash
mkdir -p ~/.config/systemd/user
```

**Step 2: Create user service file**

```bash
cp /home/sklosky/content-manager/content-manager.service ~/.config/systemd/user/content-manager.service
```

**Step 3: Edit the service file to remove User/Group lines**

```bash
nano ~/.config/systemd/user/content-manager.service
```

Remove these lines:
```
User=sklosky
Group=sklosky
```

**Step 4: Enable lingering (so service runs after logout)**

```bash
sudo loginctl enable-linger sklosky
```

**Step 5: Reload and start**

```bash
systemctl --user daemon-reload
systemctl --user enable content-manager.service
systemctl --user start content-manager.service
```

**Step 6: Use these commands (no sudo needed):**

```bash
systemctl --user start content-manager.service
systemctl --user stop content-manager.service
systemctl --user restart content-manager.service
systemctl --user status content-manager.service
journalctl --user -u content-manager.service -f
```

### Option 3: Sudo Password Caching (Temporary Solution)

Sudo caches your password for a short time (default 15 minutes). You can extend this:

```bash
sudo visudo
```

Add or modify this line:
```
Defaults timestamp_timeout=60
```

This caches the password for 60 minutes. Adjust as needed.

### Option 4: SSH Key with Sudo (If Using SSH)

If you're accessing via SSH, you can configure SSH to forward authentication:

```bash
# In your SSH config (~/.ssh/config)
Host your-server
    ForwardAgent yes
```

## Option 3: Global Passwordless Sudo (All Commands)

**WARNING: This reduces security significantly. Only use if you understand the risks.**

Allows ALL sudo commands without a password prompt.

**Setup:**
```bash
cd /home/sklosky/content-manager
./setup-global-passwordless-sudo.sh
```

**After setup:**
- All sudo commands work without password
- Maximum convenience for automated workflows
- **Security risk**: Anyone with access to your account can run any command as root

## Option 4: Extended Sudo Timeout (Balanced Approach)

Keeps password requirement but extends how long sudo remembers it.

**Setup:**
```bash
cd /home/sklosky/content-manager
./setup-sudo-timeout.sh
```

**After setup:**
- Enter password once, then no prompts for 30-240 minutes (configurable)
- More secure than passwordless sudo
- Still convenient for workflows

## Recommendation

**For Cursor workflows, I recommend:**
1. **Option 4 (Extended Timeout)** - Best balance of security and convenience
2. **Option 2 (User Systemd Service)** - For service management (no sudo needed)
3. **Option 3 (Global Passwordless)** - Only if you're the only user and understand the risks

**For one-time setup tasks, Option 1 (Passwordless Sudo)** is good for specific commands you use frequently.

## Quick Setup Script

I can create a script to set up Option 2 automatically. Would you like me to create it?

