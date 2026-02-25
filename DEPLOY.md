# Quick Deployment Guide

Deploy Canary Scanners to any device in under 5 minutes.

## Prerequisites

- Python 3.6 or higher
- Git
- Internet connection
- Access to your Thinkst Canary console

## Automated Setup (Recommended)

### Step 1: Clone and Setup

```bash
git clone https://github.com/pwhitlow/canaryscanners.git
cd canaryscanners
./setup.sh
```

The setup script will:
- Check for Python 3
- Install required dependencies
- Create `.env` file from template

### Step 2: Configure Credentials

Edit the `.env` file:

```bash
nano .env
```

Update with your credentials:
```
CANARY_CONSOLE_DOMAIN=your-console.canary.tools
CANARY_API_KEY=your-api-key-here
```

**Note**: Domain can be with or without `https://` prefix - both work:
- ✅ `1234abc.canary.tools`
- ✅ `https://1234abc.canary.tools`

### Step 3: Run

```bash
./canary_events.py
```

The script automatically loads credentials from `.env` file - no manual exports needed!

---

## Manual Setup

If the automated setup doesn't work:

```bash
# Clone repository
git clone https://github.com/pwhitlow/canaryscanners.git
cd canaryscanners

# Install dependencies
pip3 install -r requirements.txt

# Create .env file
cat > .env << 'EOF'
CANARY_CONSOLE_DOMAIN=your-console.canary.tools
CANARY_API_KEY=your-api-key-here
EOF

# Run the script
python3 canary_events.py
```

---

## Getting Your API Key

1. Log into your Canary console: `https://your-console.canary.tools`
2. Navigate to **Settings** → **API**
3. Click **Generate API Key** or copy existing key
4. Paste into `.env` file

**Tip**: You can create read-only API keys for safer deployment.

---

## Troubleshooting

### `pip3: command not found`

**Install Python and pip:**
- Ubuntu/Debian: `sudo apt install python3-pip`
- macOS: `brew install python3`
- CentOS/RHEL: `sudo yum install python3-pip`

### `Permission denied` when running setup.sh

Make the script executable:
```bash
chmod +x setup.sh
```

### `Permission denied` when running canary_events.py

Make it executable:
```bash
chmod +x canary_events.py
```

Or run with python directly:
```bash
python3 canary_events.py
```

### `ModuleNotFoundError: No module named 'dotenv'`

Install dependencies:
```bash
pip3 install -r requirements.txt
```

Or install manually:
```bash
pip3 install python-dotenv requests
```

### API Connection Errors

**Error**: `HTTPSConnectionPool(host='https'...)`
- Your domain includes `https://` and an old version of the script doesn't handle it
- **Fix**: Pull latest version: `git pull`
- Or remove `https://` from `CANARY_CONSOLE_DOMAIN` in `.env`

**Error**: `Failed to resolve` or `Connection refused`
- Check your console domain is correct
- Verify network connectivity: `ping your-console.canary.tools`
- Check firewall/proxy settings

**Error**: `Error making API request` with status code
- Status 401: Invalid API key - regenerate in console
- Status 403: Permissions issue - check API key permissions
- Status 500: Canary console issue - try again later

### `.env` File Not Loading

Verify `.env` file format:
```bash
cat .env
```

Should look like:
```
CANARY_CONSOLE_DOMAIN=1234abc.canary.tools
CANARY_API_KEY=abc123def456...
```

**Common mistakes:**
- ❌ `export CANARY_CONSOLE_DOMAIN=...` (remove `export`)
- ❌ `CANARY_CONSOLE_DOMAIN="..."` (remove quotes)
- ❌ Spaces around `=` (should be `KEY=value` not `KEY = value`)

---

## Verifying Installation

Test your installation:

```bash
python3 canary_events.py
```

**Expected behavior:**
1. "Fetching port scan incidents from Canary console..."
2. List of port scans with IPs and timestamps
3. IP grouping analysis
4. Frequency analysis with charts
5. Prompt to show repeat offenders

If you see this, installation succeeded! ✅

---

## Updating to Latest Version

Pull latest changes:

```bash
cd canaryscanners
git pull
pip3 install -r requirements.txt
```

Your `.env` file is preserved (gitignored).

---

## Security Best Practices

### Credential Protection

- ✅ `.env` file is automatically gitignored
- ✅ Never commit credentials to version control
- ✅ Use read-only API keys when possible
- ✅ Regenerate API keys periodically
- ✅ Keep `.env` file permissions restrictive:
  ```bash
  chmod 600 .env
  ```

### API Key Management

Create separate API keys for:
- Different environments (dev, prod)
- Different team members
- Different applications

This allows granular revocation if needed.

### Network Security

- Run on internal networks when possible
- Use VPN for remote access to Canary console
- Monitor API key usage in Canary console

---

## Deployment Examples

### Server Deployment

Deploy on a monitoring server:

```bash
cd /opt
sudo git clone https://github.com/pwhitlow/canaryscanners.git
cd canaryscanners
sudo ./setup.sh
sudo nano .env  # Add credentials
./canary_events.py
```

### Scheduled Execution

Run daily via cron:

```bash
# Edit crontab
crontab -e

# Add line to run daily at 9 AM
0 9 * * * cd /path/to/canaryscanners && /usr/bin/python3 canary_events.py > /var/log/canary_scan.log 2>&1
```

### Multiple Environments

Use different `.env` files:

```bash
# Production
cp .env .env.prod
# Staging
cp .env .env.staging

# Run with specific env
cat .env.prod > .env && ./canary_events.py
```

---

## Platform-Specific Notes

### macOS

- Use Homebrew to install Python: `brew install python3`
- Default shell is zsh (not bash)

### Linux

- Most distributions include Python 3
- May need to install pip: `sudo apt install python3-pip`

### Windows (WSL)

- Install WSL2: https://docs.microsoft.com/en-us/windows/wsl/install
- Follow Linux instructions inside WSL

### Docker (Optional)

For containerized deployment, see repository for Dockerfile examples.

---

## Support

**Issues**: https://github.com/pwhitlow/canaryscanners/issues

**Repository**: https://github.com/pwhitlow/canaryscanners

**Documentation**: See README.md for feature details
