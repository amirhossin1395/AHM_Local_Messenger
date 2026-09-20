# 🌐 AHM Local Messenger - API
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

from flask import Blueprint, request, jsonify, session, send_from_directory
from database import Database
from utils import Utils
from config import Config
import os
import base64
from datetime import datetime

# اضافه شده: ایمپورت‌های جدید
from encryption import encryption
from image_optimizer import image_optimizer
from voice_transcriber import transcriber
from db_compressor import db_compressor

api = Blueprint('api', __name__, url_prefix='/api')
db = Database(Config.DATABASE)

# ==================== احراز هویت ====================

@api.route('/register', methods=['POST'])
def register():
    data = request.json
    
    valid, msg = Utils.validate_username(data['username'])
    if not valid:
        return jsonify({"success": False, "message": msg}), 400
    
    valid, msg = Utils.validate_password(data['password'])
    if not valid:
        return jsonify({"success": False, "message": msg}), 400
    
    valid, msg = Utils.validate_display_name(data['display_name'])
    if not valid:
        return jsonify({"success": False, "message": msg}), 400
    
    success, message = db.register(
        data['username'],
        data['password'],
        data['display_name']
    )
    
    return jsonify({"success": success, "message": message})

@api.route('/login', methods=['POST'])
def login():
    data = request.json
    success, message, user = db.login(data['username'], data['password'])
    
    if success:
        session['username'] = data['username']
        session['user_id'] = user[0]
    
    return jsonify({
        "success": success,
        "message": message,
        "user": {
            "username": user[1],
            "display_name": user[3],
            "avatar": user[4],
            "bio": user[5]
        } if user else None
    })

@api.route('/logout', methods=['POST'])
def logout():
    data = request.json
    db.logout(data['username'])
    session.clear()
    return jsonify({"success": True})

# ==================== پیام‌ها ====================

@api.route('/messages', methods=['POST'])
def send_message():
    data = request.json
    
    file_url = None
    file_name = None
    message_type = data.get('message_type', 'text')
    
    if data.get('file_data'):
        try:
            file_name = f"{Utils.generate_token(8)}_{data.get('file_name', 'file')}"
            file_path = os.path.join(Config.UPLOAD_FOLDER, file_name)
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            
            file_data = data['file_data'].split(',')[1] if ',' in data['file_data'] else data['file_data']
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(file_data))
            
            file_url = f"/uploads/{file_name}"
            message_type = Utils.get_file_type(file_name)
            
            # اضافه شده: بهینه‌سازی عکس
            if message_type == 'image':
                image_optimizer.optimize(file_path)
                
        except Exception as e:
            return jsonify({"success": False, "message": f"خطا در ذخیره فایل: {str(e)}"}), 500
    
    message = data.get('message', '')
    if len(message) > Config.MAX_MESSAGE_LENGTH:
        return jsonify({"success": False, "message": "پیام خیلی طولانیه!"}), 400
    
    msg_id = db.save_message(
        sender=data['sender'],
        message=message,
        receiver=data.get('receiver'),
        group_id=data.get('group_id'),
        message_type=message_type,
        file_url=file_url,
        file_name=file_name
    )
    
    return jsonify({"success": True, "message_id": msg_id})

@api.route('/messages', methods=['GET'])
def get_messages():
    username = request.args.get('username')
    other_user = request.args.get('other_user')
    group_id = request.args.get('group_id')
    
    messages = db.get_messages(
        username,
        other_user,
        int(group_id) if group_id else None
    )
    
    return jsonify([{
        "id": m[0],
        "sender": m[1],
        "receiver": m[2],
        "group_id": m[3],
        "message": m[4],
        "message_type": m[5],
        "file_url": m[6],
        "file_name": m[7],
        "is_pinned": m[8],
        "is_edited": m[9],
        "is_deleted": m[10],
        "read_at": m[11],
        "created_at": m[12],
        "display_name": m[13] if len(m) > 13 else m[1],
        "avatar": m[14] if len(m) > 14 else '👤'
    } for m in messages])

