# 📹 AHM Local Messenger - WebRTC
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

from flask_socketio import emit, join_room, leave_room
from database import Database
from config import Config
import json

class WebRTCManager:
    def __init__(self, socketio):
        self.socketio = socketio
        self.active_calls = {}
        self.db = Database(Config.DATABASE)
        
        self._register_events()
    
    def _register_events(self):
        """ثبت رویدادها"""
        
        @self.socketio.on('call_request')
        def handle_call_request(data):
            """درخواست تماس"""
            caller = data.get('caller')
            receiver = data.get('receiver')
            call_type = data.get('type', 'voice')  # voice | video
            
            call_id = f"{caller}_{receiver}_{call_type}"
            self.active_calls[call_id] = {
                'caller': caller,
                'receiver': receiver,
                'type': call_type,
                'status': 'ringing',
                'started_at': None
            }
            
            emit('incoming_call', {
                'call_id': call_id,
                'caller': caller,
                'type': call_type
            }, room=receiver)
            
            emit('call_ringing', {'call_id': call_id}, room=caller)
        
        @self.socketio.on('call_accept')
        def handle_call_accept(data):
            """قبول تماس"""
            call_id = data.get('call_id')
            if call_id in self.active_calls:
                self.active_calls[call_id]['status'] = 'active'
                caller = self.active_calls[call_id]['caller']
                receiver = self.active_calls[call_id]['receiver']
                
                join_room(call_id, caller)
                join_room(call_id, receiver)
                
                emit('call_accepted', {'call_id': call_id}, room=caller)
        
        @self.socketio.on('call_reject')
        def handle_call_reject(data):
            """رد تماس"""
            call_id = data.get('call_id')
            if call_id in self.active_calls:
                caller = self.active_calls[call_id]['caller']
                emit('call_rejected', {'call_id': call_id}, room=caller)
                del self.active_calls[call_id]
        
        @self.socketio.on('call_end')
        def handle_call_end(data):
            """پایان تماس"""
            call_id = data.get('call_id')
            if call_id in self.active_calls:
                caller = self.active_calls[call_id]['caller']
                receiver = self.active_calls[call_id]['receiver']
                
                emit('call_ended', {'call_id': call_id}, room=caller)
                emit('call_ended', {'call_id': call_id}, room=receiver)
                
                del self.active_calls[call_id]
        
        @self.socketio.on('webrtc_offer')
        def handle_offer(data):
            """ارسال Offer"""
            call_id = data.get('call_id')
            offer = data.get('offer')
            emit('webrtc_offer', {
                'call_id': call_id,
                'offer': offer
            }, room=call_id, include_self=False)
        
        @self.socketio.on('webrtc_answer')
        def handle_answer(data):
            """ارسال Answer"""
            call_id = data.get('call_id')
            answer = data.get('answer')
            emit('webrtc_answer', {
                'call_id': call_id,
                'answer': answer
            }, room=call_id, include_self=False)
        
        @self.socketio.on('webrtc_ice_candidate')
        def handle_ice_candidate(data):
            """ارسال ICE Candidate"""
            call_id = data.get('call_id')
            candidate = data.get('candidate')
            emit('webrtc_ice_candidate', {
                'call_id': call_id,
                'candidate': candidate
            }, room=call_id, include_self=False)
    
    def get_active_calls(self):
        """گرفتن تماس‌های فعال"""
        return self.active_calls
    
    def get_call_stats(self):
        """آمار تماس‌ها"""
        return {
            'total': len(self.active_calls),
            'active': len([c for c in self.active_calls.values() if c['status'] == 'active']),
            'ringing': len([c for c in self.active_calls.values() if c['status'] == 'ringing'])
        }

# نمونه (بعد از ساخت socketio)
# webrtc = WebRTCManager(socketio)