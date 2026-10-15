# AHM_Local_Messenger
# 🚀 AHM Local Messenger

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Status](https://img.shields.io/badge/status-active-success)

**پیام‌رسان محلی نسل جدید - امن، سریع، هوشمند**
**Next-Generation Local Messenger - Secure, Fast, Smart**

ساخته شده توسط: **امیرحسین حاجی مرادخانی** 👦
Created by: **AmirHossein Haji Moradkhani** 👦

</div>

---

## 🎯 AHM Local Messenger چیه؟ | What is AHM Local Messenger?

**فارسی:**
یه **پیام‌رسان محلی (Local Messenger)** که روی **شبکه داخلی** کار می‌کنه و نیازی به اینترنت نداره! یعنی می‌تونی با دوستات توی مدرسه، خونه یا هر جای دیگه که به **یه وای‌فای** وصلین، بدون اینترنت پیام بفرستی!

**English:**
A **Local Messenger** that works on **Local Area Networks (LAN)** without needing internet! This means you can chat with your friends at school, home, or anywhere connected to the **same Wi-Fi** — no internet required!

---

## ✨ امکانات فوق‌العاده | Amazing Features

### 💬 پیام‌رسانی | Messaging
- ✅ **چت متنی** بی‌درنگ (Real-time) | **Real-time Text Chat**
- ✅ **ارسال فایل** و تصاویر | **File & Image Sharing**
- ✅ **تماس صوتی/تصویری** (WebRTC) | **Voice/Video Calls (WebRTC)**
- ✅ **تبدیل ویس به متن** | **Voice-to-Text Transcriber**
- ✅ **اعلان‌ها** | **Notifications**

### 🔐 امنیت | Security
- ✅ **رمزنگاری** پیام‌ها | **Message Encryption**
- ✅ **احراز هویت** کاربران | **User Authentication**
- ✅ **پروفایل کاربری** با آواتار | **User Profile with Avatar**

### 📊 مدیریت | Management
- ✅ **داشبورد کاربری** | **User Dashboard**
- ✅ **تنظیمات پیشرفته** | **Advanced Settings**
- ✅ **جستجوی هوشمند** | **Smart Search Engine**
- ✅ **آنالیتیکس** | **Analytics**

### 💾 دیتابیس | Database
- ✅ **دیتابیس SQLite** | **SQLite Database**
- ✅ **پشتیبان‌گیری خودکار** | **Auto Backup**
- ✅ **فشرده‌سازی دیتابیس** | **DB Compressor**
- ✅ **بهینه‌سازی خودکار** | **Auto Optimizer**

### 🖼️ بهینه‌سازی | Optimization
- ✅ **فشرده‌سازی تصاویر** | **Image Optimizer**
- ✅ **مدیریت فایل‌ها** | **File Manager**

---

## 🛠️ تکنولوژی‌های استفاده شده | Technologies Used

### Backend
- 🐍 **Python** — زبان اصلی | Main Language
- 🌐 **WebSocket** — ارتباط Real-time | Real-time Communication
- 🗄️ **SQLite** — دیتابیس | Database
- 🔐 **Encryption** — رمزنگاری | Encryption

### Frontend
- 📄 **HTML5** — ساختار | Structure
- 🎨 **CSS3** — طراحی | Styling
- ⚡ **JavaScript** — تعامل | Interaction
- 🔌 **WebRTC** — تماس صوتی/تصویری | Voice/Video Calls

---

## 📦 نصب و راه‌اندازی | Installation & Setup

### پیش‌نیازها | Prerequisites
- 🐍 **Python 3.8+**
- 💻 **ویندوز، لینوکس یا مک** | **Windows, Linux or macOS**

### مراحل نصب | Installation Steps

**۱. کلون کردن پروژه | 1. Clone the Project:**
```bash
git clone https://github.com/amirhossin1395/AHM_Local_Messenger.git
cd AHM_Local_Messenger

۲. نصب کتابخانه‌های مورد نیاز | 2. Install Requirements:
pip install -r requirements.txt

۳. اجرای سرور | 3. Run the Server:
python run.py

۴. باز کردن مرورگر | 4. Open Your Browser:
http://localhost:8000

###
📁 ساختار پروژه | Project Structure
AHM_Local_Messenger/
├── 📄 api.py              # API اصلی | Main API
├── 🔐 encryption.py       # رمزنگاری | Encryption
├── 🗄️ database.py        # مدیریت دیتابیس | Database Management
├── 💬 chat.html           # صفحه چت | Chat Page
├── 👤 profile.js          # پروفایل کاربری | User Profile
├── ⚙️ settings.js         # تنظیمات | Settings
├── 🎨 style.css           # استایل | Styling
├── 📊 analytics.py        # تحلیل داده‌ها | Analytics
├── 🎙️ voice_transcriber.py # تبدیل ویس به متن | Voice-to-Text
├── 🔌 webrtc.py           # تماس صوتی/تصویری | Voice/Video Calls
├── 🌐 websocket_server.py # سرور WebSocket | WebSocket Server
├── 💾 backup.py           # پشتیبان‌گیری | Backup
├── 🗜️ db_compressor.py   # فشرده‌سازی دیتابیس | DB Compressor
├── ⚡ db_optimizer.py     # بهینه‌سازی | Optimizer
├── 🖼️ image_optimizer.py  # بهینه‌سازی تصاویر | Image Optimizer
├── 📁 file_manager.py     # مدیریت فایل | File Manager
├── 🔍 search_engine.py    # موتور جستجو | Search Engine
├── 🔔 notifications.py    # اعلان‌ها | Notifications
├── 🚀 run.py              # اجرای برنامه | Run Script
├── 🖥️ server.py           # سرور اصلی | Main Server
└── 📋 requirements.txt    # کتابخانه‌ها | Requirements
🎮 چطوری ازش استفاده کنم؟ | How to Use?
فارسی:

برای کاربران عادی:

🖥️ سرور رو اجرا کن (روی یه کامپیوتر)
📱 بقیه با گوشی یا لپ‌تاپ به همون وای‌فای وصل شن
🌐 آدرس سرور رو توی مرورگر بزنن
💬 شروع به چت کنن!
برای توسعه‌دهنده‌ها:

📖 مستندات توی هر فایل کامنت‌گذاری شده
🔧 قابل توسعه با پایتون و جاوااسکریپت
🎨 قابل شخصی‌سازی کامل
English:

For Regular Users:

🖥️ Run the server (on one computer)
📱 Connect others via phone/laptop to the same Wi-Fi
🌐 Enter the server address in the browser
💬 Start chatting!
For Developers:

📖 Documented code in every file
🔧 Extendable with Python & JavaScript
🎨 Fully customizable
🤝 مشارکت | Contributing

فارسی:
اگه دوست داری کمک کنی:

🍴 Fork کن
🌿 Branch جدید بساز
✍️ تغییرات رو اعمال کن
📤 Pull Request بفرست
English:
If you'd like to contribute:

🍴 Fork the repo
🌿 Create a new branch
✍️ Make your changes
📤 Send a Pull Request
📊 آمار پروژه | Project Stats

⭐ ستاره‌ها | Stars: 1
🍴 فورک‌ها | Forks: 0
👁️ بازدید | Views: -
📅 آخرین آپدیت | Last Update: September 2026
📜 لایسنس | License

فارسی:
این پروژه تحت لایسنس MIT منتشر شده. یعنی می‌تونی:

✅ استفاده تجاری کنی
✅ تغییرش بدی
✅ توزیعش کنی
✅ خصوصی نگه داری
English:
This project is licensed under the MIT License. You can:

✅ Use commercially
✅ Modify it
✅ Distribute it
✅ Keep it private
👨‍💻 سازنده | Creator

<div align="center">
امیرحسین حاجی مرادخانی 🇮🇷
AmirHossein Haji Moradkhani 🇮🇷

🌟 نابغه ۹ ساله کرمانی 🌟
🌟 9-Year-Old Genius from Kerman 🌟

📧 ایمیل | Email: amirhosseinhajimoradkhani@gmail.com

🔗 گیت‌هاب | GitHub: @amirhossin1395

📢 کانال ایتا | Eitaa Channel: دنیای دیجیتال

</div>
🌟 حمایت | Support

فارسی:
اگه این پروژه بهت کمک کرد:

⭐ ستاره بده
🍴 فورک کن
📢 به دوستات معرفی کن
English:
If this project helped you:

⭐ Star it
🍴 Fork it
📢 Share it with friends
<div align="center">
ساخته شده با ❤️ در کرمان، ایران 🇮🇷
Made with ❤️ in Kerman, Iran 🇮🇷

© 2026 - AHM Local Messenger

</div> ```
