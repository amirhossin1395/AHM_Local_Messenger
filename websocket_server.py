# ⚡ AHM Local Messenger - WebSocket Server
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request
from database import Database
from utils import Utils
from config import Config
from datetime import datetime

socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')
db = Database(Config.DATABASE)

# ==================== اتصال ====================

@socketio.on('connect')
def handle_connect():
    """اتصال کاربر"""
    print(f"✅ کاربر متصل شد: {request.sid}")
    emit('connected', {'status': 'ok', 'sid': request.sid})

@socketio.on('disconnect')
def handle_disconnect():
    """قطع اتصال"""
    print(f"❌ کاربر قطع شد: {request.sid}")

# ==================== احراز هویت ====================

@socketio.on('auth')
def handle_auth(data):
    """احراز هویت"""
    username = data.get('username')
    if username:
        join_room(username)
        db.cursor.execute(
            "UPDATE users SET is_online = 1 WHERE username = ?",
            (username,)
        )
        db.conn.commit()
        
        # اطلاع به همه
        emit('user_online', {
            'username': username,
            'time': datetime.now().isoformat()
        }, broadcast=True)
        
        emit('auth_success', {'username': username})

# ==================== پیام‌ها ====================

@socketio.on('send_message')
def handle_send_message(data):
    """ارسال پیام Real-time"""
    sender = data.get('sender')
    message = data.get('message')
    receiver = data.get('receiver')
    group_id = data.get('group_id')
    message_type = data.get('message_type', 'text')
    file_url = data.get('file_url')
    file_name = data.get('file_name')
    
    # ذخیره توی دیتابیس
    msg_id = db.save_message(
        sender=sender,
        message=message,
        receiver=receiver,
        group_id=group_id,
        message_type=message_type,
        file_url=file_url,
        file_name=file_name
    )
    
    # اطلاعات پیام
    msg_data = {
        'id': msg_id,
        'sender': sender,
        'message': message,
        'receiver': receiver,
        'group_id': group_id,
        'message_type': message_type,
        'file_url': file_url,
        'file_name': file_name,
        'created_at': datetime.now().isoformat()
    }
    
    # ارسال به گیرنده
    if receiver:
        emit('new_message', msg_data, room=receiver)
    elif group_id:
        emit('new_message', msg_data, room=f"group_{group_id}")
    
    # ارسال به فرستنده (برای تایید)
    emit('message_sent', msg_data, room=sender)

@socketio.on('typing')
def handle_typing(data):
    """در حال تایپ"""
    sender = data.get('sender')
    receiver = data.get('receiver')
    is_typing = data.get('is_typing', False)
    
    emit('user_typing', {
        'sender': sender,
        'is_typing': is_typing
    }, room=receiver)

@socketio.on('read_message')
def handle_read_message(data):
    """علامت خوانده شدن"""
    msg_id = data.get('message_id')
    reader = data.get('reader')
    
    db.mark_read(msg_id)
    
    emit('message_read', {
        'message_id': msg_id,
        'reader': reader
    }, broadcast=True)

# ==================== گروه‌ها ====================

@socketio.on('join_group')
def handle_join_group(data):
    """عضویت در گروه"""
    group_id = data.get('group_id')
    username = data.get('username')
    
    join_room(f"group_{group_id}")
    emit('joined_group', {'group_id': group_id, 'username': username})

@socketio.on('leave_group')
def handle_leave_group(data):
    """خروج از گروه"""
    group_id = data.get('group_id')
    username = data.get('username')
    
    leave_room(f"group_{group_id}")
    emit('left_group', {'group_id': group_id, 'username': username})

# ==================== وضعیت ====================

@socketio.on('get_online_users')
def handle_get_online_users():
    """گرفتن کاربران آنلاین"""
    db.cursor.execute("SELECT username FROM users WHERE is_online = 1")
    users = [row[0] for row in db.cursor.fetchall()]
    emit('online_users', {'users': users})

@socketio.on('ping')
def handle_ping():
    """پینگ برای نگه‌داشتن اتصال"""
    emit('pong', {'time': datetime.now().isoformat()})