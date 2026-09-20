# 🚀 AHM Local Messenger - Run
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

from flask import Flask, send_from_directory
from flask_cors import CORS
from api import api
from config import Config
import os
import socket

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = Config.SECRET_KEY
CORS(app)

# ثبت API
app.register_blueprint(api)

# ==================== فایل‌های استاتیک ====================

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat')
def chat():
    return send_from_directory('.', 'chat.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# ==================== اجرا ====================

def get_local_ip():
    """گرفتن IP محلی"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == '__main__':
    local_ip = get_local_ip()
    
    print("=" * 60)
    print(f"🚀 {Config.PROJECT_NAME}")
    print(f"© {Config.PROJECT_COPYRIGHT}")
    print(f"📦 نسخه: {Config.PROJECT_VERSION}")
    print(f"📜 لایسنس: {Config.PROJECT_LICENSE}")
    print("=" * 60)
    print(f"✅ سرور روی http://localhost:{Config.PORT} فعال شد!")
    print(f"📡 برای دسترسی از گوشی: http://{local_ip}:{Config.PORT}")
    print("=" * 60)
    print("⛔ برای خروج: Ctrl + C")
    print("=" * 60)
    
    # ساخت پوشه uploads
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )