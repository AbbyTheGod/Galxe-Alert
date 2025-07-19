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
        logger.info("Starting Galxe Quest Monitor Bot...")
        
        # Test Telegram connection
        if not await self.telegram_bot.test_connection():
            logger.error("Failed to connect to Telegram. Check your bot token.")
            return False
        
        # Send startup message
        await self.telegram_bot.send_test_message()
        
        self.is_running = True
        logger.info("Bot started successfully!")
        
        # Start monitoring
        await self.monitor_quests()
        
        return True
    
    async def monitor_quests(self):
        """Main monitoring loop"""
        logger.info("Starting quest monitoring...")
        
        while self.is_running:
            try:
                await self._check_all_projects()
                
                # Wait for next check
                logger.info(f"Waiting {SCRAPING_INTERVAL_MINUTES} minutes until next check...")
                await asyncio.sleep(SCRAPING_INTERVAL_MINUTES * 60)
                
            except KeyboardInterrupt:
                logger.info("Received interrupt signal, stopping bot...")
                self.is_running = False
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await self.telegram_bot.send_error_message(str(e))
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    async def _check_all_projects(self):
        """Check all projects for new quests"""
        logger.info("Checking all projects for new quests...")
        
        new_quests_found = 0
        
        with GalxeScraper() as scraper:
            self.scraper = scraper
            
            for project_key, project_data in PROJECTS.items():
                try:
                    await self._check_project(project_data)
                    new_quests_found += await self._process_new_quests(project_data['name'])
                    
                    # Small delay between projects to be respectful
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error checking project {project_data['name']}: {e}")
                    await self.telegram_bot.send_error_message(f"Error checking {project_data['name']}: {str(e)}")
        
        if new_quests_found > 0:
            logger.info(f"Found {new_quests_found} new quests across all projects")
        else:
            logger.info("No new quests found")
    
    async def _check_project(self, project_data):
        """Check a single project for new quests"""
        project_name = project_data['name']
        quest_url = project_data['quest_url']
        
        logger.info(f"Checking project: {project_name}")
        
        # Scrape quests from the project page
        quests = self.scraper.scrape_quests(project_name, quest_url)
        
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
                    logger.info(f"Added new quest: {quest['quest_title']} for {project_name}")
        
        # Update last checked timestamp
        self.db.update_project_last_checked(project_name)
    
    async def _process_new_quests(self, project_name):
        """Process and send notifications for new quests"""
        new_quests = self.db.get_new_quests(project_name)
        sent_count = 0
        
        for quest in new_quests:
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
                
                # Send notification
                success = await self.telegram_bot.send_quest_notification(quest_data)
                
                if success:
                    # Mark as notified
                    self.db.mark_quest_notified(quest[0])
                    sent_count += 1
                    logger.info(f"Sent notification for quest: {quest_data['quest_title']}")
                
                # Small delay between notifications
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing quest notification: {e}")
        
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
        logger.info("Stopping bot...")
        self.is_running = False
        if self.scraper:
            self.scraper.close_selenium()

async def main():
    """Main function"""
    # Validate configuration
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in environment variables")
        return
    
    if not TELEGRAM_CHANNEL_ID:
        logger.error("TELEGRAM_CHANNEL_ID not set in environment variables")
        return
    
    # Create and start bot
    bot = GalxeQuestBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        bot.stop()

if __name__ == "__main__":
    # Run the bot
    asyncio.run(main()) 