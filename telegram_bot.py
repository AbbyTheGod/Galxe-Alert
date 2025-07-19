import logging
import asyncio
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from database import QuestDatabase

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.channel_id = TELEGRAM_CHANNEL_ID
        self.db = QuestDatabase()
        
    async def send_quest_notification(self, quest_data):
        """Send a quest notification to the Telegram channel"""
        try:
            # Format the message
            message = self._format_quest_message(quest_data)
            
            # Send as plain text message only (no images)
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode=ParseMode.HTML
            )
            
            logging.info(f"Successfully sent quest notification for {quest_data['quest_title']}")
            return True
            
        except Exception as e:
            logging.error(f"Error sending quest notification: {e}")
            return False
    
    def _format_quest_message(self, quest_data):
        """Format quest data into a readable message"""
        quest_url = quest_data.get('quest_url', '')
        
        # Just return the quest URL only
        return quest_url
    
    async def send_status_message(self, status_data):
        """Send a status message to the channel"""
        try:
            message = f"""
📊 <b>Bot Status Update</b>

🔍 <b>Projects Monitored:</b> {status_data['total_projects']}
📈 <b>Total Quests Found:</b> {status_data['total_quests']}
🆕 <b>New Quests Today:</b> {status_data['new_quests_today']}
⏱️ <b>Last Check:</b> {status_data['last_check']}

✅ <b>Status:</b> Running normally
"""
            
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode=ParseMode.HTML
            )
            
            logging.info("Sent status message to channel")
            
        except Exception as e:
            logging.error(f"Error sending status message: {e}")
    
    async def send_error_message(self, error_message):
        """Send an error message to the channel"""
        try:
            message = f"""
⚠️ <b>Bot Error Alert</b>

❌ <b>Error:</b> {error_message}
⏰ <b>Time:</b> {asyncio.get_event_loop().time()}

Please check the bot logs for more details.
"""
            
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode=ParseMode.HTML
            )
            
            logging.info("Sent error message to channel")
            
        except Exception as e:
            logging.error(f"Error sending error message: {e}")
    
    async def test_connection(self):
        """Test the bot connection"""
        try:
            me = await self.bot.get_me()
            logging.info(f"Bot connection successful: {me.first_name} (@{me.username})")
            return True
        except Exception as e:
            logging.error(f"Bot connection failed: {e}")
            return False
    
    async def send_test_message(self):
        """Send a test message to verify the bot is working"""
        try:
            test_message = """
🤖 <b>Galxe Quest Bot Test</b>

✅ Bot is running and connected successfully!
🔍 Ready to monitor quest pages...

<i>This is a test message to verify the bot is working properly.</i>
"""
            
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=test_message,
                parse_mode=ParseMode.HTML
            )
            
            logging.info("Test message sent successfully")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send test message: {e}")
            return False 