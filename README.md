# Galxe Quest Monitor Bot 🤖

A fully automated Telegram bot that monitors Galxe quest pages for specific projects and sends new quest notifications to a Telegram channel.

## Features ✨

- 🔍 **Automated Monitoring**: Continuously monitors multiple Galxe project pages every 5 minutes
- 📱 **Telegram Notifications**: Sends direct quest links only (clean format)
- 🗄️ **Database Storage**: Tracks quests to avoid duplicate notifications
- ⚡ **Smart Scraping**: Uses Selenium for dynamic content handling
- 🔄 **Fast Response**: Checks every 5 minutes for maximum responsiveness
- 📊 **Error Handling**: Robust error handling with logging
- 🛡️ **Rate Limiting**: Respectful scraping with delays between requests

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

- Python 3.8 or higher
- Chrome browser (for Selenium WebDriver)
- Telegram Bot Token (from @BotFather)
- Telegram Channel (public or private)

## Installation 🚀

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbbyTheGod/Galxe-Alert.git
   cd Galxe-Alert
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example file
   cp env_example.txt .env
   
   # Edit .env with your credentials
   # On Windows: notepad .env
   # On Mac/Linux: nano .env
   ```

4. **Configure your bot**
   - Get a bot token from [@BotFather](https://t.me/BotFather) on Telegram
   - Create a channel and add your bot as an administrator
   - Update the `.env` file with your bot token and channel ID

## Configuration ⚙️

### Environment Variables

Create a `.env` file with the following variables:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_username_or_id
```

### Current Settings

- **Scraping Interval**: Every 5 minutes
- **Notification Format**: Direct quest links only
- **Projects Monitored**: 6 projects (D3, T-REXNetwork, Fleek, Rayls, zkVerify, Mawari)

### Adding New Projects

Edit `config.py` to add more projects:

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

## Usage 🎮

### Quick Start

```bash
# Run the bot directly
python main.py

# Or use the helper script (Windows)
start_bot.bat

# Or use the Python runner
python run_bot.py
```

### Testing

```bash
# Test all components
python test_bot.py

# Test Telegram notifications
python test_telegram_notifications.py

# Debug scraper
python debug_scraper.py
```

## How It Works 🔧

1. **Initialization**: Bot sets up database and loads project configurations
2. **Monitoring Loop**: Checks each project's quest page every 5 minutes
3. **Web Scraping**: Uses Selenium to handle dynamic content on Galxe
4. **Quest Detection**: Extracts quest information using multiple selectors
5. **Database Storage**: Stores new quests and tracks notification status
6. **Telegram Notifications**: Sends direct quest links only
7. **Error Handling**: Logs errors and continues monitoring

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
├── run_bot.py                   # Bot runner with checks
├── start_bot.bat                # Windows batch file
├── requirements.txt             # Python dependencies
├── env_example.txt              # Environment variables example
├── .gitignore                   # Git ignore file
├── README.md                    # This file
└── quests.db                    # SQLite database (created automatically)
```

## Notification Format 📱

The bot sends clean, simple notifications:
```
https://galxe.com/quest/ProjectName/QuestID
```

Just the direct link - no extra text, no project names, no metadata.

## Customization 🎨

### Changing Monitoring Frequency

Edit `config.py`:
```python
SCRAPING_INTERVAL_MINUTES = 10  # Check every 10 minutes
```

### Modifying Notification Format

Edit `telegram_bot.py` in the `_format_quest_message` method:
```python
def _format_quest_message(self, quest_data):
    quest_url = quest_data.get('quest_url', '')
    return quest_url  # Just the URL
```

## Troubleshooting 🔧

### Common Issues

1. **Bot Token Invalid**
   - Verify your bot token from @BotFather
   - Ensure the bot is added to your channel as admin

2. **Channel ID Issues**
   - For public channels: Use `@channel_username`
   - For private channels: Forward a message to @userinfobot to get the ID

3. **Selenium Errors**
   - Ensure Chrome is installed
   - Update Chrome to the latest version
   - ChromeDriver is automatically managed

4. **No Quests Found**
   - Galxe may have changed their HTML structure
   - Check the logs for scraping errors
   - Run `python debug_scraper.py` to test scraping

### Logs

Check the console output for detailed information. The bot logs all activities.

## Features Summary 🎯

- ✅ **5-minute monitoring intervals**
- ✅ **Direct quest links only**
- ✅ **No duplicate notifications**
- ✅ **6 projects monitored**
- ✅ **Automatic ChromeDriver management**
- ✅ **Robust error handling**
- ✅ **Easy configuration**

## Support 💬

If you encounter issues:
1. Check the troubleshooting section
2. Review the console logs
3. Run the test scripts
4. Open an issue on GitHub

---

**Ready to catch those new quests! 🚀** 