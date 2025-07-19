#!/usr/bin/env python3
"""
Test script to send the latest quest from each project to Telegram
"""

import asyncio
import logging
from scraper import GalxeScraper
from telegram_bot import TelegramBot
from config import PROJECTS

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def test_telegram_notifications():
    """Test sending quest notifications to Telegram"""
    print("🧪 Testing Telegram Quest Notifications")
    print("=" * 50)
    
    # Initialize Telegram bot
    telegram_bot = TelegramBot()
    
    # Test connection
    print("📱 Testing Telegram connection...")
    connected = await telegram_bot.test_connection()
    if not connected:
        print("❌ Failed to connect to Telegram")
        return
    
    print("✅ Telegram connection successful")
    
    # Scrape quests and send notifications
    with GalxeScraper() as scraper:
        for project_name, project_data in PROJECTS.items():
            print(f"\n🔍 Checking {project_name}...")
            
            try:
                # Scrape quests
                quests = scraper.scrape_quests(project_name, project_data['quest_url'])
                
                if quests:
                    # Get the latest quest (first one in the list)
                    latest_quest = quests[0]
                    print(f"✅ Found quest: {latest_quest['quest_title']}")
                    
                    # Send notification
                    success = await telegram_bot.send_quest_notification(latest_quest)
                    
                    if success:
                        print(f"✅ Sent notification for {project_name}")
                    else:
                        print(f"❌ Failed to send notification for {project_name}")
                    
                    # Small delay between notifications
                    await asyncio.sleep(2)
                    
                else:
                    print(f"⚠️  No quests found for {project_name}")
                    
            except Exception as e:
                print(f"❌ Error processing {project_name}: {e}")
    
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    asyncio.run(test_telegram_notifications()) 