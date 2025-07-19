# Galxe Quest Monitor Bot 🤖

A fully automated Telegram bot that monitors Galxe quest pages for specific projects (like D3, T-REXNetwork, Arbitrum, Polygon, Optimism, etc.) and sends new quest notifications to a Telegram channel.

## Features ✨

- 🔍 **Automated Monitoring**: Continuously monitors multiple Galxe project pages
- 📱 **Telegram Notifications**: Sends formatted quest alerts with direct links
- 🗄️ **Database Storage**: Tracks quests to avoid duplicate notifications
- 🖼️ **Rich Media Support**: Includes quest images when available
- ⚡ **Smart Scraping**: Uses both requests and Selenium for dynamic content
- 🔄 **Configurable Intervals**: Customizable monitoring frequency
- 📊 **Error Handling**: Robust error handling with Telegram alerts
- 🛡️ **Rate Limiting**: Respectful scraping with delays between requests

## Supported Projects 🎯

Currently monitoring:
- **D3** - https://galxe.com/D3
- **T-REXNetwork** - https://galxe.com/T-REXNetwork
- **Arbitrum** - https://galxe.com/arbitrum
- **Polygon** - https://galxe.com/polygon
- **Optimism** - https://galxe.com/optimism

*Easy to add more projects in the configuration!*

## Prerequisites 📋

- Python 3.8 or higher
- Chrome browser (for Selenium WebDriver)
- Telegram Bot Token (from @BotFather)
- Telegram Channel (public or private)

## Installation 🚀

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd galxe-quest-bot
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
   nano .env
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

# Optional: Override default scraping interval (in minutes)
SCRAPING_INTERVAL_MINUTES=30
```

### Adding New Projects

Edit `config.py` to add more projects:

```python
PROJECTS = {
    'YourProject': {
        'name': 'YourProject',
        'url': 'https://galxe.com/YourProject',
        'quest_url': 'https://galxe.com/YourProject/campaigns'
    },
    # ... existing projects
}
```

## Usage 🎮

### Running the Bot

```bash
python main.py
```

The bot will:
1. Initialize the database
2. Test Telegram connection
3. Send a startup message
4. Begin monitoring quest pages
5. Send notifications for new quests

### Bot Commands

The bot automatically sends:
- **Startup Message**: Confirms the bot is running
- **Quest Notifications**: New quest alerts with project info and direct links
- **Error Alerts**: When issues occur during monitoring
- **Status Updates**: Periodic status reports (can be implemented)

## Project Structure 📁

```
galxe-quest-bot/
├── main.py              # Main bot script
├── config.py            # Configuration settings
├── database.py          # Database operations
├── scraper.py           # Web scraping functionality
├── telegram_bot.py      # Telegram bot interface
├── requirements.txt     # Python dependencies
├── env_example.txt      # Environment variables example
├── README.md           # This file
└── quests.db           # SQLite database (created automatically)
```

## How It Works 🔧

1. **Initialization**: Bot sets up database and loads project configurations
2. **Monitoring Loop**: Checks each project's quest page at regular intervals
3. **Web Scraping**: Uses Selenium to handle dynamic content on Galxe
4. **Quest Detection**: Extracts quest information using multiple selectors
5. **Database Storage**: Stores new quests and tracks notification status
6. **Telegram Notifications**: Sends formatted messages with quest details
7. **Error Handling**: Logs errors and sends alerts for critical issues

## Database Schema 🗄️

The bot uses SQLite with three main tables:

- **quests**: Stores quest information and metadata
- **projects**: Tracks monitored projects and their URLs
- **notifications**: Records sent notifications to avoid duplicates

## Customization 🎨

### Changing Monitoring Frequency

Edit `config.py`:
```python
SCRAPING_INTERVAL_MINUTES = 15  # Check every 15 minutes
```

### Modifying Quest Message Format

Edit `telegram_bot.py` in the `_format_quest_message` method:
```python
def _format_quest_message(self, quest_data):
    # Customize your message format here
    message = f"🎯 New Quest: {quest_data['quest_title']}"
    return message
```

### Adding More Scraping Selectors

Edit `scraper.py` to add more CSS selectors for quest detection:
```python
quest_selectors = [
    '[data-testid="campaign-card"]',
    '.campaign-card',
    '.your-custom-selector',  # Add your selectors here
]
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
   - Check if ChromeDriver is compatible

4. **No Quests Found**
   - Galxe may have changed their HTML structure
   - Check the logs for scraping errors
   - Update selectors in `scraper.py`

### Logs

Check the `bot.log` file for detailed information:
```bash
tail -f bot.log
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer ⚠️

This bot is for educational and personal use. Please:
- Respect Galxe's terms of service
- Use reasonable scraping intervals
- Don't overload their servers
- Monitor your bot's behavior

## Support 💬

If you encounter issues:
1. Check the troubleshooting section
2. Review the logs
3. Open an issue on GitHub
4. Provide detailed error information

---

**Happy Quest Hunting! 🚀** 