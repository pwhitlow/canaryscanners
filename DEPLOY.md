# Quick Deployment Guide

## Deploy to Another Device (5 minutes)

### Prerequisites
- Python 3.6 or higher
- Git
- Internet connection

### Deployment Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pwhitlow/canaryscanners.git
   cd canaryscanners
   ```

2. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

3. **Configure credentials:**
   ```bash
   nano .env
   ```

   Update these values:
   - `CANARY_CONSOLE_DOMAIN` - Your Canary console domain (e.g., `1234abc.canary.tools`)
   - `CANARY_API_KEY` - Your API key from Canary console (Settings → API)

4. **Run the script:**
   ```bash
   python3 canary_events.py
   ```

   The script automatically loads credentials from the `.env` file.

### Alternative: Manual Setup

If the setup script doesn't work, follow these manual steps:

```bash
# Clone repository
git clone https://github.com/pwhitlow/canaryscanners.git
cd canaryscanners

# Install dependencies
pip3 install -r requirements.txt

# Set environment variables
export CANARY_CONSOLE_DOMAIN='your-console.canary.tools'
export CANARY_API_KEY='your-api-key-here'

# Run the script
python3 canary_events.py
```

### Make Credentials Persistent

To avoid setting environment variables every time:

**On Linux/Mac (bash):**
```bash
echo "export CANARY_CONSOLE_DOMAIN='your-console.canary.tools'" >> ~/.bashrc
echo "export CANARY_API_KEY='your-api-key-here'" >> ~/.bashrc
source ~/.bashrc
```

**On Linux/Mac (zsh):**
```bash
echo "export CANARY_CONSOLE_DOMAIN='your-console.canary.tools'" >> ~/.zshrc
echo "export CANARY_API_KEY='your-api-key-here'" >> ~/.zshrc
source ~/.zshrc
```

### Troubleshooting

**Problem: `pip3: command not found`**
- Install pip: `sudo apt install python3-pip` (Ubuntu/Debian) or `brew install python3` (Mac)

**Problem: `Permission denied` when running setup.sh**
- Make it executable: `chmod +x setup.sh`

**Problem: API connection fails**
- Verify your console domain (don't include `https://`)
- Regenerate API key in Canary console if needed
- Check firewall/network connectivity

### Getting Your API Key

1. Log into your Canary console: `https://your-console.canary.tools`
2. Go to **Settings** → **API**
3. Click **Generate API Key** or copy existing key
4. Use this key in your `.env` file

### Security Notes

- Never commit `.env` file to git (it's already in `.gitignore`)
- Regenerate API keys periodically
- Use read-only API keys when possible
