# 📊 AHM Local Messenger - Analytics
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

from database import Database
from config import Config
from datetime import datetime, timedelta

class Analytics:
    def __init__(self):
        self.db = Database(Config.DATABASE)
    
    def get_stats(self):
        """آمار کلی"""
        stats = {}
        
        # کاربران
        self.db.cursor.execute("SELECT COUNT(*) FROM users")
        stats['total_users'] = self.db.cursor.fetchone()[0]
        
        self.db.cursor.execute("SELECT COUNT(*) FROM users WHERE is_online = 1")
        stats['online_users'] = self.db.cursor.fetchone()[0]
        
        # پیام‌ها
        self.db.cursor.execute("SELECT COUNT(*) FROM messages WHERE is_deleted = 0")
        stats['total_messages'] = self.db.cursor.fetchone()[0]
        
        # امروز
        today = datetime.now().strftime("%Y-%m-%d")
        self.db.cursor.execute(
            "SELECT COUNT(*) FROM messages WHERE DATE(created_at) = ? AND is_deleted = 0",
            (today,)
        )
        stats['today_messages'] = self.db.cursor.fetchone()[0]
        
        # گروه‌ها
        self.db.cursor.execute("SELECT COUNT(*) FROM groups")
        stats['total_groups'] = self.db.cursor.fetchone()[0]
        
        return stats
    
    def get_active_users(self, days=7):
        """کاربران فعال"""
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        self.db.cursor.execute(
            """SELECT sender, COUNT(*) as msg_count
               FROM messages
               WHERE created_at >= ? AND is_deleted = 0
               GROUP BY sender
               ORDER BY msg_count DESC
               LIMIT 10""",
            (since,)
        )
        
        return [{
            'username': row[0],
            'messages': row[1]
        } for row in self.db.cursor.fetchall()]
    
    def get_message_chart(self, days=7):
        """نمودار پیام‌ها"""
        chart = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            self.db.cursor.execute(
                "SELECT COUNT(*) FROM messages WHERE DATE(created_at) = ? AND is_deleted = 0",
                (date,)
            )
            count = self.db.cursor.fetchone()[0]
            chart.append({'date': date, 'count': count})
        
        return list(reversed(chart))
    
    def get_top_groups(self, limit=5):
        """گروه‌های برتر"""
        self.db.cursor.execute(
            """SELECT g.name, COUNT(m.id) as msg_count
               FROM groups g
               LEFT JOIN messages m ON g.id = m.group_id
               GROUP BY g.id
               ORDER BY msg_count DESC
               LIMIT ?""",
            (limit,)
        )
        
        return [{
            'name': row[0],
            'messages': row[1]
        } for row in self.db.cursor.fetchall()]

# نمونه
analytics = Analytics()