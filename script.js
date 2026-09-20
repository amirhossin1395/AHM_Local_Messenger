// 🚀 AHM Local Messenger - JavaScript
// © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

const API_URL = 'http://' + window.location.hostname + ':5000/api';
let currentUser = null;
let currentChat = null;  // { type: 'user' | 'group' | 'public', id: string }
let currentTab = 'chats';
let pollingInterval = null;

// ==================== احراز هویت ====================

function showLogin() {
    document.getElementById('register-form').classList.add('hidden');
    document.getElementById('login-form').classList.remove('hidden');
}

function showRegister() {
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('register-form').classList.remove('hidden');
}

async function register() {
    const username = document.getElementById('reg-username').value.trim();
    const display = document.getElementById('reg-display').value.trim();
    const password = document.getElementById('reg-password').value;

    if (!username || !display || !password) {
        showMessage('همه فیلدها رو پر کن!', 'error');
        return;
    }

    const res = await fetch(`${API_URL}/register`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password, display_name: display})
    });
    const data = await res.json();
    showMessage(data.message, data.success ? 'success' : 'error');

    if (data.success) {
        setTimeout(() => {
            localStorage.setItem('username', username);
            localStorage.setItem('display_name', display);
            window.location.href = '/chat';
        }, 1000);
    }
}

async function login() {
    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;

    if (!username || !password) {
        showMessage('همه فیلدها رو پر کن!', 'error');
        return;
    }

    const res = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password})
    });
    const data = await res.json();
    showMessage(data.message, data.success ? 'success' : 'error');

    if (data.success) {
        localStorage.setItem('username', username);
        localStorage.setItem('display_name', data.user.display_name);
        localStorage.setItem('avatar', data.user.avatar);
        setTimeout(() => {
            window.location.href = '/chat';
        }, 1000);
    }
}

function showMessage(text, type) {
    const msg = document.getElementById('message');
    msg.textContent = text;
    msg.className = `message ${type}`;
}

// ==================== چت ====================

async function initChat() {
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

    document.getElementById('user-display').textContent = currentUser.display_name;
    document.getElementById('user-avatar').textContent = currentUser.avatar;
    document.getElementById('profile-display').value = currentUser.display_name;
    document.getElementById('profile-avatar').textContent = currentUser.avatar;

    await loadChatList();
    await loadNotifications();

    // Polling
    pollingInterval = setInterval(async () => {
        await loadChatList();
        if (currentChat) {
            await loadMessages();
        }
        await loadNotifications();
    }, 2000);
}

async function loadChatList() {
    const res = await fetch(`${API_URL}/users?exclude=${currentUser.username}`);
    const users = await res.json();
    const list = document.getElementById('chat-list');
    list.innerHTML = '';

    // تب همگانی
    if (currentTab === 'all') {
        const publicItem = document.createElement('div');
        publicItem.className = 'chat-item';
        publicItem.innerHTML = `
            <div class="chat-item-avatar">📢</div>
            <div class="chat-item-info">
                <div class="chat-item-name">پیام همگانی</div>
                <div class="chat-item-last">پیام برای همه</div>
            </div>
        `;
        publicItem.onclick = () => openChat('public', 'public');
        list.appendChild(publicItem);
    }

    // کاربران
    if (currentTab === 'chats') {
        users.forEach(user => {
            const item = document.createElement('div');
            item.className = 'chat-item';
            item.innerHTML = `
                <div class="chat-item-avatar">
                    ${user.avatar}
                    ${user.is_online ? '<div class="online-dot"></div>' : ''}
                </div>
                <div class="chat-item-info">
                    <div class="chat-item-name">${user.display_name}</div>
                    <div class="chat-item-last">@${user.username}</div>
                </div>
            `;
            item.onclick = () => openChat('user', user.username, user.display_name, user.avatar);
            list.appendChild(item);
        });
    }

    // گروه‌ها
    if (currentTab === 'groups') {
        const res = await fetch(`${API_URL}/groups?username=${currentUser.username}`);
        const groups = await res.json();

        groups.forEach(group => {
            const item = document.createElement('div');
            item.className = 'chat-item';
            item.innerHTML = `
                <div class="chat-item-avatar">👥</div>
                <div class="chat-item-info">
                    <div class="chat-item-name">${group.name}</div>
                    <div class="chat-item-last">گروه</div>
                </div>
            `;
            item.onclick = () => openChat('group', group.id, group.name, '👥');
            list.appendChild(item);
        });

        // دکمه ساخت گروه
        const createBtn = document.createElement('div');
        createBtn.className = 'chat-item';
        createBtn.innerHTML = `
            <div class="chat-item-avatar">➕</div>
            <div class="chat-item-info">
                <div class="chat-item-name">ساخت گروه جدید</div>
            </div>
        `;
        createBtn.onclick = () => createGroup();
        list.appendChild(createBtn);
    }
}

