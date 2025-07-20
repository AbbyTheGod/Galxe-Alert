import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')

# Galxe Projects to Monitor
PROJECTS = {
    'D3': {
        'name': 'D3',
        'url': 'https://app.galxe.com/quest/D3',
        'quest_url': 'https://app.galxe.com/quest/D3'
    },
    'T-REXNetwork': {
        'name': 'T-REXNetwork',
        'url': 'https://app.galxe.com/quest/T-REXNetwork',
        'quest_url': 'https://app.galxe.com/quest/T-REXNetwork'
    },
    'Fleek': {
        'name': 'Fleek',
        'url': 'https://app.galxe.com/quest/fleek',
        'quest_url': 'https://app.galxe.com/quest/fleek'
    },
    'Rayls': {
        'name': 'Rayls',
        'url': 'https://app.galxe.com/quest/rayls',
        'quest_url': 'https://app.galxe.com/quest/rayls'
    },
    'zkVerify': {
        'name': 'zkVerify',
        'url': 'https://app.galxe.com/quest/zkverify',
        'quest_url': 'https://app.galxe.com/quest/zkverify'
    },
    'Mawari': {
        'name': 'Mawari',
        'url': 'https://app.galxe.com/quest/mawari',
        'quest_url': 'https://app.galxe.com/quest/mawari'
    },
    'WDKbxYkaZdwzc2f54sVSeb': {
        'name': 'WDKbxYkaZdwzc2f54sVSeb',
        'url': 'https://app.galxe.com/quest/WDKbxYkaZdwzc2f54sVSeb',
        'quest_url': 'https://app.galxe.com/quest/WDKbxYkaZdwzc2f54sVSeb'
    },
    'Irys': {
        'name': 'Irys',
        'url': 'https://app.galxe.com/quest/Irys',
        'quest_url': 'https://app.galxe.com/quest/Irys'
    },
    'DonutBrowser': {
        'name': 'Donut Browser',
        'url': 'https://app.galxe.com/quest/Donut%20Browser',
        'quest_url': 'https://app.galxe.com/quest/Donut%20Browser'
    },
    'LitProtocol': {
        'name': 'Lit Protocol',
        'url': 'https://app.galxe.com/quest/Lit%20Protocol',
        'quest_url': 'https://app.galxe.com/quest/Lit%20Protocol'
    },
    'KarrierOne': {
        'name': 'KarrierOne',
        'url': 'https://app.galxe.com/quest/KarrierOne',
        'quest_url': 'https://app.galxe.com/quest/KarrierOne'
    },
    'Genlayer': {
        'name': 'Genlayer',
        'url': 'https://app.galxe.com/quest/Genlayer',
        'quest_url': 'https://app.galxe.com/quest/Genlayer'
    },
    'plasma': {
        'name': 'plasma',
        'url': 'https://app.galxe.com/quest/plasma',
        'quest_url': 'https://app.galxe.com/quest/plasma'
    },
    'dango': {
        'name': 'dango',
        'url': 'https://app.galxe.com/quest/dango',
        'quest_url': 'https://app.galxe.com/quest/dango'
    },
    'ducat': {
        'name': 'ducat',
        'url': 'https://app.galxe.com/quest/ducat',
        'quest_url': 'https://app.galxe.com/quest/ducat'
    }
}

# Scraping Configuration
SCRAPING_INTERVAL_MINUTES = 30  # Check every 30 minutes
REQUEST_DELAY = 2  # Delay between requests in seconds
MAX_RETRIES = 3

# Database Configuration
DATABASE_PATH = 'quests.db'

# User Agent for web requests
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FILE = 'bot.log' 