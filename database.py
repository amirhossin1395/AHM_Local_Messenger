# 🗄️ AHM Local Messenger - Database
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

import sqlite3
import hashlib
from datetime import datetime

class Database:
    def __init__(self, db_name="ahm_messenger.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """ساخت جدول‌ها"""
        # کاربران
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                display_name TEXT NOT NULL,
                avatar TEXT DEFAULT '👤',
                bio TEXT DEFAULT '',
                is_online INTEGER DEFAULT 0,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # پیام‌ها
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                receiver TEXT,
                group_id INTEGER,
                message TEXT NOT NULL,
                message_type TEXT DEFAULT 'text',
                file_url TEXT,
                file_name TEXT,
                is_pinned INTEGER DEFAULT 0,
                is_edited INTEGER DEFAULT 0,
                is_deleted INTEGER DEFAULT 0,
                read_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # گروه‌ها
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_by TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # اعضای گروه
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS group_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # اعلان‌ها
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
        print("✅ دیتابیس آماده شد!")
    
    def hash_password(self, password):
        """هش کردن رمز"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username, password, display_name):
        """ثبت‌نام"""
        try:
            hashed = self.hash_password(password)
            self.cursor.execute(
                "INSERT INTO users (username, password, display_name) VALUES (?, ?, ?)",
                (username, hashed, display_name)
            )
            self.conn.commit()
            return True, "✅ ثبت‌نام موفق!"
        except sqlite3.IntegrityError:
            return False, "❌ این نام کاربری قبلاً وجود داره!"
    
    def login(self, username, password):
        """ورود"""
        hashed = self.hash_password(password)
        self.cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hashed)
        )
        user = self.cursor.fetchone()
        if user:
            self.cursor.execute(
                "UPDATE users SET is_online = 1 WHERE username = ?",
                (username,)
            )
            self.conn.commit()
            return True, "✅ ورود موفق!", user
        return False, "❌ نام کاربری یا رمز اشتباهه!", None
    
    def logout(self, username):
        """خروج"""
        self.cursor.execute(
            "UPDATE users SET is_online = 0, last_seen = CURRENT_TIMESTAMP WHERE username = ?",
            (username,)
        )
        self.conn.commit()
    
    def save_message(self, sender, message, receiver=None, group_id=None, 
                     message_type='text', file_url=None, file_name=None):
        """ذخیره پیام"""
        self.cursor.execute(
            """INSERT INTO messages (sender, receiver, group_id, message, 
               message_type, file_url, file_name) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (sender, receiver, group_id, message, message_type, file_url, file_name)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_messages(self, username, other_user=None, group_id=None, limit=100):
        """گرفتن پیام‌ها"""
        if group_id:
            self.cursor.execute(
                """SELECT m.*, u.display_name, u.avatar FROM messages m
                   LEFT JOIN users u ON m.sender = u.username
                   WHERE m.group_id = ? AND m.is_deleted = 0
                   ORDER BY m.created_at ASC LIMIT ?""",
                (group_id, limit)
            )
        elif other_user:
            self.cursor.execute(
                """SELECT m.*, u.display_name, u.avatar FROM messages m
                   LEFT JOIN users u ON m.sender = u.username
                   WHERE ((m.sender = ? AND m.receiver = ?) OR (m.sender = ? AND m.receiver = ?))
                   AND m.group_id IS NULL AND m.is_deleted = 0
                   ORDER BY m.created_at ASC LIMIT ?""",
                (username, other_user, other_user, username, limit)
            )
        else:
            self.cursor.execute(
                """SELECT m.*, u.display_name, u.avatar FROM messages m
                   LEFT JOIN users u ON m.sender = u.username
                   WHERE m.is_deleted = 0
                   ORDER BY m.created_at DESC LIMIT ?""",
                (limit,)
            )
        return self.cursor.fetchall()
    
    def get_users(self, exclude=None):
        """گرفتن کاربران"""
        if exclude:
            self.cursor.execute(
                "SELECT username, display_name, avatar, is_online, last_seen FROM users WHERE username != ?",
                (exclude,)
            )
        else:
            self.cursor.execute(
                "SELECT username, display_name, avatar, is_online, last_seen FROM users"
            )
        return self.cursor.fetchall()
    
    def search_messages(self, query, username):
        """جستجوی پیام"""
        self.cursor.execute(
            """SELECT m.*, u.display_name FROM messages m
               LEFT JOIN users u ON m.sender = u.username
               WHERE m.message LIKE ? AND m.is_deleted = 0
               AND (m.receiver = ? OR m.sender = ? OR m.receiver IS NULL)
               ORDER BY m.created_at DESC LIMIT 50""",
            (f"%{query}%", username, username)
        )
        return self.cursor.fetchall()
    
    def delete_message(self, message_id, username):
        """حذف پیام"""
        self.cursor.execute(
            "UPDATE messages SET is_deleted = 1 WHERE id = ? AND sender = ?",
            (message_id, username)
        )
        self.conn.commit()
    
    def edit_message(self, message_id, new_text, username):
        """ویرایش پیام"""
        self.cursor.execute(
            "UPDATE messages SET message = ?, is_edited = 1 WHERE id = ? AND sender = ?",
            (new_text, message_id, username)
        )
        self.conn.commit()
    
    def pin_message(self, message_id):
        """پین پیام"""
        self.cursor.execute(
            "UPDATE messages SET is_pinned = 1 WHERE id = ?",
            (message_id,)
        )
        self.conn.commit()
    
    def mark_read(self, message_id):
        """تیک خوانده شدن"""
        self.cursor.execute(
            "UPDATE messages SET read_at = CURRENT_TIMESTAMP WHERE id = ?",
            (message_id,)
        )
        self.conn.commit()
    
    def create_group(self, name, created_by, members):
        """ساخت گروه"""
        self.cursor.execute(
            "INSERT INTO groups (name, created_by) VALUES (?, ?)",
            (name, created_by)
        )
        group_id = self.cursor.lastrowid
        
        for member in members:
            self.cursor.execute(
                "INSERT INTO group_members (group_id, username) VALUES (?, ?)",
                (group_id, member)
            )
        
        self.conn.commit()
        return group_id
    
    def get_groups(self, username):
        """گرفتن گروه‌های کاربر"""
        self.cursor.execute(
            """SELECT g.* FROM groups g
               INNER JOIN group_members gm ON g.id = gm.group_id
               WHERE gm.username = ?""",
            (username,)
        )
        return self.cursor.fetchall()
    
    def get_group_members(self, group_id):
        """گرفتن اعضای گروه"""
        self.cursor.execute(
            "SELECT username FROM group_members WHERE group_id = ?",
            (group_id,)
        )
        return [row[0] for row in self.cursor.fetchall()]
    
    def update_profile(self, username, display_name=None, avatar=None, bio=None):
        """به‌روزرسانی پروفایل"""
        if display_name:
            self.cursor.execute(
                "UPDATE users SET display_name = ? WHERE username = ?",
                (display_name, username)
            )
        if avatar:
            self.cursor.execute(
                "UPDATE users SET avatar = ? WHERE username = ?",
                (avatar, username)
            )
        if bio:
            self.cursor.execute(
                "UPDATE users SET bio = ? WHERE username = ?",
                (bio, username)
            )
        self.conn.commit()
    
    def get_user(self, username):
        """گرفتن اطلاعات کاربر"""
        self.cursor.execute(
            "SELECT username, display_name, avatar, bio, is_online, last_seen FROM users WHERE username = ?",
            (username,)
        )
        return self.cursor.fetchone()
    
    def add_notification(self, username, title, body):
        """اضافه کردن اعلان"""
        self.cursor.execute(
            "INSERT INTO notifications (username, title, body) VALUES (?, ?, ?)",
            (username, title, body)
        )
        self.conn.commit()
    
    def get_notifications(self, username):
        """گرفتن اعلان‌ها"""
        self.cursor.execute(
            "SELECT * FROM notifications WHERE username = ? ORDER BY created_at DESC",
            (username,)
        )
        return self.cursor.fetchall()
# اضافه شده: رمزنگاری پیام‌ها
from encryption import encryption

# توی save_message:
def save_message(self, sender, message, receiver=None, group_id=None, 
                 message_type='text', file_url=None, file_name=None):
    """ذخیره پیام (با رمزنگاری)"""
    # رمزنگاری پیام
    if Config.ENCRYPTION_ENABLED and message:
        encrypted_message = encryption.encrypt(message)
    else:
        encrypted_message = message
    
    self.cursor.execute(
        """INSERT INTO messages (sender, receiver, group_id, message, 
           message_type, file_url, file_name) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (sender, receiver, group_id, encrypted_message, message_type, file_url, file_name)
    )
    self.conn.commit()
    return self.cursor.lastrowid

# توی get_messages:
def get_messages(self, username, other_user=None, group_id=None, limit=100):
    """گرفتن پیام‌ها (با رمزگشایی)"""
    # ... کوئری ...
    messages = self.cursor.fetchall()
    
    # رمزگشایی
    decrypted = []
    for m in messages:
        msg = list(m)
        if Config.ENCRYPTION_ENABLED and msg[4]:
            msg[4] = encryption.decrypt(msg[4])
        decrypted.append(tuple(msg))
    
    return decrypted
# تست
if __name__ == "__main__":
    db = Database()
    print("✅ دیتابیس آماده شد!")