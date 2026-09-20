# 💾 AHM Local Messenger - Backup
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

import shutil
import os
import zipfile
from datetime import datetime
from config import Config

class BackupManager:
    def __init__(self):
        self.db_file = Config.DATABASE
        self.upload_folder = Config.UPLOAD_FOLDER
        self.backup_folder = 'backups'
        os.makedirs(self.backup_folder, exist_ok=True)
    
    def create_backup(self):
        """ساخت پشتیبان"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}.zip"
        backup_path = os.path.join(self.backup_folder, backup_name)
        
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # دیتابیس
            if os.path.exists(self.db_file):
                zipf.write(self.db_file, 'database.db')
            
            # فایل‌های آپلود
            if os.path.exists(self.upload_folder):
                for root, dirs, files in os.walk(self.upload_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, '.')
                        zipf.write(file_path, arcname)
        
        return {
            'success': True,
            'backup_name': backup_name,
            'backup_path': backup_path,
            'size': os.path.getsize(backup_path)
        }
    
    def restore_backup(self, backup_name):
        """بازیابی پشتیبان"""
        backup_path = os.path.join(self.backup_folder, backup_name)
        
        if not os.path.exists(backup_path):
            return {'success': False, 'message': 'فایل پشتیبان پیدا نشد'}
        
        try:
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall('.')
            
            return {'success': True, 'message': '✅ بازیابی موفق!'}
        except Exception as e:
            return {'success': False, 'message': f'خطا: {str(e)}'}
    
    def list_backups(self):
        """لیست پشتیبان‌ها"""
        backups = []
        
        for file_name in os.listdir(self.backup_folder):
            if file_name.endswith('.zip'):
                file_path = os.path.join(self.backup_folder, file_name)
                backups.append({
                    'name': file_name,
                    'size': os.path.getsize(file_path),
                    'created_at': datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
                })
        
        return sorted(backups, key=lambda x: x['created_at'], reverse=True)
    
    def delete_backup(self, backup_name):
        """حذف پشتیبان"""
        backup_path = os.path.join(self.backup_folder, backup_name)
        
        if os.path.exists(backup_path):
            os.remove(backup_path)
            return True
        return False
    
    def auto_backup(self, days=7):
        """پشتیبان خودکار"""
        backups = self.list_backups()
        
        if not backups:
            return self.create_backup()
        
        last_backup = datetime.fromisoformat(backups[0]['created_at'])
        if (datetime.now() - last_backup).days >= days:
            return self.create_backup()
        
        return None

# نمونه
backup_manager = BackupManager()