@api.route('/messages/<int:msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    username = request.json.get('username')
    db.delete_message(msg_id, username)
    return jsonify({"success": True})

@api.route('/messages/<int:msg_id>', methods=['PUT'])
def edit_message(msg_id):
    data = request.json
    db.edit_message(msg_id, data['message'], data['username'])
    return jsonify({"success": True})

@api.route('/messages/<int:msg_id>/pin', methods=['POST'])
def pin_message(msg_id):
    db.pin_message(msg_id)
    return jsonify({"success": True})

@api.route('/messages/<int:msg_id>/read', methods=['POST'])
def mark_read(msg_id):
    db.mark_read(msg_id)
    return jsonify({"success": True})

@api.route('/messages/search', methods=['GET'])
def search_messages():
    query = request.args.get('q', '')
    username = request.args.get('username', '')
    
    if len(query) < 2:
        return jsonify([])
    
    messages = db.search_messages(query, username)
    return jsonify([{
        "id": m[0],
        "sender": m[1],
        "message": m[4],
        "created_at": m[12],
        "display_name": m[13] if len(m) > 13 else m[1]
    } for m in messages])

# اضافه شده: تبدیل ویس
@api.route('/messages/<int:msg_id>/transcribe', methods=['POST'])
def transcribe_voice(msg_id):
    """تبدیل ویس به متن"""
    result = transcriber.transcribe_message(msg_id)
    return jsonify(result)

# ==================== کاربران ====================

@api.route('/users', methods=['GET'])
def get_users():
    exclude = request.args.get('exclude')
    users = db.get_users(exclude)
    return jsonify([{
        "username": u[0],
        "display_name": u[1],
        "avatar": u[2],
        "is_online": u[3],
        "last_seen": u[4]
    } for u in users])

@api.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = db.get_user(username)
    if user:
        return jsonify({
            "username": user[0],
            "display_name": user[1],
            "avatar": user[2],
            "bio": user[3],
            "is_online": user[4],
            "last_seen": user[5]
        })
    return jsonify({"error": "کاربر پیدا نشد"}), 404

@api.route('/profile', methods=['PUT'])
def update_profile():
    data = request.json
    db.update_profile(
        data['username'],
        data.get('display_name'),
        data.get('avatar'),
        data.get('bio')
    )
    return jsonify({"success": True})

# ==================== گروه‌ها ====================

@api.route('/groups', methods=['POST'])
def create_group():
    data = request.json
    group_id = db.create_group(
        data['name'],
        data['created_by'],
        data['members']
    )
    return jsonify({"success": True, "group_id": group_id})

@api.route('/groups', methods=['GET'])
def get_groups():
    username = request.args.get('username')
    groups = db.get_groups(username)
    return jsonify([{
        "id": g[0],
        "name": g[1],
        "created_by": g[2],
        "created_at": g[3]
    } for g in groups])

@api.route('/groups/<int:group_id>/members', methods=['GET'])
def get_group_members(group_id):
    members = db.get_group_members(group_id)
    return jsonify(members)

# ==================== اعلان‌ها ====================

@api.route('/notifications/<username>', methods=['GET'])
def get_notifications(username):
    notifs = db.get_notifications(username)
    return jsonify([{
        "id": n[0],
        "title": n[2],
        "body": n[3],
        "is_read": n[4],
        "created_at": n[5]
    } for n in notifs])

# ==================== فایل‌ها ====================

@api.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)

# ==================== مدیریت ====================

# اضافه شده: فشرده‌سازی دیتابیس
@api.route('/admin/compress', methods=['POST'])
def compress_db():
    """فشرده‌سازی دیتابیس"""
    result = db_compressor.full_compression()
    return jsonify(result)

# اضافه شده: آمار دیتابیس
@api.route('/admin/db-stats', methods=['GET'])
def db_stats():
    """آمار دیتابیس"""
    return jsonify(db_compressor.analyze_database())

# اضافه شده: بهینه‌سازی عکس‌ها
@api.route('/admin/optimize-images', methods=['POST'])
def optimize_images():
    """بهینه‌سازی همه عکس‌ها"""
    result = image_optimizer.get_total_savings()
    return jsonify(result)