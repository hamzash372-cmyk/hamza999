// ===== JavaScript لموقع الوسائط المتعددة =====

// وضع ليلي/نهاري
let darkMode = false;

function toggleDarkMode() {
    const body = document.body;
    const darkModeBtn = document.getElementById('darkModeBtn');
    
    if (!darkMode) {
        // تفعيل الوضع الليلي
        body.classList.add('dark-mode');
        darkModeBtn.innerHTML = '☀️ الوضع النهاري';
        darkMode = true;
        localStorage.setItem('darkMode', 'enabled');
    } else {
        // إلغاء الوضع الليلي
        body.classList.remove('dark-mode');
        darkModeBtn.innerHTML = '🌙 الوضع الليلي';
        darkMode = false;
        localStorage.setItem('darkMode', 'disabled');
    }
}

// تحميل تفضيل الوضع الليلي عند بدء التشغيل
function loadDarkModePreference() {
    const savedMode = localStorage.getItem('darkMode');
    const darkModeBtn = document.getElementById('darkModeBtn');
    
    if (savedMode === 'enabled') {
        document.body.classList.add('dark-mode');
        darkModeBtn.innerHTML = '☀️ الوضع النهاري';
        darkMode = true;
    }
}

// تأثيرات التنقل السلس
document.addEventListener('DOMContentLoaded', function() {
    console.log('موقع الوسائط المتعددة جاهز!');
    
    // تحميل تفضيل الوضع الليلي
    loadDarkModePreference();
    
    // تأثيرات للبطاقات عند التمرير
    const mediaCards = document.querySelectorAll('.media-card, .topic-card, .app-card, .team-card');
    
    mediaCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // تغيير لون الهيدر عند التمرير
    window.addEventListener('scroll', function() {
        const header = document.querySelector('header');
        if (window.scrollY > 100) {
            header.style.background = 'rgba(44, 62, 80, 0.95)';
            header.style.backdropFilter = 'blur(10px)';
        } else {
            header.style.background = '';
            header.style.backdropFilter = 'none';
        }
    });
    
    // تأثيرات التمرير (Fade-in)
    const fadeElements = document.querySelectorAll('.fade-in');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });
    
    fadeElements.forEach(el => observer.observe(el));
});

// تشغيل/إيقاف الفيديو
let videoPlaying = false;

function toggleVideo() {
    const videoPlaceholder = document.querySelector('.video-placeholder');
    if (!videoPlaying) {
        videoPlaceholder.innerHTML = '🎥 الفيديو يشغل الآن (ضع هنا الفيديو الحقيقي لاحقاً)';
        videoPlaceholder.style.background = 'linear-gradient(45deg, #e74c3c, #c0392b)';
        videoPlaying = true;
    } else {
        videoPlaceholder.innerHTML = '▶ مكان الفيديو التعليمي';
        videoPlaceholder.style.background = 'linear-gradient(45deg, #34495e, #2c3e50)';
        videoPlaying = false;
    }
}

// عدّاد زوار بسيط
function updateVisitorCount() {
    let count = localStorage.getItem('visitorCount') || 0;
    count = parseInt(count) + 1;
    localStorage.setItem('visitorCount', count);
    
    const visitorElement = document.getElementById('visitorCount');
    if (visitorElement) {
        visitorElement.textContent = `عدد الزوار: ${count}`;
    }
}
// إصلاح شامل للوضع الليلي
function applyDarkModeFixes() {
    if (document.body.classList.contains('dark-mode')) {
        // إصلاح جميع العناصر التي قد تكون بيضاء
        const elements = document.querySelectorAll('*');
        elements.forEach(el => {
            const bgColor = window.getComputedStyle(el).backgroundColor;
            if (bgColor === 'rgb(255, 255, 255)' || bgColor === 'rgb(248, 249, 250)') {
                el.style.backgroundColor = 'transparent';
            }
        });
    }
}

// تحديث الدالة toggleDarkMode
function toggleDarkMode() {
    const body = document.body;
    const darkModeBtn = document.getElementById('darkModeBtn');
    
    if (!darkMode) {
        body.classList.add('dark-mode');
        darkModeBtn.innerHTML = '☀️ الوضع النهاري';
        darkMode = true;
        localStorage.setItem('darkMode', 'enabled');
    } else {
        body.classList.remove('dark-mode');
        darkModeBtn.innerHTML = '🌙 الوضع الليلي';
        darkMode = false;
        localStorage.setItem('darkMode', 'disabled');
    }
    
    // تطبيق الإصلاحات بعد التبديل
    setTimeout(applyDarkModeFixes, 100);
}

// تطبيق الإصلاحات عند التحميل
document.addEventListener('DOMContentLoaded', function() {
    loadDarkModePreference();
    setTimeout(applyDarkModeFixes, 500);
});
// استدعاء وظيفة عداد الزوار عند تحميل الصفحة
updateVisitorCount();