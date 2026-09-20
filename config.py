# ⚙️ AHM Local Messenger - Config
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

import os

class Config:
    # سرور
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    
    # دیتابیس
    DATABASE = 'ahm_messenger.db'
    
    # امنیت
    SECRET_KEY = os.environ.get('SECRET_KEY', 'AHM_LOCAL_MESSENGER_2026_SECRET_KEY')
    PASSWORD_HASH = 'sha256'
    
    # فایل‌ها
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB
    ALLOWED_EXTENSIONS = {
        'image': {'png', 'jpg', 'jpeg', 'gif', 'webp'},
        'audio': {'mp3', 'wav', 'ogg', 'm4a', 'aac'},
        'video': {'mp4', 'webm', 'avi'},
        'file': {'pdf', 'doc', 'docx', 'txt', 'zip', 'rar'}
    }
    
    # پیام‌ها
    MAX_MESSAGE_LENGTH = 5000
    MESSAGES_PER_PAGE = 50
    
    # کاربر
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20
    MIN_PASSWORD_LENGTH = 4
    
    # ظاهر
    DEFAULT_THEME = 'light'
    DEFAULT_LANGUAGE = 'fa'
    
    # اطلاعات پروژه
    PROJECT_NAME = 'AHM Local Messenger'
    PROJECT_VERSION = '1.0.0'
    PROJECT_COPYRIGHT = 'C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)'
    PROJECT_LICENSE = 'MIT'

    # 🔐 امنیت
ENCRYPTION_ENABLED = True
JWT_SECRET = 'AHM_JWT_SECRET_2026'
JWT_EXPIRE_HOURS = 24
RATE_LIMIT_PER_MINUTE = 60

# 📹 WebRTC
WEBRTC_ENABLED = True
STUN_SERVER = 'stun:stun.l.google.com:19302'
TURN_SERVER = ''

# 🎤 تبدیل ویس
VOICE_TRANSCRIBE_ENABLED = True
VOICE_LANGUAGE = 'fa-IR'

# 🖼️ عکس
IMAGE_OPTIMIZE_ENABLED = True
IMAGE_MAX_SIZE = (1920, 1920)
IMAGE_QUALITY = 85
THUMBNAIL_SIZE = (200, 200)

# 🗜️ فشرده‌سازی
COMPRESSION_ENABLED = True
COMPRESSION_LEVEL = 9
COMPRESS_AFTER_DAYS = 7

# 📊 کش
CACHE_ENABLED = True
CACHE_TTL = 300  # 5 دقیقه