# 🛠️ AHM Local Messenger - Utils
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

import hashlib
import secrets
import re
from datetime import datetime, timedelta
from config import Config

class Utils:
    @staticmethod
    def hash_password(password: str) -> str:
        """هش کردن رمز عبور با SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """تولید توکن تصادفی"""
        return secrets.token_hex(length)
    
    @staticmethod
    def validate_username(username: str) -> tuple:
        """اعتبارسنجی نام کاربری"""
        if len(username) < Config.MIN_USERNAME_LENGTH:
            return False, f"نام کاربری باید حداقل {Config.MIN_USERNAME_LENGTH} کاراکتر باشه"
        if len(username) > Config.MAX_USERNAME_LENGTH:
            return False, f"نام کاربری باید حداکثر {Config.MAX_USERNAME_LENGTH} کاراکتر باشه"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "نام کاربری فقط می‌تونه شامل حروف انگلیسی، عدد و _ باشه"
        return True, "✅ نام کاربری معتبره"
    
    @staticmethod
    def validate_password(password: str) -> tuple:
        """اعتبارسنجی رمز عبور"""
        if len(password) < Config.MIN_PASSWORD_LENGTH:
            return False, f"رمز عبور باید حداقل {Config.MIN_PASSWORD_LENGTH} کاراکتر باشه"
        return True, "✅ رمز عبور معتبره"
    
    @staticmethod
    def validate_display_name(name: str) -> tuple:
        """اعتبارسنجی نام نمایشی"""
        if len(name) < 2:
            return False, "نام نمایشی باید حداقل ۲ کاراکتر باشه"
        if len(name) > 50:
            return False, "نام نمایشی باید حداکثر ۵۰ کاراکتر باشه"
        return True, "✅ نام نمایشی معتبره"
    
    @staticmethod
    def format_time(dt) -> str:
        """فرمت کردن زمان"""
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        
        now = datetime.now()
        diff = now - dt
        
        if diff < timedelta(minutes=1):
            return "همین الان"
        elif diff < timedelta(hours=1):
            return f"{int(diff.total_seconds() / 60)} دقیقه پیش"
        elif diff < timedelta(days=1):
            return dt.strftime("%H:%M")
        elif diff < timedelta(days=7):
            return dt.strftime("%A %H:%M")
        else:
            return dt.strftime("%Y/%m/%d")
    
    @staticmethod
    def get_file_type(filename: str) -> str:
        """تشخیص نوع فایل"""
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        
        for file_type, extensions in Config.ALLOWED_EXTENSIONS.items():
            if ext in extensions:
                return file_type
        
        return 'file'
    
    @staticmethod
    def is_allowed_file(filename: str) -> bool:
        """چک کردن مجاز بودن فایل"""
        if '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[-1].lower()
        
        for extensions in Config.ALLOWED_EXTENSIONS.values():
            if ext in extensions:
                return True
        
        return False
    
    @staticmethod
    def generate_avatar(username: str) -> str:
        """تولید آواتار پیش‌فرض"""
        avatars = ['👤', '😎', '🚀', '🌌', '⭐', '🔥', '💪', '🎮', '🎨', '🎵']
        index = sum(ord(c) for c in username) % len(avatars)
        return avatars[index]
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 50) -> str:
        """کوتاه کردن متن"""
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."
    
    @staticmethod
    def escape_html(text: str) -> str:
        """فرار از HTML"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))
    
    @staticmethod
    def get_initials(name: str) -> str:
        """گرفتن حروف اول"""
        parts = name.split()
        if len(parts) >= 2:
            return parts[0][0] + parts[1][0]
        return name[:2].upper()