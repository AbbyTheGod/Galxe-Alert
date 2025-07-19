#!/usr/bin/env python3
"""
Debug script to test the Galxe scraper and see what it's finding
"""

import asyncio
import logging
from scraper import GalxeScraper
from config import PROJECTS

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def debug_scraper():
    """Debug the scraper to see what it's finding"""
    print("🔍 Debugging Galxe Scraper")
    print("=" * 50)
    
    with GalxeScraper() as scraper:
        for project_name, project_data in PROJECTS.items():
            print(f"\n📋 Testing {project_name}...")
            print(f"URL: {project_data['quest_url']}")
            
            # Get page content
            content = scraper.get_page_content(project_data['quest_url'], use_selenium=True)
            if not content:
                print("❌ Failed to get page content")
                continue
            
            print(f"✅ Got page content ({len(content)} characters)")
            
            # Test quest extraction
            quests = scraper.scrape_quests(project_name, project_data['quest_url'])
            
            if quests:
                print(f"✅ Found {len(quests)} quests:")
                for i, quest in enumerate(quests, 1):
                    print(f"   {i}. {quest['quest_title']}")
                    print(f"      URL: {quest['quest_url']}")
                    if quest.get('quest_description'):
                        print(f"      Desc: {quest['quest_description'][:100]}...")
            else:
                print("❌ No quests found")
            
            print("-" * 30)

if __name__ == "__main__":
    asyncio.run(debug_scraper()) 