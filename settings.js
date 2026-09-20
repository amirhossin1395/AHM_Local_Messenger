// ⚙️ AHM Local Messenger - Settings JavaScript
// © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

const API_URL = 'http://' + window.location.hostname + ':5000/api';
let currentUser = null;

// ==================== شروع ====================

function initSettings() {
    const username = localStorage.getItem('username');
    if (!username) {
        window.location.href = '/';
        return;
    }

    currentUser = { username };

    // بارگذاری تنظیمات ذخیره شده
    loadSettings();
}

function loadSettings() {
    // حالت شب
    const darkMode = localStorage.getItem('theme') === 'dark';
    document.getElementById('dark-mode').checked = darkMode;
    if (darkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
    }

    // رنگ تم
    const themeColor = localStorage.getItem('theme_color') || '#2AABEE';
    document.getElementById('theme-color').value = themeColor;
    document.documentElement.style.setProperty('--tg-blue', themeColor);

    // اندازه فونت
    const fontSize = localStorage.getItem('font_size') || '16';
    document.getElementById('font-size').value = fontSize;
    document.documentElement.style.fontSize = fontSize + 'px';

    // اعلان‌ها
    document.getElementById('sound-notif').checked = localStorage.getItem('sound_notif') !== 'false';
    document.getElementById('vibration').checked = localStorage.getItem('vibration') !== 'false';

    // حریم خصوصی
    document.getElementById('show-online').checked = localStorage.getItem('show_online') !== 'false';
    document.getElementById('read-receipt').checked = localStorage.getItem('read_receipt') !== 'false';
}

// ==================== ظاهر ====================

function toggleDarkMode() {
    const isDark = document.getElementById('dark-mode').checked;
    if (isDark) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
    }
}

function changeThemeColor() {
    const color = document.getElementById('theme-color').value;
    document.documentElement.style.setProperty('--tg-blue', color);
    localStorage.setItem('theme_color', color);
}

function changeFontSize() {
    const size = document.getElementById('font-size').value;
    document.documentElement.style.fontSize = size + 'px';
    localStorage.setItem('font_size', size);
}

// ==================== اعلان‌ها ====================

function toggleSound() {
    localStorage.setItem('sound_notif', document.getElementById('sound-notif').checked);
}

function toggleVibration() {
    localStorage.setItem('vibration', document.getElementById('vibration').checked);
}

// ==================== حساب ====================

async function changePassword() {
    const oldPass = prompt('رمز فعلی رو وارد کن:');
    if (!oldPass) return;

    const newPass = prompt('رمز جدید رو وارد کن:');
    if (!newPass) return;

    const confirmPass = prompt('رمز جدید رو دوباره وارد کن:');
    if (newPass !== confirmPass) {
        alert('❌ رمزهای جدید یکسان نیستن!');
        return;
    }

    const res = await fetch(`${API_URL}/change-password`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            username: currentUser.username,
            old_password: oldPass,
            new_password: newPass
        })
    });

    const data = await res.json();
    alert(data.message);
}

async function deleteAccount() {
    if (!confirm('⚠️ مطمئنی می‌خوای حساب کاربریت رو حذف کنی؟')) return;
    if (!confirm('⚠️ این کار قابل بازگشت نیست!')) return;

    await fetch(`${API_URL}/users/${currentUser.username}`, {
        method: 'DELETE'
    });

    localStorage.clear();
    window.location.href = '/';
}

// ==================== داده‌ها ====================

async function exportData() {
    const res = await fetch(`${API_URL}/messages?username=${currentUser.username}`);
    const messages = await res.json();

    const data = {
        username: currentUser.username,
        messages: messages,
        exported_at: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ahm_data_${currentUser.username}_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
}

function clearCache() {
    if (!confirm('🗑️ مطمئنی می‌خوای کش رو پاک کنی؟')) return;
    localStorage.removeItem('cache');
    alert('✅ کش پاک شد!');
}

// ==================== ناوبری ====================

function goBack() {
    window.location.href = '/chat';
}

// ==================== شروع ====================

if (window.location.pathname.includes('settings')) {
    initSettings();
}