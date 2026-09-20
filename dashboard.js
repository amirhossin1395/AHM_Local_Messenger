// 📊 AHM Local Messenger - Dashboard JavaScript
// © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

const API_URL = 'http://' + window.location.hostname + ':5000/api';
let currentUser = null;

// ==================== شروع ====================

async function initDashboard() {
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

    // نمایش اطلاعات
    document.getElementById('dashboard-avatar').textContent = currentUser.avatar;
    document.getElementById('dashboard-name').textContent = currentUser.display_name;
    document.getElementById('dashboard-username').textContent = `@${currentUser.username}`;

    // بارگذاری آمار
    await loadStats();
    await loadActivity();
}

async function loadStats() {
    // پیام‌ها
    try {
        const res = await fetch(`${API_URL}/messages?username=${currentUser.username}`);
        const messages = await res.json();
        const userMessages = messages.filter(m => m.sender === currentUser.username);
        document.getElementById('dash-messages').textContent = userMessages.length;

        // فایل‌ها
        const files = messages.filter(m => m.file_url);
        document.getElementById('dash-files').textContent = files.length;
    } catch (e) {
        document.getElementById('dash-messages').textContent = '0';
    }

    // گروه‌ها
    try {
        const res = await fetch(`${API_URL}/groups?username=${currentUser.username}`);
        const groups = await res.json();
        document.getElementById('dash-groups').textContent = groups.length;
    } catch (e) {
        document.getElementById('dash-groups').textContent = '0';
    }

    // دوستان (کاربران آنلاین)
    try {
        const res = await fetch(`${API_URL}/users?exclude=${currentUser.username}`);
        const users = await res.json();
        document.getElementById('dash-friends').textContent = users.length;
    } catch (e) {
        document.getElementById('dash-friends').textContent = '0';
    }
}

async function loadActivity() {
    const res = await fetch(`${API_URL}/messages?username=${currentUser.username}`);
    const messages = await res.json();
    const list = document.getElementById('activity-list');

    const recent = messages.slice(0, 5);

    if (recent.length === 0) {
        list.innerHTML = '<p style="text-align:center;color:var(--tg-text-secondary);">فعالیتی نداری</p>';
        return;
    }

    list.innerHTML = recent.map(msg => `
        <div class="activity-item">
            <span class="activity-icon">💬</span>
            <div class="activity-info">
                <div class="activity-text">${msg.message.substring(0, 50)}...</div>
                <div class="activity-time">${new Date(msg.created_at).toLocaleString('fa-IR')}</div>
            </div>
        </div>
    `).join('');
}

// ==================== ناوبری ====================

function goBack() {
    window.location.href = '/chat';
}

function newGroup() {
    window.location.href = '/chat';
    setTimeout(() => {
        // TODO: باز کردن پنل ساخت گروه
    }, 500);
}

// ==================== شروع ====================

if (window.location.pathname.includes('dashboard')) {
    initDashboard();
}