# 🖼️ AHM Local Messenger - Image Optimizer
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

import os
from PIL import Image
from config import Config

class ImageOptimizer:
    def __init__(self):
        self.upload_folder = Config.UPLOAD_FOLDER
        self.thumbnail_size = (200, 200)
        self.medium_size = (800, 800)
        self.quality = 85
    
    def optimize(self, image_path: str, max_size: tuple = None) -> dict:
        """بهینه‌سازی عکس"""
        try:
            if not os.path.exists(image_path):
                return {'success': False, 'message': 'فایل پیدا نشد'}
            
            img = Image.open(image_path)
            original_size = os.path.getsize(image_path)
            
            # تبدیل به RGB اگه RGBA بود
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # تغییر اندازه
            if max_size:
                img.thumbnail(max_size, Image.LANCZOS)
            
            # ذخیره با کیفیت پایین‌تر
            img.save(image_path, 'JPEG', quality=self.quality, optimize=True)
            
            new_size = os.path.getsize(image_path)
            
            return {
                'success': True,
                'original_size': original_size,
                'new_size': new_size,
                'saved': original_size - new_size,
                'saved_percent': round((1 - new_size / original_size) * 100, 2)
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def create_thumbnail(self, image_path: str) -> str:
        """ساخت thumbnail"""
        try:
            img = Image.open(image_path)
            img.thumbnail(self.thumbnail_size, Image.LANCZOS)
            
            thumb_path = image_path.replace('.', '_thumb.')
            img.save(thumb_path, 'JPEG', quality=70)
            
            return thumb_path
        except:
            return None
    
    def create_medium(self, image_path: str) -> str:
        """ساخت نسخه متوسط"""
        try:
            img = Image.open(image_path)
            img.thumbnail(self.medium_size, Image.LANCZOS)
            
            medium_path = image_path.replace('.', '_medium.')
            img.save(medium_path, 'JPEG', quality=85)
            
            return medium_path
        except:
            return None
    
    def optimize_all(self):
        """بهینه‌سازی همه عکس‌ها"""
        results = []
        
        for file_name in os.listdir(self.upload_folder):
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(self.upload_folder, file_name)
                result = self.optimize(file_path)
                results.append({
                    'file': file_name,
                    'result': result
                })
        
        return results
    
    def get_total_savings(self):
        """محاسبه صرفه‌جویی کل"""
        results = self.optimize_all()
        total_saved = sum(r['result'].get('saved', 0) for r in results if r['result']['success'])
        
        return {
            'files_optimized': len(results),
            'total_saved_bytes': total_saved,
            'total_saved_mb': round(total_saved / (1024 * 1024), 2)
        }

# نمونه
image_optimizer = ImageOptimizer()