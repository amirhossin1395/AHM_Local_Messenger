# 🎤 AHM Local Messenger - Voice Transcriber
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

import os
import speech_recognition as sr
from database import Database
from config import Config

class VoiceTranscriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.db = Database(Config.DATABASE)
    
    def transcribe(self, audio_path: str, language: str = 'fa-IR') -> dict:
        """تبدیل ویس به متن"""
        try:
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
            
            # تلاش برای تبدیل
            text = self.recognizer.recognize_google(audio, language=language)
            
            return {
                'success': True,
                'text': text,
                'language': language
            }
        except sr.UnknownValueError:
            return {
                'success': False,
                'message': 'صدا قابل تشخیص نبود'
            }
        except sr.RequestError as e:
            return {
                'success': False,
                'message': f'خطا در سرویس: {e}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'خطا: {e}'
            }
    
    def transcribe_message(self, message_id: int) -> dict:
        """تبدیل ویس پیام به متن"""
        # گرفتن پیام از دیتابیس
        self.db.cursor.execute(
            "SELECT file_url FROM messages WHERE id = ?",
            (message_id,)
        )
        result = self.db.cursor.fetchone()
        
        if not result or not result[0]:
            return {'success': False, 'message': 'فایل پیدا نشد'}
        
        # مسیر فایل
        file_path = result[0].replace('/uploads/', Config.UPLOAD_FOLDER + '/')
        
        if not os.path.exists(file_path):
            return {'success': False, 'message': 'فایل وجود نداره'}
        
        # تبدیل
        result = self.transcribe(file_path)
        
        if result['success']:
            # ذخیره متن توی دیتابیس
            self.db.cursor.execute(
                "UPDATE messages SET message = ? WHERE id = ?",
                (result['text'], message_id)
            )
            self.db.conn.commit()
        
        return result
    
    def transcribe_all_voices(self):
        """تبدیل همه ویس‌ها"""
        self.db.cursor.execute(
            "SELECT id FROM messages WHERE message_type = 'voice' AND message = ''"
        )
        messages = self.db.cursor.fetchall()
        
        results = []
        for msg in messages:
            result = self.transcribe_message(msg[0])
            results.append({
                'message_id': msg[0],
                'result': result
            })
        
        return results

# نمونه
transcriber = VoiceTranscriber()