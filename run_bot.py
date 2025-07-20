#!/usr/bin/env python3
"""
Simple runner script for the Galxe Quest Monitor Bot
Enhanced version with better error handling and status reporting
"""

import sys
import os
import asyncio
import logging
import time
from pathlib import Path
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    dependencies = {
        'telegram': 'python-telegram-bot',
        'requests': 'requests',
        'bs4': 'beautifulsoup4',
        'selenium': 'selenium',
        'dotenv': 'python-dotenv',
        'sqlite3': 'built-in',
        'asyncio': 'built-in'
    }
    
    missing_deps = []
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {package}")
        except ImportError:
            missing_deps.append(package)
            print(f"❌ {package}")
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def check_environment():
    """Check if environment variables are set"""
    print("\n🔍 Checking environment variables...")
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHANNEL_ID']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            print(f"❌ {var}: Not set")
        elif value == "your_telegram_bot_token_here" or value == "your_telegram_channel_id_here":
            missing_vars.append(var)
            print(f"❌ {var}: Still has placeholder value")
        else:
            print(f"✅ {var}: Configured")
    
    if missing_vars:
        print(f"\n❌ Missing or invalid environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file with the required variables")
        print("See env_example.txt for reference")
        return False
    
    print("✅ Environment variables are configured")
    return True

def check_files():
    """Check if required files exist"""
    print("\n🔍 Checking required files...")
    required_files = [
        'main.py',
        'config.py',
        'database.py',
        'scraper.py',
        'telegram_bot.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            missing_files.append(file)
            print(f"❌ {file}")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files are present")
    return True

def show_bot_info():
    """Show bot configuration information"""
    print("\n📊 Bot Configuration:")
    print("=" * 40)
    
    try:
        from config import PROJECTS, SCRAPING_INTERVAL_MINUTES
        print(f"📋 Projects to monitor: {len(PROJECTS)}")
        print(f"⏰ Check interval: {SCRAPING_INTERVAL_MINUTES} minutes")
        print(f"🔄 Requests per day: {len(PROJECTS) * (1440 // SCRAPING_INTERVAL_MINUTES)}")
        
        print("\n📋 Project List:")
        for i, (key, project) in enumerate(PROJECTS.items(), 1):
            print(f"  {i:2d}. {project['name']}")
        
    except ImportError as e:
        print(f"❌ Could not load configuration: {e}")

def main():
    """Main function"""
    print("🤖 Galxe Quest Monitor Bot")
    print("=" * 50)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing packages.")
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please configure your .env file.")
        sys.exit(1)
    
    # Check files
    if not check_files():
        print("\n❌ File check failed. Please ensure all required files are present.")
        sys.exit(1)
    
    # Show bot info
    show_bot_info()
    
    print("\n🚀 Starting bot...")
    print("💡 Press Ctrl+C to stop the bot")
    print("📱 Check your Telegram channel for notifications")
    print("-" * 50)
    
    try:
        # Import and run the main bot
        from main import main as bot_main
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Bot stopped by user")
        print("👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Bot error: {e}")
        print("🔧 Check the logs for more details")
        logging.error(f"Bot error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 