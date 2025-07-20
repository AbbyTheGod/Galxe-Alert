import time
import sqlite3
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Projects to monitor
PROJECTS = ['D3', 'T-REXNetwork', 'Fleek', 'Rayls', 'zkVerify', 'Mawari']

# selenium setup
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920x1080')
driver = webdriver.Chrome(options=options)

# sqlite setup
conn = sqlite3.connect("quests_test.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS quests (
        url TEXT PRIMARY KEY
    )
""")
conn.commit()

# format quest message to match Discord style
def format_quest_message(project_name, quest_title, quest_url, network, quest_type):
    return f"""{project_name}

{quest_title}
{quest_url}
Network: #{network}
TYPE: #{quest_type}
#galxe"""

# helper to check if url already seen
def is_new_quest(url):
    cursor.execute("SELECT 1 FROM quests WHERE url=?", (url,))
    return cursor.fetchone() is None

def save_quest(url):
    cursor.execute("INSERT OR IGNORE INTO quests(url) VALUES (?)", (url,))
    conn.commit()

def extract_network(element):
    """Extract network from quest element"""
    text = element.get_text().lower()
    networks = ['ethereum', 'polygon', 'arbitrum', 'optimism', 'bsc', 'avalanche', 'solana', 'base', 'gravity_alpha']
    for network in networks:
        if network in text:
            return network.upper()
    return "UNKNOWN"

def extract_quest_type(element):
    """Extract quest type from quest element"""
    text = element.get_text().lower()
    if 'points' in text:
        return "Points"
    elif 'social' in text:
        return "Social"
    elif 'quiz' in text:
        return "Quiz"
    elif 'task' in text:
        return "Task"
    elif 'campaign' in text:
        return "Campaign"
    else:
        return "Quest"

def extract_quests(project):
    base_url = f"https://app.galxe.com/quest/{project}"
    print(f"[→] checking: {project}")
    try:
        driver.get(base_url)
        time.sleep(5)  # wait for JavaScript content to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        quest_cards = soup.select('[data-testid="campaign-card"], [data-testid="quest-card"], .card, a[href*="/campaign/"], a[href*="/quest/"]')
        print(f"Found {len(quest_cards)} potential quest cards")
        
        for i, card in enumerate(quest_cards[:3]):  # Only test first 3 cards
            try:
                title = card.get_text(strip=True)
                href = card.get("href")
                if not href or "/campaign/" not in href and "/quest/" not in href:
                    continue
                full_url = "https://app.galxe.com" + href
                
                # Try to extract network and type from the quest data
                network = extract_network(card)
                quest_type = extract_quest_type(card)

                message = format_quest_message(project, title, full_url, network, quest_type)
                
                print(f"\n{'='*60}")
                print(f"TEST MESSAGE #{i+1} for {project}:")
                print('='*60)
                print(message)
                print('='*60)
                
                if not is_new_quest(full_url):
                    print("(This quest already exists in database)")
                else:
                    print("(This would be a NEW quest)")
                
            except Exception as e:
                print(f"[!] failed to process card: {e}")
    except Exception as e:
        print(f"[!] failed to load {project}: {e}")

# test function - now scrapes real data
def test_real_scraping():
    print("🧪 TESTING REAL SCRAPING FROM GALXE")
    print("="*60)
    
    # Test with real scraping from first project
    test_project = PROJECTS[0]  # D3
    print(f"🌐 Testing with real data from: {test_project}")
    
    base_url = f"https://app.galxe.com/quest/{test_project}"
    try:
        driver.get(base_url)
        time.sleep(5)  # wait for JavaScript content to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        quest_cards = soup.select('[data-testid="campaign-card"], [data-testid="quest-card"], .card, a[href*="/campaign/"], a[href*="/quest/"]')
        print(f"Found {len(quest_cards)} potential quest cards")
        
        real_quests_found = 0
        for i, card in enumerate(quest_cards[:5]):  # Test first 5 cards
            try:
                title = card.get_text(strip=True)
                href = card.get("href")
                
                if not href or "/campaign/" not in href and "/quest/" not in href:
                    continue
                    
                full_url = "https://app.galxe.com" + href
                
                # Skip if title is too short or seems invalid
                if len(title) < 5 or title.lower() in ['galxe', 'quest', 'campaign']:
                    continue
                
                # Try to extract network and type from the quest data
                network = extract_network(card)
                quest_type = extract_quest_type(card)

                message = format_quest_message(test_project, title, full_url, network, quest_type)
                
                real_quests_found += 1
                print(f"\n{'='*60}")
                print(f"REAL QUEST #{real_quests_found} from {test_project}:")
                print('='*60)
                print(message)
                print('='*60)
                
                if not is_new_quest(full_url):
                    print("(This quest already exists in database)")
                else:
                    print("(This would be a NEW quest)")
                
                # Only show first 3 real quests to avoid spam
                if real_quests_found >= 3:
                    break
                
            except Exception as e:
                print(f"[!] failed to process card: {e}")
                
        if real_quests_found == 0:
            print("❌ No valid quests found. This might indicate:")
            print("   - Galxe page structure changed")
            print("   - Selectors need updating")
            print("   - Network issues")
            
    except Exception as e:
        print(f"[!] failed to load {test_project}: {e}")
    
    print("\n" + "="*60)
    print("✅ REAL SCRAPING TEST COMPLETE")
    print("="*60)

# main test
if __name__ == '__main__':
    print("🧪 Starting Galxe Quest Monitor TEST...")
    print(f"📊 Will test {len(PROJECTS)} projects: {', '.join(PROJECTS)}")
    print("⚠️  This is a TEST - no messages will be sent to Telegram")
    print("="*60)
    
    # Test with real scraping from Galxe
    test_real_scraping()
    
    try:
        print("\n🌐 TESTING ADDITIONAL PROJECTS...")
        print("="*60)
        
        for project in PROJECTS[1:3]:  # Test next 2 projects
            extract_quests(project)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    finally:
        print("\n🧹 Cleaning up...")
        driver.quit()
        conn.close()
        print("✅ Test completed!") 