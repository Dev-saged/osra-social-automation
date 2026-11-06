import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            last_interaction TIMESTAMP,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            post_text TEXT,
            post_image TEXT,
            post_video TEXT,
            last_interaction TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS smart_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            response_text TEXT NOT NULL,
            usage_count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def update_interaction(platform, action):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO interactions (platform, last_interaction, likes, comments)
        VALUES (?, datetime('now'), COALESCE(likes, 0) + 1, COALESCE(comments, 0) + 1)
    ''', (platform,))
    conn.commit()
    conn.close()

def get_last_interaction(platform):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('SELECT last_interaction FROM interactions WHERE platform = ?', (platform,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
