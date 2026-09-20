# ⚡ AHM Local Messenger - Database Optimizer
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

import sqlite3
from database import Database
from config import Config

class DatabaseOptimizer:
    def __init__(self):
        self.db = Database(Config.DATABASE)
    
    def create_indexes(self):
        """ساخت ایندکس‌ها برای سرعت"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender)",
            "CREATE INDEX IF NOT EXISTS idx_messages_receiver ON messages(receiver)",
            "CREATE INDEX IF NOT EXISTS idx_messages_group ON messages(group_id)",
            "CREATE INDEX IF NOT EXISTS idx_messages_created ON messages(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_messages_type ON messages(message_type)",
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
            "CREATE INDEX IF NOT EXISTS idx_users_online ON users(is_online)",
            "CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(username)",
            "CREATE INDEX IF NOT EXISTS idx_group_members_group ON group_members(group_id)",
            "CREATE INDEX IF NOT EXISTS idx_group_members_user ON group_members(username)",
        ]
        
        for idx in indexes:
            self.db.cursor.execute(idx)
        
        self.db.conn.commit()
        return len(indexes)
    
    def analyze_tables(self):
        """تحلیل جدول‌ها"""
        self.db.cursor.execute("ANALYZE")
        self.db.conn.commit()
        return True
    
    def optimize_all(self):
        """بهینه‌سازی کامل"""
        results = {}
        
        results['indexes_created'] = self.create_indexes()
        results['analyzed'] = self.analyze_tables()
        results['vacuum'] = self.db.cursor.execute("VACUUM") or True
        self.db.conn.commit()
        
        return results

# نمونه
db_optimizer = DatabaseOptimizer()