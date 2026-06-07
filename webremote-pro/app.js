// Web Remote Pro - Client App

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const trackpad = document.getElementById('trackpad');
    const ipDisplay = document.getElementById('ip-display');
    const statusText = document.getElementById('status-text');
    const statusDot = document.getElementById('status-dot');
    const volumeLabel = document.getElementById('volume-label');
    const typeInput = document.getElementById('type-input');
    const btnSendText = document.getElementById('btn-send-text');

    // Display host IP
    ipDisplay.textContent = `Host: ${window.location.hostname || 'localhost'}:${window.location.port || '5000'}`;

    // Haptic Feedback Helper
    const vibrate = (ms = 15) => {
        if ('vibrate' in navigator) {
            navigator.vibrate(ms);
        }
    };

    // Tab Navigation
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            vibrate(10);
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const tabId = btn.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // API Request Wrapper
    async function sendCommand(endpoint, data = {}) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Network response not ok');
            
            // Mark online
            statusDot.className = 'status-dot online';
            statusText.textContent = 'Online';
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            statusDot.className = 'status-dot offline';
            statusText.textContent = 'Offline';
            return { status: 'error', message: error.message };
        }
    }

    // --- Trackpad Input Handling ---
    let lastX = 0;
    let lastY = 0;
    let isMoving = false;
    let touchStartTime = 0;
    let lastTapTime = 0;
    const scrollThreshold = 10; // Scroll detection start
    
    // Smooth touchpad delta scaling
    const sensitivity = 1.3;

    trackpad.addEventListener('touchstart', (e) => {
        vibrate(8);
        const touch = e.touches[0];
        lastX = touch.clientX;
        lastY = touch.clientY;
        isMoving = true;
        touchStartTime = Date.now();
        trackpad.classList.add('active');
    });

    // Request throttling variables
    let animationFrameId = null;
    let pendingX = 0;
    let pendingY = 0;

    trackpad.addEventListener('touchmove', (e) => {
        if (!isMoving) return;
        e.preventDefault();

        const touch = e.touches[0];
        const dx = (touch.clientX - lastX) * sensitivity;
        const dy = (touch.clientY - lastY) * sensitivity;

        lastX = touch.clientX;
        lastY = touch.clientY;

        // Check if touch is within scroll zone (right 15% of trackpad)
        const rect = trackpad.getBoundingClientRect();
        const touchXRelative = touch.clientX - rect.left;
        const inScrollZone = touchXRelative > (rect.width * 0.82);

        if (inScrollZone) {
            // Scroll action
            // Send scroll every few pixels
            if (Math.abs(dy) > 1) {
                // Negative is scroll down, positive is scroll up
                sendCommand('/api/mouse/scroll', { y: Math.round(-dy * 0.5) });
            }
        } else {
            // Mouse move action
            pendingX += dx;
            pendingY += dy;

            if (!animationFrameId) {
                animationFrameId = requestAnimationFrame(() => {
                    if (Math.round(pendingX) !== 0 || Math.round(pendingY) !== 0) {
                        sendCommand('/api/mouse/move', { 
                            x: Math.round(pendingX), 
                            y: Math.round(pendingY) 
                        });
                    }
                    pendingX = 0;
                    pendingY = 0;
                    animationFrameId = null;
                });
            }
        }
    }, { passive: false });

    trackpad.addEventListener('touchend', (e) => {
        isMoving = false;
        trackpad.classList.remove('active');
        
        const duration = Date.now() - touchStartTime;
        if (duration < 250) {
            // It's a tap!
            const now = Date.now();
            if (now - lastTapTime < 250) {
                // Double tap
                vibrate(25);
                sendCommand('/api/mouse/click', { button: 'left' });
                setTimeout(() => sendCommand('/api/mouse/click', { button: 'left' }), 50);
            } else {
                // Single tap
                vibrate(15);
                sendCommand('/api/mouse/click', { button: 'left' });
            }
            lastTapTime = now;
        }
    });

    // Mouse buttons
    document.getElementById('btn-left-click').addEventListener('click', () => {
        vibrate(12);
        sendCommand('/api/mouse/click', { button: 'left' });
    });
    document.getElementById('btn-middle-click').addEventListener('click', () => {
        vibrate(12);
        sendCommand('/api/mouse/click', { button: 'middle' });
    });
    document.getElementById('btn-right-click').addEventListener('click', () => {
        vibrate(12);
        sendCommand('/api/mouse/click', { button: 'right' });
    });


    // --- Media Controls ---
    const mediaActions = {
        'btn-vol-down': 'volume_down',
        'btn-vol-up': 'volume_up',
        'btn-mute': 'mute',
        'btn-prev': 'prev',
        'btn-next': 'next',
        'btn-play-pause': 'play_pause'
    };

    Object.entries(mediaActions).forEach(([btnId, action]) => {
        document.getElementById(btnId).addEventListener('click', () => {
            vibrate(15);
            sendCommand('/api/media/control', { action });
            if (action.startsWith('volume') || action === 'mute') {
                setTimeout(updateStatus, 300);
            }
        });
    });

    // --- Keyboard Controls ---
    const keys = {
        'btn-key-esc': 'esc',
        'btn-key-tab': 'tab',
        'btn-key-super': 'super',
        'btn-key-space': 'space',
        'btn-key-backspace': 'backspace',
        'btn-key-enter': 'enter',
        'btn-key-up': 'up',
        'btn-key-down': 'down',
        'btn-key-left': 'left',
        'btn-key-right': 'right'
    };

    Object.entries(keys).forEach(([btnId, key]) => {
        document.getElementById(btnId).addEventListener('click', () => {
            vibrate(12);
            sendCommand('/api/keyboard/key', { key });
        });
    });

    // Text typing
    btnSendText.addEventListener('click', () => {
        const text = typeInput.value;
        if (text) {
            vibrate(20);
            sendCommand('/api/keyboard/type', { text });
            typeInput.value = '';
        }
    });

    typeInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            btnSendText.click();
        }
    });

    // --- System Controls ---
    document.getElementById('btn-sys-lock').addEventListener('click', () => {
        vibrate(25);
        sendCommand('/api/system/control', { action: 'lock' });
    });

    document.getElementById('btn-sys-suspend').addEventListener('click', () => {
        vibrate(30);
        if (confirm('Suspend System?')) {
            sendCommand('/api/system/control', { action: 'suspend' });
        }
    });

    document.getElementById('btn-sys-reboot').addEventListener('click', () => {
        vibrate(35);
        if (confirm('Reboot System?')) {
            sendCommand('/api/system/control', { action: 'reboot' });
        }
    });

    document.getElementById('btn-sys-poweroff').addEventListener('click', () => {
        vibrate(40);
        if (confirm('Shut down System?')) {
            sendCommand('/api/system/control', { action: 'poweroff' });
        }
    });

    // --- Periodic Status Updates ---
    async function updateStatus() {
        try {
            const res = await sendCommand('/api/status');
            if (res && res.volume) {
                // Format nicely
                let vol = res.volume.replace('Volume:', '').trim();
                volumeLabel.textContent = `Volume: ${vol}`;
                
                // Mute state detection
                const muteBtn = document.getElementById('btn-mute');
                if (vol.toLowerCase().includes('mute')) {
                    muteBtn.classList.add('active');
                } else {
                    muteBtn.classList.remove('active');
                }
            }
        } catch (e) {
            console.error('Failed to get status update', e);
        }
    }

    // Auto-update status every 5 seconds
    setInterval(updateStatus, 5000);
    updateStatus();
});
