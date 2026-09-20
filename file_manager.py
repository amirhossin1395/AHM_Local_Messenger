# 📁 AHM Local Messenger - File Manager
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

import os
import base64
import mimetypes
from datetime import datetime
from config import Config
from utils import Utils

class FileManager:
    def __init__(self):
        self.upload_folder = Config.UPLOAD_FOLDER
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def save_file(self, file_data, original_name):
        """ذخیره فایل"""
        try:
            # تولید نام یکتا
            file_name = f"{Utils.generate_token(8)}_{original_name}"
            file_path = os.path.join(self.upload_folder, file_name)
            
            # دیکد کردن Base64
            if ',' in file_data:
                file_data = file_data.split(',')[1]
            
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(file_data))
            
            # تشخیص نوع
            file_type = Utils.get_file_type(original_name)
            
            return {
                'success': True,
                'file_name': file_name,
                'file_url': f"/uploads/{file_name}",
                'file_type': file_type,
                'file_size': os.path.getsize(file_path)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"خطا در ذخیره فایل: {str(e)}"
            }
    
    def delete_file(self, file_name):
        """حذف فایل"""
        try:
            file_path = os.path.join(self.upload_folder, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except:
            return False
    
    def get_file_info(self, file_name):
        """گرفتن اطلاعات فایل"""
        file_path = os.path.join(self.upload_folder, file_name)
        
        if not os.path.exists(file_path):
            return None
        
        mime_type, _ = mimetypes.guess_type(file_path)
        
        return {
            'name': file_name,
            'size': os.path.getsize(file_path),
            'mime_type': mime_type or 'application/octet-stream',
            'type': Utils.get_file_type(file_name),
            'created_at': datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
        }
    
    def list_files(self, file_type=None):
        """لیست فایل‌ها"""
        files = []
        
        for file_name in os.listdir(self.upload_folder):
            file_path = os.path.join(self.upload_folder, file_name)
            
            if os.path.isfile(file_path):
                info = self.get_file_info(file_name)
                if info and (not file_type or info['type'] == file_type):
                    files.append(info)
        
        return sorted(files, key=lambda x: x['created_at'], reverse=True)
    
    def get_total_size(self):
        """حجم کل فایل‌ها"""
        total = 0
        for file_name in os.listdir(self.upload_folder):
            file_path = os.path.join(self.upload_folder, file_name)
            if os.path.isfile(file_path):
                total += os.path.getsize(file_path)
        return total
    
    def clean_old_files(self, days=30):
        """پاک کردن فایل‌های قدیمی"""
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=days)
        deleted = 0
        
        for file_name in os.listdir(self.upload_folder):
            file_path = os.path.join(self.upload_folder, file_name)
            
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if file_time < cutoff:
                    os.remove(file_path)
                    deleted += 1
        
        return deleted

# نمونه
file_manager = FileManager()