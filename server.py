# 🚀 AHM Local Messenger - Server (Updated)
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

from flask import Flask, send_from_directory
from flask_cors import CORS
from api import api
from websocket_server import socketio
from config import Config
import os

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = Config.SECRET_KEY
CORS(app)

# ثبت API
app.register_blueprint(api)

# راه‌اندازی SocketIO
socketio.init_app(app)

# ==================== فایل‌های استاتیک ====================

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat')
def chat():
    return send_from_directory('.', 'chat.html')

@app.route('/profile')
def profile():
    return send_from_directory('.', 'user_profile.html')

@app.route('/settings')
def settings():
    return send_from_directory('.', 'user_settings.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'user_dashboard.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)
# اضافه شده: ماژول‌های جدید
from encryption import encryption
from image_optimizer import image_optimizer
from db_compressor import db_compressor
from db_optimizer import db_optimizer
from voice_transcriber import transcriber

# اضافه شده: راه‌اندازی WebRTC
from webrtc import WebRTCManager
webrtc = WebRTCManager(socketio)

# اضافه شده: بهینه‌سازی دیتابیس در شروع
db_optimizer.optimize_all()
print("✅ دیتابیس بهینه شد!")

# اضافه شده: فشرده‌سازی خودکار (هر ۲۴ ساعت)
import threading
import time

def auto_compress():
    while True:
        time.sleep(86400)  # 24 ساعت
        try:
            results = db_compressor.full_compression()
            print(f"✅ فشرده‌سازی خودکار: {results['compressed_messages']} پیام")
        except Exception as e:
            print(f"❌ خطا در فشرده‌سازی: {e}")

threading.Thread(target=auto_compress, daemon=True).start()
# ==================== اجرا ====================

if __name__ == '__main__':
    socketio.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )