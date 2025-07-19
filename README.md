# Galxe Quest Monitor Bot 🤖

A fully automated Telegram bot that monitors Galxe quest pages for specific projects and sends new quest notifications to a Telegram channel. Optimized for Ubuntu VPS deployment.

## Features ✨

- 🔍 **Automated Monitoring**: Continuously monitors multiple Galxe project pages every 5 minutes
- 📱 **Telegram Notifications**: Sends direct quest links only (clean format)
- 🗄️ **Database Storage**: Tracks quests to avoid duplicate notifications
- ⚡ **Smart Scraping**: Uses Selenium for dynamic content handling
- 🔄 **Fast Response**: Checks every 5 minutes for maximum responsiveness
- 📊 **Error Handling**: Robust error handling with logging
- 🛡️ **Rate Limiting**: Respectful scraping with delays between requests
- 🖥️ **VPS Optimized**: Designed for 24/7 Ubuntu VPS operation

## Supported Projects 🎯

Currently monitoring:
- **D3** - https://app.galxe.com/quest/D3
- **T-REXNetwork** - https://app.galxe.com/quest/T-REXNetwork
- **Fleek** - https://app.galxe.com/quest/fleek
- **Rayls** - https://app.galxe.com/quest/rayls
- **zkVerify** - https://app.galxe.com/quest/zkverify
- **Mawari** - https://app.galxe.com/quest/mawari

*Easy to add more projects in the configuration!*

## Prerequisites 📋

- Ubuntu 18.04+ VPS
- Python 3.8 or higher
- Chrome browser (for Selenium WebDriver)
- Telegram Bot Token (from @BotFather)
- Telegram Channel (public or private)

## VPS Setup 🚀

### 1. Connect to Your VPS
```bash
ssh root@your-vps-ip
```

### 2. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Install Python and Dependencies
```bash
# Install Python 3.8+
sudo apt install python3 python3-pip python3-venv -y

# Install Chrome and ChromeDriver
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable -y

# Install additional dependencies
sudo apt install git screen htop -y
```

### 4. Clone Repository
```bash
git clone https://github.com/AbbyTheGod/Galxe-Alert.git
cd Galxe-Alert
```

### 5. Setup Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 6. Configure Environment
```bash
# Copy environment template
cp env_example.txt .env

# Edit environment file
nano .env
```

Add your Telegram credentials:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_username_or_id
```

### 7. Test Installation
```bash
# Test all components
python test_bot.py

# Test Telegram notifications
python test_telegram_notifications.py
```

## Running the Bot 🎮

### Method 1: Direct Run
```bash
# Activate virtual environment
source venv/bin/activate

# Run the bot
python main.py
```

### Method 2: Screen Session (Recommended for VPS)
```bash
# Create a new screen session
screen -S galxe-bot

# Activate virtual environment
source venv/bin/activate

# Run the bot
python main.py

# Detach from screen: Press Ctrl+A, then D
# Reattach to screen: screen -r galxe-bot
```

### Method 3: Systemd Service (For 24/7 Operation)
```bash
# Create service file
sudo nano /etc/systemd/system/galxe-bot.service
```

Add this content:
```ini
[Unit]
Description=Galxe Quest Monitor Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/Galxe-Alert
Environment=PATH=/root/Galxe-Alert/venv/bin
ExecStart=/root/Galxe-Alert/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable galxe-bot
sudo systemctl start galxe-bot

# Check status
sudo systemctl status galxe-bot

# View logs
sudo journalctl -u galxe-bot -f
```

## Configuration ⚙️

### Current Settings

- **Scraping Interval**: Every 5 minutes
- **Notification Format**: Direct quest links only
- **Projects Monitored**: 6 projects (D3, T-REXNetwork, Fleek, Rayls, zkVerify, Mawari)

### Adding New Projects

Edit `config.py`:
```python
PROJECTS = {
    'YourProject': {
        'name': 'YourProject',
        'url': 'https://app.galxe.com/quest/YourProject',
        'quest_url': 'https://app.galxe.com/quest/YourProject'
    },
    # ... existing projects
}
```

### Changing Monitoring Frequency

Edit `config.py`:
```python
SCRAPING_INTERVAL_MINUTES = 10  # Check every 10 minutes
```

## Monitoring and Maintenance 🔧

### Check Bot Status
```bash
# If using screen
screen -r galxe-bot

# If using systemd
sudo systemctl status galxe-bot

# View recent logs
sudo journalctl -u galxe-bot -n 50
```

### Update Bot
```bash
cd Galxe-Alert
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart galxe-bot
```

### Database Management
```bash
# View database
sqlite3 quests.db ".tables"
sqlite3 quests.db "SELECT * FROM quests LIMIT 10;"

# Backup database
cp quests.db quests_backup_$(date +%Y%m%d_%H%M%S).db
```

## Project Structure 📁

```
Galxe-Alert/
├── main.py                      # Main bot script
├── config.py                    # Configuration settings
├── database.py                  # Database operations
├── scraper.py                   # Web scraping functionality
├── telegram_bot.py              # Telegram bot interface
├── test_bot.py                  # Component testing
├── test_telegram_notifications.py # Telegram notification testing
├── debug_scraper.py             # Scraper debugging
├── requirements.txt             # Python dependencies
├── env_example.txt              # Environment variables example
├── .gitignore                   # Git ignore file
├── README.md                    # This file
├── venv/                        # Python virtual environment
└── quests.db                    # SQLite database (created automatically)
```

## Notification Format 📱

The bot sends clean, simple notifications:
```
https://galxe.com/quest/ProjectName/QuestID
```

Just the direct link - no extra text, no project names, no metadata.

## Troubleshooting 🔧

### Common VPS Issues

1. **Chrome/ChromeDriver Issues**
   ```bash
   # Reinstall Chrome
   sudo apt remove google-chrome-stable
   sudo apt install google-chrome-stable
   
   # Check Chrome version
   google-chrome --version
   ```

2. **Permission Issues**
   ```bash
   # Fix permissions
   sudo chown -R root:root Galxe-Alert
   sudo chmod -R 755 Galxe-Alert
   ```

3. **Memory Issues**
   ```bash
   # Monitor memory usage
   htop
   
   # Check available memory
   free -h
   ```

4. **Service Won't Start**
   ```bash
   # Check service logs
   sudo journalctl -u galxe-bot -n 100
   
   # Test manual run
   cd Galxe-Alert
   source venv/bin/activate
   python main.py
   ```

### Bot-Specific Issues

1. **Telegram Token Invalid**
   - Verify bot token from @BotFather
   - Ensure bot is added to channel as admin

2. **No Quests Found**
   ```bash
   # Test scraper manually
   python debug_scraper.py
   ```

3. **Database Issues**
   ```bash
   # Reset database (WARNING: Will lose all data)
   rm quests.db
   python main.py
   ```

## VPS Optimization 🚀

### Resource Monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs -y

# Monitor system resources
htop
```

### Log Rotation
```bash
# Create logrotate config
sudo nano /etc/logrotate.d/galxe-bot

# Add content:
/var/log/galxe-bot.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}
```

### Firewall Setup
```bash
# Allow SSH and block unnecessary ports
sudo ufw allow ssh
sudo ufw enable
```

## Features Summary 🎯

- ✅ **5-minute monitoring intervals**
- ✅ **Direct quest links only**
- ✅ **No duplicate notifications**
- ✅ **6 projects monitored**
- ✅ **Automatic ChromeDriver management**
- ✅ **Robust error handling**
- ✅ **VPS optimized for 24/7 operation**
- ✅ **Systemd service support**
- ✅ **Screen session support**

## Support 💬

If you encounter issues:
1. Check the troubleshooting section
2. Review system logs: `sudo journalctl -u galxe-bot -f`
3. Test components manually
4. Open an issue on GitHub

---

**Ready to catch those new quests on your VPS! 🚀** 