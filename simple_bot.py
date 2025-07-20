import time
import sqlite3
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Projects to monitor
PROJECTS = ['D3', 'T-REXNetwork', 'Fleek', 'Rayls', 'zkVerify', 'Mawari', 'OP_NET', 'Irys', 'Donut Browser', 'Lit Protocol', 'KarrierOne', 'Genlayer', 'plasma', 'dango', 'ducat']

# telegram bot setup
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# selenium setup
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920x1080')
driver = webdriver.Chrome(options=options)

# sqlite setup
conn = sqlite3.connect("quests.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS quests (
        url TEXT PRIMARY KEY
    )
""")
conn.commit()

# format quest message - just the link only
def format_quest_message(quest_url):
    return quest_url

# helper to check if url already seen
def is_new_quest(url):
    cursor.execute("SELECT 1 FROM quests WHERE url=?", (url,))
    return cursor.fetchone() is None

def save_quest(url):
    cursor.execute("INSERT OR IGNORE INTO quests(url) VALUES (?)", (url,))
    conn.commit()

def extract_quests(project):
    base_url = f"https://app.galxe.com/quest/{project}"
    print(f"[→] checking: {project}")
    try:
        driver.get(base_url)
        time.sleep(5)  # wait for JavaScript content to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        quest_cards = soup.select('[data-testid="campaign-card"], [data-testid="quest-card"], .card, a[href*="/campaign/"], a[href*="/quest/"]')
        for card in quest_cards:
            try:
                title = card.get_text(strip=True)
                href = card.get("href")
                if not href or "/campaign/" not in href and "/quest/" not in href:
                    continue
                full_url = "https://app.galxe.com" + href
                if not is_new_quest(full_url):
                    continue
                
                message = format_quest_message(full_url)
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
                save_quest(full_url)
                print(f"[✓] Sent new quest: {title[:50]}...")
            except Exception as e:
                print(f"[!] failed to process card: {e}")
    except Exception as e:
        print(f"[!] failed to load {project}: {e}")



# main loop
if __name__ == '__main__':
    print("🚀 Starting Galxe Quest Monitor...")
    print(f"📊 Monitoring {len(PROJECTS)} projects: {', '.join(PROJECTS)}")
    print("⏰ Check interval: 30 minutes")
    print("=" * 50)
    
    try:
        while True:
            for project in PROJECTS:
                extract_quests(project)
                time.sleep(2)  # Small delay between projects
            print(f"😴 Sleeping for 30 minutes... Next check at {time.strftime('%H:%M:%S')}")
            time.sleep(1800)  # 30 minutes
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        driver.quit()
        conn.close() 