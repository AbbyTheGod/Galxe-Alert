import sqlite3
import logging
from datetime import datetime
from config import DATABASE_PATH

class QuestDatabase:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create quests table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS quests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        project_name TEXT NOT NULL,
                        quest_title TEXT NOT NULL,
                        quest_url TEXT UNIQUE NOT NULL,
                        quest_description TEXT,
                        quest_image TEXT,
                        quest_status TEXT DEFAULT 'active',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create projects table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS projects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        project_name TEXT UNIQUE NOT NULL,
                        project_url TEXT NOT NULL,
                        quest_url TEXT NOT NULL,
                        is_active BOOLEAN DEFAULT 1,
                        last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create notifications table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS notifications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        quest_id INTEGER,
                        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (quest_id) REFERENCES quests (id)
                    )
                ''')
                
                conn.commit()
                logging.info("Database initialized successfully")
                
        except Exception as e:
            logging.error(f"Error initializing database: {e}")
    
    def add_quest(self, project_name, quest_title, quest_url, quest_description=None, quest_image=None):
        """Add a new quest to the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO quests 
                    (project_name, quest_title, quest_url, quest_description, quest_image)
                    VALUES (?, ?, ?, ?, ?)
                ''', (project_name, quest_title, quest_url, quest_description, quest_image))
                
                conn.commit()
                return cursor.rowcount > 0  # Returns True if new quest was added
                
        except Exception as e:
            logging.error(f"Error adding quest: {e}")
            return False
    
    def quest_exists(self, quest_url):
        """Check if a quest already exists in the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM quests WHERE quest_url = ?', (quest_url,))
                return cursor.fetchone() is not None
                
        except Exception as e:
            logging.error(f"Error checking quest existence: {e}")
            return False
    
    def get_new_quests(self, project_name):
        """Get quests that haven't been notified yet"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT q.* FROM quests q
                    LEFT JOIN notifications n ON q.id = n.quest_id
                    WHERE q.project_name = ? AND n.id IS NULL
                    ORDER BY q.discovered_at DESC
                ''', (project_name,))
                
                return cursor.fetchall()
                
        except Exception as e:
            logging.error(f"Error getting new quests: {e}")
            return []
    
    def mark_quest_notified(self, quest_id):
        """Mark a quest as notified"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO notifications (quest_id)
                    VALUES (?)
                ''', (quest_id,))
                conn.commit()
                
        except Exception as e:
            logging.error(f"Error marking quest as notified: {e}")
    
    def update_project_last_checked(self, project_name):
        """Update the last checked timestamp for a project"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE projects 
                    SET last_checked = CURRENT_TIMESTAMP
                    WHERE project_name = ?
                ''', (project_name,))
                conn.commit()
                
        except Exception as e:
            logging.error(f"Error updating project last checked: {e}")
    
    def add_project(self, project_name, project_url, quest_url):
        """Add a new project to monitor"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO projects 
                    (project_name, project_url, quest_url)
                    VALUES (?, ?, ?)
                ''', (project_name, project_url, quest_url))
                conn.commit()
                
        except Exception as e:
            logging.error(f"Error adding project: {e}")
    
    def get_all_projects(self):
        """Get all active projects"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT project_name, project_url, quest_url 
                    FROM projects 
                    WHERE is_active = 1
                ''')
                return cursor.fetchall()
                
        except Exception as e:
            logging.error(f"Error getting projects: {e}")
            return [] 