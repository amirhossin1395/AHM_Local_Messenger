# 🔍 AHM Local Messenger - Search Engine
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

from database import Database
from config import Config
import re

class SearchEngine:
    def __init__(self):
        self.db = Database(Config.DATABASE)
    
    def search(self, query, username, filters=None):
        """جستجوی پیشرفته"""
        results = {
            'messages': [],
            'users': [],
            'files': []
        }
        
        # جستجوی پیام‌ها
        if not filters or 'messages' in filters:
            results['messages'] = self._search_messages(query, username)
        
        # جستجوی کاربران
        if not filters or 'users' in filters:
            results['users'] = self._search_users(query)
        
        return results
    
    def _search_messages(self, query, username):
        """جستجوی پیام‌ها"""
        self.db.cursor.execute(
            """SELECT m.id, m.sender, m.message, m.created_at, u.display_name
               FROM messages m
               LEFT JOIN users u ON m.sender = u.username
               WHERE m.message LIKE ? 
               AND m.is_deleted = 0
               AND (m.sender = ? OR m.receiver = ? OR m.receiver IS NULL)
               ORDER BY m.created_at DESC
               LIMIT 50""",
            (f"%{query}%", username, username)
        )
        
        return [{
            'id': row[0],
            'sender': row[1],
            'message': self._highlight(row[2], query),
            'created_at': row[3],
            'display_name': row[4]
        } for row in self.db.cursor.fetchall()]
    
    def _search_users(self, query):
        """جستجوی کاربران"""
        self.db.cursor.execute(
            """SELECT username, display_name, avatar, is_online
               FROM users
               WHERE username LIKE ? OR display_name LIKE ?
               LIMIT 20""",
            (f"%{query}%", f"%{query}%")
        )
        
        return [{
            'username': row[0],
            'display_name': row[1],
            'avatar': row[2],
            'is_online': row[3]
        } for row in self.db.cursor.fetchall()]
    
    def _highlight(self, text, query):
        """هایلایت کلمه جستجو شده"""
        if not query or not text:
            return text
        
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        return pattern.sub(f"<mark>{query}</mark>", text)
    
    def get_suggestions(self, query, limit=5):
        """پیشنهاد جستجو"""
        self.db.cursor.execute(
            """SELECT DISTINCT message FROM messages
               WHERE message LIKE ? AND is_deleted = 0
               LIMIT ?""",
            (f"%{query}%", limit)
        )
        
        return [row[0] for row in self.db.cursor.fetchall()]
    
    def search_by_date(self, username, start_date, end_date):
        """جستجو بر اساس تاریخ"""
        self.db.cursor.execute(
            """SELECT id, sender, message, created_at
               FROM messages
               WHERE created_at BETWEEN ? AND ?
               AND (sender = ? OR receiver = ?)
               ORDER BY created_at DESC""",
            (start_date, end_date, username, username)
        )
        
        return [{
            'id': row[0],
            'sender': row[1],
            'message': row[2],
            'created_at': row[3]
        } for row in self.db.cursor.fetchall()]
    
    def search_by_sender(self, sender, username):
        """جستجو بر اساس فرستنده"""
        self.db.cursor.execute(
            """SELECT id, sender, message, created_at
               FROM messages
               WHERE sender = ?
               AND (receiver = ? OR receiver IS NULL)
               ORDER BY created_at DESC
               LIMIT 50""",
            (sender, username)
        )
        
        return [{
            'id': row[0],
            'sender': row[1],
            'message': row[2],
            'created_at': row[3]
        } for row in self.db.cursor.fetchall()]

# نمونه
search_engine = SearchEngine()