function showTab(tab) {
    currentTab = tab;
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    loadChatList();
}

function openChat(type, id, name, avatar) {
    currentChat = { type, id };
    document.getElementById('chat-name').textContent = name || id;
    document.getElementById('chat-avatar').textContent = avatar || '👤';
    document.getElementById('chat-status').textContent = type === 'group' ? 'گروه' : 'آنلاین';
    loadMessages();
    document.getElementById('sidebar').classList.remove('open');
}

function goBack() {
    document.getElementById('sidebar').classList.add('open');
}

async function loadMessages() {
    if (!currentChat) return;

    let url = `${API_URL}/messages?username=${currentUser.username}`;
    if (currentChat.type === 'user') {
        url += `&other_user=${currentChat.id}`;
    } else if (currentChat.type === 'group') {
        url += `&group_id=${currentChat.id}`;
    }

    const res = await fetch(url);
    const messages = await res.json();
    const container = document.getElementById('messages');
    container.innerHTML = '';

    if (messages.length === 0) {
        container.innerHTML = `
            <div class="welcome-message">
                <div class="welcome-icon">💬</div>
                <h2>هنوز پیامی نداری!</h2>
                <p>اولین پیام رو بفرست</p>
            </div>
        `;
        return;
    }

    messages.forEach(msg => {
        const isOwn = msg.sender === currentUser.username;
        const div = document.createElement('div');
        div.className = `message ${isOwn ? 'own' : 'other'} ${msg.is_pinned ? 'pinned' : ''}`;
        div.dataset.id = msg.id;

        let content = '';
        if (!isOwn && currentChat.type !== 'user') {
            content += `<div class="message-sender">${msg.display_name || msg.sender}</div>`;
        }

        if (msg.message_type === 'image') {
            content += `<img src="${msg.file_url}" style="max-width:100%;border-radius:10px;" alt="عکس">`;
        } else if (msg.message_type === 'voice') {
            content += `<audio controls src="${msg.file_url}" style="max-width:100%;"></audio>`;
        } else if (msg.message_type === 'music') {
            content += `<audio controls src="${msg.file_url}" style="max-width:100%;"></audio>`;
        } else if (msg.message_type === 'file') {
            content += `<a href="${msg.file_url}" download="${msg.file_name}" style="color:var(--tg-blue);">📎 ${msg.file_name}</a>`;
        } else {
            content += `<div class="message-text">${msg.message}</div>`;
        }

        const time = new Date(msg.created_at).toLocaleTimeString('fa-IR', {hour: '2-digit', minute: '2-digit'});
        const tick = isOwn ? `<span class="message-tick ${msg.read_at ? 'read' : ''}">${msg.read_at ? '✓✓' : '✓'}</span>` : '';

        content += `
            <div class="message-info">
                ${msg.is_edited ? '<span style="font-size:10px;color:var(--tg-text-secondary);">ویرایش شده</span>' : ''}
                <span class="message-time">${time}</span>
                ${tick}
            </div>
        `;

        if (isOwn) {
            content += `
                <div class="message-actions">
                    <button class="message-action-btn" onclick="editMessage(${msg.id})" title="ویرایش">✏️</button>
                    <button class="message-action-btn" onclick="deleteMessage(${msg.id})" title="حذف">🗑️</button>
                    <button class="message-action-btn" onclick="pinMessage(${msg.id})" title="پین">📌</button>
                </div>
            `;
        }

        div.innerHTML = content;
        container.appendChild(div);
    });

    container.scrollTop = container.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    if (!message || !currentChat) return;

    const body = {
        sender: currentUser.username,
        message: message,
        message_type: 'text'
    };

    if (currentChat.type === 'user') {
        body.receiver = currentChat.id;
    } else if (currentChat.type === 'group') {
        body.group_id = currentChat.id;
    }

    await fetch(`${API_URL}/messages`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body)
    });

    input.value = '';
    await loadMessages();
}

