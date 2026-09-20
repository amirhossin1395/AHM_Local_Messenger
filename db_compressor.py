# 🗜️ AHM Local Messenger - Database Compressor
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

import sqlite3
import gzip
import zlib
import os
import base64
from datetime import datetime, timedelta
from config import Config
from database import Database

class DatabaseCompressor:
    def __init__(self):
        self.db = Database(Config.DATABASE)
        self.compression_level = 9  # حداکثر فشرده‌سازی
    
    def compress_text(self, text: str) -> str:
        """فشرده‌سازی متن"""
        if not text:
            return text
        compressed = zlib.compress(text.encode(), self.compression_level)
        return base64.b64encode(compressed).decode()
    
    def decompress_text(self, compressed: str) -> str:
        """بازکردن متن فشرده"""
        if not compressed:
            return compressed
        try:
            decompressed = zlib.decompress(base64.b64decode(compressed))
            return decompressed.decode()
        except:
            return compressed
    
    def compress_old_messages(self, days=30):
        """فشرده‌سازی پیام‌های قدیمی"""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        self.db.cursor.execute(
            """SELECT id, message FROM messages 
               WHERE created_at < ? AND message != '' AND message NOT LIKE 'COMPRESSED:%'""",
            (cutoff,)
        )
        
        messages = self.db.cursor.fetchall()
        compressed_count = 0
        
        for msg_id, message in messages:
            compressed = self.compress_text(message)
            self.db.cursor.execute(
                "UPDATE messages SET message = ? WHERE id = ?",
                (f"COMPRESSED:{compressed}", msg_id)
            )
            compressed_count += 1
        
        self.db.conn.commit()
        return compressed_count
    
    def decompress_message(self, msg_id: int) -> str:
        """بازکردن پیام فشرده"""
        self.db.cursor.execute(
            "SELECT message FROM messages WHERE id = ?",
            (msg_id,)
        )
        result = self.db.cursor.fetchone()
        
        if result and result[0].startswith('COMPRESSED:'):
            return self.decompress_text(result[0].replace('COMPRESSED:', ''))
        
        return result[0] if result else ''
    
    def vacuum_database(self):
        """فشرده‌سازی فیزیکی دیتابیس"""
        self.db.cursor.execute("VACUUM")
        self.db.conn.commit()
        return True
    
    def analyze_database(self):
        """تحلیل دیتابیس"""
        # حجم فایل
        db_size = os.path.getsize(Config.DATABASE)
        
        # تعداد رکوردها
        self.db.cursor.execute("SELECT COUNT(*) FROM messages")
        total_messages = self.db.cursor.fetchone()[0]
        
        self.db.cursor.execute("SELECT COUNT(*) FROM users")
        total_users = self.db.cursor.fetchone()[0]
        
        # حجم پیام‌ها
        self.db.cursor.execute("SELECT SUM(LENGTH(message)) FROM messages")
        total_message_size = self.db.cursor.fetchone()[0] or 0
        
        # پیام‌های فشرده
        self.db.cursor.execute(
            "SELECT COUNT(*) FROM messages WHERE message LIKE 'COMPRESSED:%'"
        )
        compressed_messages = self.db.cursor.fetchone()[0]
        
        return {
            'db_size_bytes': db_size,
            'db_size_mb': round(db_size / (1024 * 1024), 2),
            'total_messages': total_messages,
            'total_users': total_users,
            'total_message_size_kb': round(total_message_size / 1024, 2),
            'compressed_messages': compressed_messages,
            'compression_ratio': round(compressed_messages / total_messages * 100, 2) if total_messages else 0
        }
    
    def full_compression(self):
        """فشرده‌سازی کامل"""
        results = {}
        
        # ۱. فشرده‌سازی پیام‌های قدیمی
        results['compressed_messages'] = self.compress_old_messages(days=7)
        
        # ۲. VACUUM
        self.vacuum_database()
        results['vacuum'] = True
        
        # ۳. تحلیل
        results['analysis'] = self.analyze_database()
        
        return results
    
    def backup_compressed(self):
        """پشتیبان فشرده"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"db_backup_{timestamp}.db.gz"
        
        with open(Config.DATABASE, 'rb') as f_in:
            with gzip.open(backup_name, 'wb', compresslevel=9) as f_out:
                f_out.write(f_in.read())
        
        original_size = os.path.getsize(Config.DATABASE)
        compressed_size = os.path.getsize(backup_name)
        
        return {
            'backup_name': backup_name,
            'original_size_mb': round(original_size / (1024 * 1024), 2),
            'compressed_size_mb': round(compressed_size / (1024 * 1024), 2),
            'saved_percent': round((1 - compressed_size / original_size) * 100, 2)
        }

# نمونه
db_compressor = DatabaseCompressor()