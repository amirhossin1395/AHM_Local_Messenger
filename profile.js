// 👤 AHM Local Messenger - Profile JavaScript
// © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

const API_URL = 'http://' + window.location.hostname + ':5000/api';
let currentUser = null;
let selectedAvatar = '👤';

// ==================== شروع ====================

async function initProfile() {
    const username = localStorage.getItem('username');
    if (!username) {
        window.location.href = '/';
        return;
    }

    currentUser = {
        username,
        display_name: localStorage.getItem('display_name') || username,
        avatar: localStorage.getItem('avatar') || '👤'
    };

    // بارگذاری اطلاعات
    await loadProfile();
    await loadStats();

    // تم
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.getElementById('theme-toggle').checked = true;
    }
}

// ==================== پروفایل ====================

async function loadProfile() {
    const res = await fetch(`${API_URL}/users/${currentUser.username}`);
    const user = await res.json();

    document.getElementById('profile-display').value = user.display_name || '';
    document.getElementById('profile-username').value = user.username || '';
    document.getElementById('profile-bio').value = user.bio || '';
    document.getElementById('avatar-display').textContent = user.avatar || '👤';
    
    selectedAvatar = user.avatar || '👤';
}

async function saveProfile() {
    const display = document.getElementById('profile-display').value;
    const bio = document.getElementById('profile-bio').value;

    const res = await fetch(`${API_URL}/profile`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            username: currentUser.username,
            display_name: display,
            avatar: selectedAvatar,
            bio: bio
        })
    });

    const data = await res.json();
    if (data.success) {
        localStorage.setItem('display_name', display);
        localStorage.setItem('avatar', selectedAvatar);
        showToast('✅ پروفایل ذخیره شد!', 'success');
    } else {
        showToast('❌ خطا در ذخیره!', 'error');
    }
}

// ==================== آواتار ====================

function showAvatarPicker() {
    document.getElementById('avatar-modal').classList.remove('hidden');
}

function closeAvatarPicker() {
    document.getElementById('avatar-modal').classList.add('hidden');
}

function selectAvatar(avatar) {
    selectedAvatar = avatar;
    document.getElementById('avatar-display').textContent = avatar;
    closeAvatarPicker();
}

// ==================== آمار ====================

async function loadStats() {
    try {
        const res = await fetch(`${API_URL}/messages?username=${currentUser.username}`);
        const messages = await res.json();
        
        const userMessages = messages.filter(m => m.sender === currentUser.username);
        document.getElementById('stat-messages').textContent = userMessages.length;
    } catch (e) {
        document.getElementById('stat-messages').textContent = '0';
    }

    try {
        const res = await fetch(`${API_URL}/groups?username=${currentUser.username}`);
        const groups = await res.json();
        document.getElementById('stat-groups').textContent = groups.length;
    } catch (e) {
        document.getElementById('stat-groups').textContent = '0';
    }

    document.getElementById('stat-friends').textContent = '0';
}

// ==================== تم ====================

function toggleTheme() {
    const isDark = document.getElementById('theme-toggle').checked;
    if (isDark) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
    }
}

function setThemeColor(color) {
    document.documentElement.style.setProperty('--tg-blue', color);
    localStorage.setItem('theme_color', color);
}

// ==================== خروج ====================

function goBack() {
    window.location.href = '/chat';
}

async function logout() {
    if (!confirm('مطمئنی می‌خوای خارج بشی؟')) return;
    
    await fetch(`${API_URL}/logout`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: currentUser.username})
    });
    
    localStorage.clear();
    window.location.href = '/';
}

// ==================== توست ====================

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
    }, 100);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ==================== شروع ====================

if (window.location.pathname.includes('profile')) {
    initProfile();
    // تم ذخیره شده
    const savedColor = localStorage.getItem('theme_color');
    if (savedColor) {
        document.documentElement.style.setProperty('--tg-blue', savedColor);
    }
}