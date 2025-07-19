#!/usr/bin/env python3
"""
Galxe Quest Monitor Bot
Automated Telegram bot that monitors Galxe quest pages for specific projects
"""

import asyncio
import logging
import time
import schedule
from datetime import datetime, timedelta
from config import (
    PROJECTS, SCRAPING_INTERVAL_MINUTES, LOG_LEVEL, LOG_FILE,
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
)
from database import QuestDatabase
from scraper import GalxeScraper
from telegram_bot import TelegramBot

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class GalxeQuestBot:
    def __init__(self):
        self.db = QuestDatabase()
        self.telegram_bot = TelegramBot()
        self.scraper = None
        self.is_running = False
        
        # Initialize projects in database
        self._init_projects()
    
    def _init_projects(self):
        """Initialize projects in the database"""
        for project_key, project_data in PROJECTS.items():
            self.db.add_project(
                project_data['name'],
                project_data['url'],
                project_data['quest_url']
            )
        logger.info(f"Initialized {len(PROJECTS)} projects in database")
    
    async def start(self):
        """Start the bot"""
        logger.info("🚀 Starting Galxe Quest Monitor Bot...")
        logger.info(f"📊 Monitoring {len(PROJECTS)} projects: {', '.join([p['name'] for p in PROJECTS.values()])}")
        logger.info(f"⏰ Check interval: {SCRAPING_INTERVAL_MINUTES} minutes")
        
        # Test Telegram connection
        logger.info("📱 Testing Telegram connection...")
        if not await self.telegram_bot.test_connection():
            logger.error("❌ Failed to connect to Telegram. Check your bot token.")
            return False
        logger.info("✅ Telegram connection successful!")
        
        # Send startup message
        logger.info("📤 Sending startup message to Telegram...")
        await self.telegram_bot.send_test_message()
        
        self.is_running = True
        logger.info("🎉 Bot started successfully and ready to monitor!")
        
        # Start monitoring
        await self.monitor_quests()
        
        return True
    
    async def monitor_quests(self):
        """Main monitoring loop"""
        logger.info("🔍 Starting quest monitoring loop...")
        check_count = 0
        
        while self.is_running:
            try:
                check_count += 1
                logger.info(f"🔄 Starting check #{check_count} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                await self._check_all_projects()
                
                # Wait for next check
                next_check = datetime.now() + timedelta(minutes=SCRAPING_INTERVAL_MINUTES)
                logger.info(f"⏳ Next check scheduled for: {next_check.strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"😴 Sleeping for {SCRAPING_INTERVAL_MINUTES} minutes...")
                await asyncio.sleep(SCRAPING_INTERVAL_MINUTES * 60)
                
            except KeyboardInterrupt:
                logger.info("🛑 Received interrupt signal, stopping bot...")
                self.is_running = False
                break
            except Exception as e:
                logger.error(f"❌ Error in monitoring loop: {e}")
                await self.telegram_bot.send_error_message(str(e))
                logger.info("⏰ Waiting 1 minute before retrying...")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    async def _check_all_projects(self):
        """Check all projects for new quests"""
        logger.info("🔍 Checking all projects for new quests...")
        
        new_quests_found = 0
        total_quests_scraped = 0
        
        with GalxeScraper() as scraper:
            self.scraper = scraper
            logger.info("🌐 Web scraper initialized successfully")
            
            for i, (project_key, project_data) in enumerate(PROJECTS.items(), 1):
                try:
                    logger.info(f"📋 [{i}/{len(PROJECTS)}] Processing project: {project_data['name']}")
                    
                    await self._check_project(project_data)
                    project_new_quests = await self._process_new_quests(project_data['name'])
                    new_quests_found += project_new_quests
                    
                    if project_new_quests > 0:
                        logger.info(f"🎉 Found {project_new_quests} new quests for {project_data['name']}")
                    else:
                        logger.info(f"✅ No new quests for {project_data['name']}")
                    
                    # Small delay between projects to be respectful
                    if i < len(PROJECTS):  # Don't delay after the last project
                        logger.info("⏱️ Waiting 2 seconds before next project...")
                        await asyncio.sleep(2)
                    
                except Exception as e:
                    logger.error(f"❌ Error checking project {project_data['name']}: {e}")
                    await self.telegram_bot.send_error_message(f"Error checking {project_data['name']}: {str(e)}")
        
        # Summary
        if new_quests_found > 0:
            logger.info(f"🎊 SUMMARY: Found {new_quests_found} new quests across all projects!")
        else:
            logger.info("📭 SUMMARY: No new quests found in this check")
        
        logger.info(f"📊 Check completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    async def _check_project(self, project_data):
        """Check a single project for new quests"""
        project_name = project_data['name']
        quest_url = project_data['quest_url']
        
        logger.info(f"🌐 Scraping quests from: {quest_url}")
        
        # Scrape quests from the project page
        quests = self.scraper.scrape_quests(project_name, quest_url)
        logger.info(f"📄 Found {len(quests)} quests on {project_name} page")
        
        new_quests_added = 0
        # Add new quests to database
        for quest in quests:
            if not self.db.quest_exists(quest['quest_url']):
                success = self.db.add_quest(
                    quest['project_name'],
                    quest['quest_title'],
                    quest['quest_url'],
                    quest.get('quest_description'),
                    quest.get('quest_image')
                )
                if success:
                    new_quests_added += 1
                    logger.info(f"➕ Added new quest to database: {quest['quest_title'][:50]}...")
        
        if new_quests_added > 0:
            logger.info(f"💾 Added {new_quests_added} new quests to database for {project_name}")
        else:
            logger.info(f"📝 No new quests to add for {project_name}")
        
        # Update last checked timestamp
        self.db.update_project_last_checked(project_name)
        logger.info(f"⏰ Updated last check timestamp for {project_name}")
    
    async def _process_new_quests(self, project_name):
        """Process and send notifications for new quests"""
        new_quests = self.db.get_new_quests(project_name)
        
        if not new_quests:
            logger.info(f"📭 No new quests to process for {project_name}")
            return 0
        
        logger.info(f"📤 Processing {len(new_quests)} new quests for {project_name}")
        sent_count = 0
        
        for i, quest in enumerate(new_quests, 1):
            try:
                # Convert database row to dict
                quest_data = {
                    'project_name': quest[1],
                    'quest_title': quest[2],
                    'quest_url': quest[3],
                    'quest_description': quest[4],
                    'quest_image': quest[5],
                    'discovered_at': quest[8]
                }
                
                logger.info(f"📨 [{i}/{len(new_quests)}] Sending notification for: {quest_data['quest_title'][:50]}...")
                
                # Send notification
                success = await self.telegram_bot.send_quest_notification(quest_data)
                
                if success:
                    # Mark as notified
                    self.db.mark_quest_notified(quest[0])
                    sent_count += 1
                    logger.info(f"✅ Successfully sent notification for quest: {quest_data['quest_title'][:50]}...")
                else:
                    logger.error(f"❌ Failed to send notification for quest: {quest_data['quest_title'][:50]}...")
                
                # Small delay between notifications
                if i < len(new_quests):  # Don't delay after the last notification
                    logger.info("⏱️ Waiting 1 second before next notification...")
                    await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Error processing quest notification: {e}")
        
        logger.info(f"📊 Sent {sent_count}/{len(new_quests)} notifications for {project_name}")
        return sent_count
    
    async def send_status_report(self):
        """Send a status report to the channel"""
        try:
            # Get status data
            projects = self.db.get_all_projects()
            
            status_data = {
                'total_projects': len(projects),
                'total_quests': 0,  # Would need to implement this
                'new_quests_today': 0,  # Would need to implement this
                'last_check': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            await self.telegram_bot.send_status_message(status_data)
            
        except Exception as e:
            logger.error(f"Error sending status report: {e}")
    
    def stop(self):
        """Stop the bot"""
        logger.info("🛑 Stopping Galxe Quest Monitor Bot...")
        self.is_running = False
        if self.scraper:
            logger.info("🔧 Closing web scraper...")
            self.scraper.close_selenium()
        logger.info("👋 Bot stopped successfully!")

async def main():
    """Main function"""
    logger.info("🎯 Galxe Quest Monitor Bot - Starting up...")
    logger.info("=" * 60)
    
    # Validate configuration
    if not TELEGRAM_BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN not set in environment variables")
        return
    
    if not TELEGRAM_CHANNEL_ID:
        logger.error("❌ TELEGRAM_CHANNEL_ID not set in environment variables")
        return
    
    logger.info("✅ Environment variables validated successfully")
    
    # Create and start bot
    logger.info("🔧 Initializing bot components...")
    bot = GalxeQuestBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("🛑 Bot interrupted by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
    finally:
        bot.stop()
        logger.info("=" * 60)
        logger.info("👋 Bot shutdown complete")

if __name__ == "__main__":
    # Run the bot
    asyncio.run(main()) 