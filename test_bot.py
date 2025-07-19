#!/usr/bin/env python3
"""
Test script for Galxe Quest Monitor Bot
Tests all components before running the full bot
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import config
        print("✅ config.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import config.py: {e}")
        return False
    
    try:
        import database
        print("✅ database.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import database.py: {e}")
        return False
    
    try:
        import scraper
        print("✅ scraper.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import scraper.py: {e}")
        return False
    
    try:
        import telegram_bot
        print("✅ telegram_bot.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import telegram_bot.py: {e}")
        return False
    
    return True

def test_database():
    """Test database operations"""
    print("\n🗄️  Testing database...")
    
    try:
        from database import QuestDatabase
        db = QuestDatabase()
        print("✅ Database initialized successfully")
        
        # Test adding a project
        db.add_project("TestProject", "https://galxe.com/test", "https://galxe.com/test/campaigns")
        print("✅ Project addition test passed")
        
        # Test adding a quest
        success = db.add_quest("TestProject", "Test Quest", "https://galxe.com/test/quest", "Test description")
        print("✅ Quest addition test passed")
        
        # Test quest existence check
        exists = db.quest_exists("https://galxe.com/test/quest")
        print(f"✅ Quest existence check: {exists}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

async def test_telegram():
    """Test Telegram bot connection"""
    print("\n📱 Testing Telegram connection...")
    
    try:
        from telegram_bot import TelegramBot
        from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
        
        if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
            print("⚠️  Telegram credentials not configured")
            print("   To configure:")
            print("   1. Get a bot token from @BotFather on Telegram")
            print("   2. Create a channel and add your bot as admin")
            print("   3. Edit the .env file with your credentials")
            print("   4. Run this test again")
            return True  # Don't fail the test, just warn
        
        if not TELEGRAM_CHANNEL_ID or TELEGRAM_CHANNEL_ID == "@your_channel_username_or_id":
            print("⚠️  Telegram channel ID not configured")
            print("   To configure:")
            print("   1. Create a Telegram channel")
            print("   2. Add your bot as administrator")
            print("   3. For public channels: use @channel_username")
            print("   4. For private channels: forward a message to @userinfobot to get ID")
            print("   5. Edit the .env file with your channel ID")
            return True  # Don't fail the test, just warn
        
        bot = TelegramBot()
        connected = await bot.test_connection()
        
        if connected:
            print("✅ Telegram connection successful")
            return True
        else:
            print("❌ Telegram connection failed")
            print("   Check your bot token and channel ID")
            return False
            
    except Exception as e:
        print(f"❌ Telegram test failed: {e}")
        print("   Make sure your bot token and channel ID are correct")
        return False

def test_scraper():
    """Test scraper functionality"""
    print("\n🌐 Testing scraper...")
    
    try:
        from scraper import GalxeScraper
        
        # Test scraper initialization
        with GalxeScraper() as scraper:
            print("✅ Scraper initialized successfully")
            
            # Test basic page content retrieval
            test_url = "https://galxe.com"
            content = scraper.get_page_content(test_url, use_selenium=False)
            
            if content and len(content) > 1000:
                print("✅ Basic page content retrieval successful")
                return True
            else:
                print("❌ Page content retrieval failed")
                return False
                
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n⚙️  Testing configuration...")
    
    try:
        from config import PROJECTS, SCRAPING_INTERVAL_MINUTES
        
        if PROJECTS and len(PROJECTS) > 0:
            print(f"✅ Configuration loaded: {len(PROJECTS)} projects configured")
            
            for project_name, project_data in PROJECTS.items():
                print(f"   - {project_name}: {project_data['quest_url']}")
            
            print(f"✅ Scraping interval: {SCRAPING_INTERVAL_MINUTES} minutes")
            return True
        else:
            print("❌ No projects configured")
            return False
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 Galxe Quest Monitor Bot - Component Tests")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Database", test_database),
        ("Scraper", test_scraper),
        ("Telegram", test_telegram),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
                
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Bot is ready to run.")
        print("\nTo start the bot, run:")
        print("   python run_bot.py")
        return True
    else:
        print("⚠️  Some tests failed. Please fix the issues before running the bot.")
        print("\n📋 Next Steps:")
        print("1. Configure your Telegram bot credentials in the .env file")
        print("2. Run 'python test_bot.py' again to verify everything works")
        print("3. Start the bot with 'python run_bot.py'")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        sys.exit(1) 