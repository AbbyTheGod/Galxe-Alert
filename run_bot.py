#!/usr/bin/env python3
"""
Simple runner script for the Galxe Quest Monitor Bot
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import telegram
        import requests
        import bs4
        import selenium
        import dotenv
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_environment():
    """Check if environment variables are set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHANNEL_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file with the required variables")
        print("See env_example.txt for reference")
        return False
    
    print("✅ Environment variables are configured")
    return True

def main():
    """Main function"""
    print("🤖 Galxe Quest Monitor Bot")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    print("\n🚀 Starting bot...")
    print("Press Ctrl+C to stop the bot")
    print("-" * 40)
    
    try:
        # Import and run the main bot
        from main import main as bot_main
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot error: {e}")
        logging.error(f"Bot error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 