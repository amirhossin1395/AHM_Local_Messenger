# 🔔 AHM Local Messenger - Notifications
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

from database import Database
from config import Config
from datetime import datetime

class NotificationManager:
    def __init__(self):
        self.db = Database(Config.DATABASE)
    
    def send(self, username, title, body, notif_type='info'):
        """ارسال اعلان"""
        self.db.add_notification(username, title, body)
        
        # TODO: ارسال از طریق WebSocket
        
        return True
    
    def send_message_notification(self, sender, receiver, message):
        """اعلان پیام جدید"""
        title = f"💬 پیام جدید از {sender}"
        body = message[:100] + "..." if len(message) > 100 else message
        return self.send(receiver, title, body, 'message')
    
    def send_group_notification(self, sender, group_name, message, members):
        """اعلان پیام گروه"""
        title = f"👥 پیام جدید در {group_name}"
        body = f"{sender}: {message[:80]}..."
        
        for member in members:
            if member != sender:
                self.send(member, title, body, 'group')
        
        return True
    
    def send_online_notification(self, username):
        """اعلان آنلاین شدن"""
        # به همه کاربران آنلاین اطلاع بده
        self.db.cursor.execute(
            "SELECT username FROM users WHERE is_online = 1 AND username != ?",
            (username,)
        )
        users = [row[0] for row in self.db.cursor.fetchall()]
        
        for user in users:
            self.send(
                user,
                f"🟢 {username} آنلاین شد",
                "برای چت کلیک کن",
                'online'
            )
        
        return True
    
    def send_system_notification(self, title, body):
        """اعلان سیستمی"""
        self.db.cursor.execute("SELECT username FROM users")
        users = [row[0] for row in self.db.cursor.fetchall()]
        
        for user in users:
            self.send(user, title, body, 'system')
        
        return True
    
    def get_unread_count(self, username):
        """تعداد اعلان‌های نخوانده"""
        self.db.cursor.execute(
            "SELECT COUNT(*) FROM notifications WHERE username = ? AND is_read = 0",
            (username,)
        )
        return self.db.cursor.fetchone()[0]
    
    def mark_all_read(self, username):
        """همه رو خوانده شده کن"""
        self.db.cursor.execute(
            "UPDATE notifications SET is_read = 1 WHERE username = ?",
            (username,)
        )
        self.db.conn.commit()
        return True

# نمونه
notifier = NotificationManager()