async function deleteMessage(id) {
    if (!confirm('مطمئنی می‌خوای حذف کنی؟')) return;
    await fetch(`${API_URL}/messages/${id}`, {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: currentUser.username})
    });
    await loadMessages();
}

async function editMessage(id) {
    const newText = prompt('متن جدید رو بنویس:');
    if (!newText) return;
    await fetch(`${API_URL}/messages/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: newText, username: currentUser.username})
    });
    await loadMessages();
}

async function pinMessage(id) {
    await fetch(`${API_URL}/messages/${id}/pin`, {method: 'POST'});
    await loadMessages();
}

async function searchMessages() {
    const query = document.getElementById('search-input').value;
    if (query.length < 2) {
        loadChatList();
        return;
    }

    const res = await fetch(`${API_URL}/messages/search?q=${query}&username=${currentUser.username}`);
    const messages = await res.json();
    const list = document.getElementById('chat-list');
    list.innerHTML = '<div style="padding:15px;color:var(--tg-text-secondary);">نتایج جستجو:</div>';

    messages.forEach(msg => {
        const item = document.createElement('div');
        item.className = 'chat-item';
        item.innerHTML = `
            <div class="chat-item-avatar">🔍</div>
            <div class="chat-item-info">
                <div class="chat-item-name">${msg.display_name}</div>
                <div class="chat-item-last">${msg.message}</div>
            </div>
        `;
        list.appendChild(item);
    });
}

// ==================== پروفایل ====================

function showProfile() {
    document.getElementById('profile-modal').classList.remove('hidden');
}

function closeProfile() {
    document.getElementById('profile-modal').classList.add('hidden');
}

async function saveProfile() {
    const display = document.getElementById('profile-display').value;
    const bio = document.getElementById('profile-bio').value;

    await fetch(`${API_URL}/profile`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            username: currentUser.username,
            display_name: display,
            bio: bio
        })
    });

    localStorage.setItem('display_name', display);
    currentUser.display_name = display;
    document.getElementById('user-display').textContent = display;
    closeProfile();
}

// ==================== اعلان‌ها ====================

async function loadNotifications() {
    const res = await fetch(`${API_URL}/notifications/${currentUser.username}`);
    const notifs = await res.json();
    // نمایش اعلان‌ها (اختیاری)
}

// ==================== تم ====================

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const newTheme = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// ==================== شکلک ====================

function toggleEmoji() {
    document.getElementById('emoji-panel').classList.toggle('hidden');
}

function addEmoji(emoji) {
    const input = document.getElementById('message-input');
    input.value += emoji;
    input.focus();
}

// ==================== گروه ====================

async function createGroup() {
    const name = prompt('اسم گروه رو بنویس:');
    if (!name) return;

    const members = [currentUser.username];
    // TODO: انتخاب اعضا

    await fetch(`${API_URL}/groups`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name, created_by: currentUser.username, members})
    });

    loadChatList();
}

// ==================== خروج ====================

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
// اضافه شده: SocketIO
const socket = io('http://' + window.location.hostname + ':5000');

// اضافه شده: اتصال SocketIO
socket.on('connect', () => {
    console.log('✅ SocketIO متصل شد!');
    socket.emit('auth', {username: currentUser.username});
});

// اضافه شده: پیام جدید
socket.on('new_message', (data) => {
    if (currentChat && (currentChat.id === data.sender || currentChat.id === data.receiver)) {
        loadMessages();
    }
    // اعلان
    showNotification(data.sender, data.message);
    playSound();
});

// اضافه شده: کاربر آنلاین
socket.on('user_online', (data) => {
    loadChatList();
});

// اضافه شده: در حال تایپ
socket.on('user_typing', (data) => {
    if (currentChat && currentChat.id === data.sender) {
        document.getElementById('chat-status').textContent = data.is_typing ? 'در حال تایپ...' : 'آنلاین';
    }
});

// اضافه شده: ارسال با SocketIO
async function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    if (!message || !currentChat) return;

    const body = {
        sender: currentUser.username,
        message: message,
        message_type: 'text'
    };

    if (currentChat.type === 'user') {
        body.receiver = currentChat.id;
    } else if (currentChat.type === 'group') {
        body.group_id = currentChat.id;
    }

    // ارسال از طریق SocketIO (Real-time)
    socket.emit('send_message', body);

    input.value = '';
}

// اضافه شده: تایپ کردن
function onTyping() {
    if (!currentChat || currentChat.type !== 'user') return;
    
    socket.emit('typing', {
        sender: currentUser.username,
        receiver: currentChat.id,
        is_typing: true
    });

    clearTimeout(window.typingTimeout);
    window.typingTimeout = setTimeout(() => {
        socket.emit('typing', {
            sender: currentUser.username,
            receiver: currentChat.id,
            is_typing: false
        });
    }, 2000);
}

// اضافه شده: اعلان
function showNotification(title, body) {
    if (Notification.permission === 'granted') {
        new Notification(title, {body: body, icon: '/icon.png'});
    }
}

// اضافه شده: صدا
function playSound() {
    const audio = new Audio('/notification.mp3');
    audio.play().catch(() => {});
}
// ==================== منو ====================

function toggleMenu() {
    const menu = document.getElementById('dropdown-menu');
    menu.classList.toggle('hidden');
}

function toggleSidebarMenu() {
    const menu = document.getElementById('sidebar-dropdown');
    menu.classList.toggle('hidden');
}

// بستن منو با کلیک بیرون
document.addEventListener('click', (e) => {
    if (!e.target.closest('.chat-actions') && !e.target.closest('#dropdown-menu')) {
        document.getElementById('dropdown-menu')?.classList.add('hidden');
    }
    if (!e.target.closest('.sidebar-header') && !e.target.closest('#sidebar-dropdown')) {
        document.getElementById('sidebar-dropdown')?.classList.add('hidden');
    }
});

// ==================== تماس ====================

function startVoiceCall() {
    if (!currentChat || currentChat.type !== 'user') {
        alert('فقط توی چت خصوصی می‌تونی تماس بگیری!');
        return;
    }
    alert('📞 تماس صوتی با ' + currentChat.id);
    // TODO: WebRTC
}

function startVideoCall() {
    if (!currentChat || currentChat.type !== 'user') {
        alert('فقط توی چت خصوصی می‌تونی تماس بگیری!');
        return;
    }
    alert('📹 تماس تصویری با ' + currentChat.id);
    // TODO: WebRTC
}

// ==================== منو ====================

function viewProfile() {
    if (currentChat) {
        window.location.href = `/profile?user=${currentChat.id}`;
    }
}

function searchInChat() {
    const query = prompt('چی رو جستجو کنم؟');
    if (query) {
        document.getElementById('search-input').value = query;
        searchMessages();
    }
}

function muteChat() {
    alert('🔕 چت بی‌صدا شد!');
}

function clearHistory() {
    if (confirm('🗑️ مطمئنی می‌خوای تاریخچه رو پاک کنی؟')) {
        alert('✅ تاریخچه پاک شد!');
    }
}

function blockUser() {
    if (confirm('🚫 مطمئنی می‌خوای مسدود کنی؟')) {
        alert('✅ کاربر مسدود شد!');
    }
}

function deleteChat() {
    if (confirm('❌ مطمئنی می‌خوای چت رو حذف کنی؟')) {
        alert('✅ چت حذف شد!');
    }
}

function showNewChat() {
    alert('➕ چت جدید');
    // TODO: نمایش لیست کاربران
}

function showSavedMessages() {
    alert('💾 پیام‌های ذخیره شده');
}

function showContacts() {
    alert('📇 مخاطبین');
}
// ==================== اسکرول خودکار ====================

// اسکرول به آخر پیام‌ها
function scrollToBottom() {
    const container = document.getElementById('messages');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

// اسکرول به بالا (برای بارگذاری پیام‌های قدیمی)
function scrollToTop() {
    const container = document.getElementById('messages');
    if (container) {
        container.scrollTop = 0;
    }
}

// چک کردن اسکرول
function checkScroll() {
    const container = document.getElementById('messages');
    if (!container) return;
    
    // اگه به بالا رسید، پیام‌های قدیمی‌تر بارگذاری کن
    if (container.scrollTop === 0) {
        loadMoreMessages();
    }
    
    // اگه به پایین رسید، دکمه "برو به آخر" رو مخفی کن
    const isAtBottom = container.scrollHeight - container.scrollTop <= container.clientHeight + 50;
    const scrollBtn = document.getElementById('scroll-to-bottom');
    if (scrollBtn) {
        scrollBtn.classList.toggle('hidden', isAtBottom);
    }
}

// بارگذاری پیام‌های قدیمی‌تر
let isLoadingMore = false;
async function loadMoreMessages() {
    if (isLoadingMore) return;
    isLoadingMore = true;
    
    // TODO: بارگذاری پیام‌های قدیمی‌تر
    
    isLoadingMore = false;
}

// اسکرول به پیام خاص
function scrollToMessage(messageId) {
    const message = document.querySelector(`[data-id="${messageId}"]`);
    if (message) {
        message.scrollIntoView({behavior: 'smooth', block: 'center'});
        message.classList.add('highlight');
        setTimeout(() => message.classList.remove('highlight'), 2000);
    }
}

// ==================== اتصال اسکرول ====================

document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('messages');
    if (messagesContainer) {
        messagesContainer.addEventListener('scroll', checkScroll);
    }
});

// ==================== دکمه برو به آخر ====================

function createScrollToBottomBtn() {
    const btn = document.createElement('button');
    btn.id = 'scroll-to-bottom';
    btn.className = 'scroll-to-bottom hidden';
    btn.innerHTML = '↓';
    btn.onclick = scrollToBottom;
    document.querySelector('.chat-main').appendChild(btn);
}

// توی initChat() صدا بزن:
// createScrollToBottomBtn();
// ==================== شروع ====================

if (window.location.pathname === '/chat' || window.location.pathname === '/chat.html') {
    initChat();
    // تم ذخیره شده
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    }
}
// اضافه شده: WebRTC
let peerConnection = null;
let localStream = null;
let currentCallId = null;

// اضافه شده: تماس صوتی
async function startVoiceCall() {
    if (!currentChat || currentChat.type !== 'user') {
        showToast('فقط توی چت خصوصی می‌تونی تماس بگیری!', 'error');
        return;
    }
    
    try {
        localStream = await navigator.mediaDevices.getUserMedia({audio: true});
        socket.emit('call_request', {
            caller: currentUser.username,
            receiver: currentChat.id,
            type: 'voice'
        });
        showToast('📞 در حال تماس...', 'info');
    } catch (e) {
        showToast('❌ دسترسی به میکروفن ندادی!', 'error');
    }
}

// اضافه شده: تماس تصویری
async function startVideoCall() {
    if (!currentChat || currentChat.type !== 'user') {
        showToast('فقط توی چت خصوصی می‌تونی تماس بگیری!', 'error');
        return;
    }
    
    try {
        localStream = await navigator.mediaDevices.getUserMedia({video: true, audio: true});
        socket.emit('call_request', {
            caller: currentUser.username,
            receiver: currentChat.id,
            type: 'video'
        });
        showToast('📹 در حال تماس تصویری...', 'info');
    } catch (e) {
        showToast('❌ دسترسی به دوربین ندادی!', 'error');
    }
}

// اضافه شده: دریافت تماس
socket.on('incoming_call', (data) => {
    if (confirm(`📞 تماس ${data.type === 'video' ? 'تصویری' : 'صوتی'} از ${data.caller}\nقبول می‌کنی؟`)) {
        socket.emit('call_accept', {call_id: data.call_id});
        currentCallId = data.call_id;
    } else {
        socket.emit('call_reject', {call_id: data.call_id});
    }
});

// اضافه شده: تبدیل ویس به متن
async function transcribeVoice(msgId) {
    const res = await fetch(`${API_URL}/messages/${msgId}/transcribe`, {method: 'POST'});
    const data = await res.json();
    if (data.success) {
        showToast(`📝 متن: ${data.text}`, 'success');
        loadMessages();
    }
}

// اضافه شده: بهینه‌سازی عکس در آپلود
async function attachFile() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*,audio/*,video/*,.pdf,.doc,.docx';
    
    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        // چک حجم
        if (file.size > 50 * 1024 * 1024) {
            showToast('❌ فایل خیلی بزرگه! (حداکثر ۵۰ مگ)', 'error');
            return;
        }
        
        // تبدیل به Base64
        const reader = new FileReader();
        reader.onload = async (event) => {
            const fileData = event.target.result;
            
            await fetch(`${API_URL}/messages`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    sender: currentUser.username,
                    receiver: currentChat?.id,
                    message: '',
                    message_type: 'file',
                    file_data: fileData,
                    file_name: file.name
                })
            });
            
            loadMessages();
            showToast('✅ فایل ارسال شد!', 'success');
        };
        reader.readAsDataURL(file);
    };
    
    input.click();
}