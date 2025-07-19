import requests
import time
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from config import USER_AGENT, REQUEST_DELAY, MAX_RETRIES

class GalxeScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': UserAgent().random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.driver = None
        
    def setup_selenium(self):
        """Setup Selenium WebDriver for dynamic content"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument(f'--user-agent={UserAgent().random}')
            
            self.driver = webdriver.Chrome(
                options=chrome_options
            )
            logging.info("Selenium WebDriver setup successfully")
            
        except Exception as e:
            logging.error(f"Error setting up Selenium: {e}")
            self.driver = None
    
    def close_selenium(self):
        """Close Selenium WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
                logging.info("Selenium WebDriver closed")
            except Exception as e:
                logging.error(f"Error closing Selenium: {e}")
    
    def get_page_content(self, url, use_selenium=False):
        """Get page content using either requests or Selenium"""
        for attempt in range(MAX_RETRIES):
            try:
                if use_selenium and self.driver:
                    return self._get_content_selenium(url)
                else:
                    return self._get_content_requests(url)
                    
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(REQUEST_DELAY * (attempt + 1))
                else:
                    logging.error(f"Failed to get content from {url} after {MAX_RETRIES} attempts")
                    return None
    
    def _get_content_requests(self, url):
        """Get page content using requests"""
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    
    def _get_content_selenium(self, url):
        """Get page content using Selenium"""
        self.driver.get(url)
        
        # Wait for content to load
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Additional wait for dynamic content
        time.sleep(5)
        
        return self.driver.page_source
    
    def scrape_quests(self, project_name, quest_url):
        """Scrape quests from a project's campaign page"""
        logging.info(f"Scraping quests for {project_name} from {quest_url}")
        
        content = self.get_page_content(quest_url, use_selenium=True)
        if not content:
            return []
        
        quests = []
        soup = BeautifulSoup(content, 'html.parser')
        
        try:
            # Enhanced quest selectors for current Galxe structure
            quest_selectors = [
                # Modern Galxe selectors
                '[data-testid="campaign-card"]',
                '[data-testid="quest-card"]',
                '.campaign-card',
                '.quest-card',
                '.card[href*="/campaign/"]',
                '.card[href*="/quest/"]',
                # Generic selectors
                '[class*="campaign"]',
                '[class*="quest"]',
                '[class*="Card"]',
                '.card',
                # Link-based selectors
                'a[href*="/campaign/"]',
                'a[href*="/quest/"]'
            ]
            
            quest_elements = []
            for selector in quest_selectors:
                quest_elements = soup.select(selector)
                if quest_elements:
                    logging.info(f"Found {len(quest_elements)} quests using selector: {selector}")
                    break
            
            if not quest_elements:
                # Fallback: look for any links that might be quests
                all_links = soup.find_all('a', href=True)
                quest_links = [elem for elem in all_links if '/campaign/' in elem.get('href', '') or '/quest/' in elem.get('href', '')]
                logging.info(f"Found {len(quest_links)} potential quest links from all links")
                
                # Also look for divs that might contain quest info
                quest_divs = soup.find_all('div', class_=lambda x: x and any(word in x.lower() for word in ['campaign', 'quest', 'card']))
                logging.info(f"Found {len(quest_divs)} potential quest divs")
                
                quest_elements = quest_links + quest_divs
            
            # Debug: Log page structure
            logging.info(f"Page title: {soup.title.string if soup.title else 'No title'}")
            logging.info(f"Total links found: {len(soup.find_all('a', href=True))}")
            
            for element in quest_elements:
                quest_data = self._extract_quest_data(element, project_name)
                if quest_data:
                    quests.append(quest_data)
            
            logging.info(f"Successfully extracted {len(quests)} quests for {project_name}")
            
        except Exception as e:
            logging.error(f"Error scraping quests for {project_name}: {e}")
        
        return quests
    
    def _extract_quest_data(self, element, project_name):
        """Extract quest data from a single element"""
        try:
            # Try to get quest URL
            quest_url = None
            if element.name == 'a':
                quest_url = element.get('href')
            else:
                link_elem = element.find('a', href=True)
                if link_elem:
                    quest_url = link_elem.get('href')
            
            if not quest_url:
                # Try to find URL in parent or child elements
                parent = element.parent
                if parent and parent.name == 'a':
                    quest_url = parent.get('href')
                else:
                    # Look for any link within this element
                    all_links = element.find_all('a', href=True)
                    for link in all_links:
                        href = link.get('href', '')
                        if '/campaign/' in href or '/quest/' in href:
                            quest_url = href
                            break
            
            if not quest_url:
                return None
            
            # Make URL absolute if it's relative
            if quest_url.startswith('/'):
                quest_url = f"https://galxe.com{quest_url}"
            elif not quest_url.startswith('http'):
                quest_url = f"https://galxe.com/{quest_url}"
            
            # Extract quest title
            quest_title = self._extract_text(element)
            if not quest_title:
                return None
            
            # Extract quest description
            quest_description = self._extract_description(element)
            
            # Extract quest image
            quest_image = self._extract_image(element)
            
            # Extract network and quest type
            network = self._extract_network(element)
            quest_type = self._extract_quest_type(element)
            
            # Debug logging
            logging.info(f"Extracted quest: {quest_title} -> {quest_url}")
            
            return {
                'project_name': project_name,
                'quest_title': quest_title.strip(),
                'quest_url': quest_url,
                'quest_description': quest_description.strip() if quest_description else None,
                'quest_image': quest_image,
                'network': network,
                'quest_type': quest_type
            }
            
        except Exception as e:
            logging.error(f"Error extracting quest data: {e}")
            return None
    
    def _extract_text(self, element):
        """Extract text content from element"""
        # Try multiple selectors for title
        title_selectors = [
            '[data-testid="campaign-title"]',
            '.campaign-title',
            '.quest-title',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            '[class*="title"]',
            '[class*="name"]'
        ]
        
        for selector in title_selectors:
            title_elem = element.select_one(selector)
            if title_elem and title_elem.get_text(strip=True):
                return title_elem.get_text(strip=True)
        
        # Fallback: get any text content
        text = element.get_text(strip=True)
        if text and len(text) < 200:  # Reasonable title length
            return text
        
        return None
    
    def _extract_description(self, element):
        """Extract description from element"""
        desc_selectors = [
            '[data-testid="campaign-description"]',
            '.campaign-description',
            '.quest-description',
            '[class*="description"]',
            'p'
        ]
        
        for selector in desc_selectors:
            desc_elem = element.select_one(selector)
            if desc_elem:
                text = desc_elem.get_text(strip=True)
                if text and len(text) > 10:
                    return text
        
        return None
    
    def _extract_image(self, element):
        """Extract image URL from element"""
        img_selectors = [
            'img',
            '[data-testid="campaign-image"]',
            '.campaign-image',
            '.quest-image'
        ]
        
        for selector in img_selectors:
            img_elem = element.select_one(selector)
            if img_elem:
                src = img_elem.get('src') or img_elem.get('data-src')
                if src:
                    if src.startswith('/'):
                        return f"https://galxe.com{src}"
                    elif not src.startswith('http'):
                        return f"https://galxe.com/{src}"
                    return src
        
        return None
    
    def _extract_network(self, element):
        """Extract network information from element"""
        # Try to find network info in various selectors
        network_selectors = [
            '[data-testid="network"]',
            '.network',
            '[class*="network"]',
            '[class*="chain"]',
            '.chain'
        ]
        
        for selector in network_selectors:
            network_elem = element.select_one(selector)
            if network_elem:
                text = network_elem.get_text(strip=True)
                if text:
                    return text
        
        # Look for common network names in text
        text = element.get_text()
        networks = ['Ethereum', 'Polygon', 'Arbitrum', 'Optimism', 'BSC', 'Avalanche', 'Solana', 'Base']
        for network in networks:
            if network.lower() in text.lower():
                return network
        
        return 'Unknown'
    
    def _extract_quest_type(self, element):
        """Extract quest type information from element"""
        # Try to find quest type in various selectors
        type_selectors = [
            '[data-testid="quest-type"]',
            '.quest-type',
            '[class*="type"]',
            '.type'
        ]
        
        for selector in type_selectors:
            type_elem = element.select_one(selector)
            if type_elem:
                text = type_elem.get_text(strip=True)
                if text:
                    return text
        
        # Look for common quest types in text
        text = element.get_text()
        quest_types = ['Social', 'Quiz', 'Task', 'Campaign', 'Event', 'Challenge']
        for quest_type in quest_types:
            if quest_type.lower() in text.lower():
                return quest_type
        
        return 'Quest'
    
    def __enter__(self):
        self.setup_selenium()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_selenium() 