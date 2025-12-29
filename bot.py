import telebot
from telebot import types
import json
import os
from threading import Thread
from flask import Flask

# --- إعداد سيرفر وهمي لـ Render ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running and healthy!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# --- إعدادات البوت ---
API_TOKEN = '8275792876:AAFdv5D_XoqghqHx9fIIvevr_WNl71B_2zw'
bot = telebot.TeleBot(API_TOKEN)
ADMIN_IDS = [1015861625]
FILES_JSON = "files.json"
USERS_JSON = "users.json" # أضفنا هذا الملف لحفظ المشتركين

# ================= هيكلية البيانات (الحقوق والإعلام) =================
DATA = {
    "كلية الحقوق": {
        "السنة الأولى": {
            "فصل الخريف": ["عقوبات 1", "القانون الدولي العام", "مبادئ علم الاقتصاد", "القانون الدستوري", "المنهجية القانونية", "مدخل إلى علم القانون", "قيادة الحاسوب", "التعليم الإلكتروني"],
            "فصل الربيع": ["حريات عامة وحقوق إنسان", "عقوبات 2", "مبادئ الشريعة الإسلامية", "المدخل إلى علم السياسة", "مقدمة إلى علم القانون الإنكليزي 1", "القانون المدني 1"]
        },
        "السنة الثانية": {
            "فصل الخريف": ["عقوبات 3", "القانون التجاري 1", "القانون الإداري 1", "قانون الأحوال الشخصية 1", "القانون الدولي الاقتصادي", "القانون المدني 2"],
            "فصل الربيع": ["عقوبات 4", "القانون التجاري 2", "التشريع التعاوني", "القانون الجنائي الإنكليزي 2", "القانون المدني 3", "القانون الإداري 2"]
        },
        "السنة الثالثة": {
            "فصل الخريف": ["أصول المحاكمات المدنية 1", "المالية العامة 1", "القانون التجاري 3", "القانون المدني 4", "قانون الأحوال الشخصية 2", "القانون الإداري 3"],
            "فصل الربيع": ["أصول المحاكمات المدنية 2", "القانون الدولي الخاص 1", "القانون الدولي العام 3", "القانون المدني 5", "أصول المحاكمات الجزائية 1", "القانون التجاري 4"]
        },
        "السنة الرابعة": {
            "فصل الخريف": ["القانون الدولي الخاص 2", "أصول التنفيذ", "قانون التجارة الدولية", "القانون المدني 6", "أصول المحاكمات الجزائية 2", "التحكيم"],
            "فصل الربيع": ["المالية العامة 2", "قانون العمل", "أصول الفقه"],
            "مجموعات الاختصاص": {
                "المجموعة A (تجاري)": ["التأمين", "المصارف", "الإفلاس", "التجارة الإلكترونية"],
                "المجموعة B (مدني)": ["قانون العلاقات الزرااسية", "حقوق الملكية", "قانون حماية المستهلك", "علم الاجتماع القانوني"],
                "المجموعة C (عام)": ["التشريع البيئي", "العقود الإدارية", "الرقابة المالية", "قانون الإدارة المحلية"],
                "المجموعة D (دولي)": ["العلاقات الدبلوماسية", "القانون الدولي الإنساني", "المنظمات الدولية", "القانون الدولي للبحار"],
                "المجموعة E (جزائي)": ["قانون المخدرات", "قانون الأحداث الجانحين", "قانون غسل الأموال", "جرائم المعلوماتية"]
            }
        }
    },
    "كلية الإعلام": {
        "السنة الأولى": {
            "فصل الخريف": ["مقدمة في الإعلام", "لغة عربية", "ثقافة عامة"],
            "فصل الربيع": ["تكنولوجيا الإعلام", "لغة إنجليزية", "مهارات الاتصال"]
        }
    }
}

# ================= إدارة الملفات والمستخدمين =================
admin_upload_state = {} 

def load_json(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return default
    return default

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_user(user_id):
    users = load_json(USERS_JSON, [])
    if user_id not in users:
        users.append(user_id)
        save_json(USERS_JSON, users)

# ================= دوال القوائم (نفس منطق كودك) =================
def main_menu_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for college in DATA.keys(): markup.add(types.KeyboardButton(college))
    return markup

def years_menu_markup(college):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for year in DATA[college].keys(): markup.add(types.KeyboardButton(f"{college} - {year}"))
    markup.add(types.KeyboardButton("🏠 القائمة الرئيسية"))
    return markup

def semester_menu_markup(college, year):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for sem in DATA[college][year].keys(): markup.add(types.KeyboardButton(f"{college} | {year} | {sem}"))
    markup.add(types.KeyboardButton("🏠 القائمة الرئيسية"))
    return markup

def subjects_menu_markup(college, year, semester):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    subjects = DATA[college][year][semester]
    files = load_json(FILES_JSON, {})
    if isinstance(subjects, dict):
        for group in subjects.keys(): markup.add(types.KeyboardButton(f"{college} || {year} || {semester} || {group}"))
    else:
        for sub in subjects:
            prefix = "✅ " if files.get(sub) else "📝 "
            markup.add(types.KeyboardButton(f"{prefix}{sub}"))
    markup.add(types.KeyboardButton("🏠 القائمة الرئيسية"))
    return markup

def group_subjects_menu_markup(college, year, semester, group):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    subjects = DATA[college][year][semester][group]
    files = load_json(FILES_JSON, {})
    for sub in subjects:
        prefix = "✅ " if files.get(sub) else "📝 "
        markup.add(types.KeyboardButton(f"{prefix}{sub}"))
    markup.add(types.KeyboardButton("🏠 القائمة الرئيسية"))
    return markup

# ================= معالجة الرسائل =================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.chat.id) # حفظ المستخدم للإرسال الجماعي
    bot.send_message(message.chat.id, "📚 *أهلاً بك في مكتبة الشام الافتراضية*\n\nاختر الكلية:", 
                     reply_markup=main_menu_markup(), parse_mode="Markdown")

# --- ميزة الإرسال الجماعي (الجديدة) ---
@bot.message_handler(commands=['broadcast'])
def ask_broadcast(message):
    if message.from_user.id in ADMIN_IDS:
        msg = bot.send_message(message.chat.id, "📢 أرسل الآن الرسالة التي ستصل لجميع المستخدمين:")
        bot.register_next_step_handler(msg, start_broadcast)

def start_broadcast(message):
    users = load_json(USERS_JSON, [])
    count = 0
    bot.send_message(message.chat.id, f"🚀 جاري الإرسال لـ {len(users)} مشترك...")
    for user_id in users:
        try:
            bot.copy_message(user_id, message.chat.id, message.message_id)
            count += 1
        except: continue
    bot.send_message(message.chat.id, f"✅ تم الإرسال لـ {count} مستخدم.")

# --- بقية المنطق الخاص بك كما هو ---
@bot.message_handler(func=lambda m: m.text in DATA.keys())
def handle_college(m):
    bot.send_message(m.chat.id, f"🏛 {m.text}\nاختر السنة:", reply_markup=years_menu_markup(m.text))

@bot.message_handler(func=lambda m: " - " in m.text and " | " not in m.text)
def handle_year(m):
    try:
        col, yr = m.text.split(" - ")
        bot.send_message(m.chat.id, f"📅 {yr}\nاختر الفصل:", reply_markup=semester_menu_markup(col, yr))
    except: pass

@bot.message_handler(func=lambda m: " | " in m.text and " || " not in m.text)
def handle_semester(m):
    try:
        p = m.text.split(" | ")
        bot.send_message(m.chat.id, "📖 اختر المادة:", reply_markup=subjects_menu_markup(p[0], p[1], p[2]))
    except: pass

@bot.message_handler(func=lambda m: " || " in m.text)
def handle_group(m):
    try:
        p = m.text.split(" || ")
        bot.send_message(m.chat.id, f"📂 {p[3]}", reply_markup=group_subjects_menu_markup(p[0], p[1], p[2], p[3]))
    except: pass

@bot.message_handler(func=lambda m: m.text.startswith(("✅ ", "📝 ")))
def handle_subject(m):
    sub = m.text[2:]
    files = load_json(FILES_JSON, {})
    file_id = files.get(sub)
    if m.from_user.id in ADMIN_IDS:
        markup = types.InlineKeyboardMarkup()
        if file_id: markup.add(types.InlineKeyboardButton("📥 تجربة", callback_data=f"dl_{sub}"))
        markup.add(types.InlineKeyboardButton("📤 رفع/تغيير", callback_data=f"up_{sub}"))
        bot.reply_to(m, f"👨‍✈️ إدارة: {sub}", reply_markup=markup)
    else:
        if file_id: bot.send_document(m.chat.id, file_id, caption=f"📚 {sub}")
        else: bot.reply_to(m, "⏳ غير متوفر حالياً.")

@bot.callback_query_handler(func=lambda call: True)
def admin_callbacks(call):
    if call.data.startswith("dl_"):
        bot.send_document(call.message.chat.id, load_json(FILES_JSON, {}).get(call.data[3:]))
    elif call.data.startswith("up_"):
        sub = call.data[3:]
        admin_upload_state[call.from_user.id] = sub
        bot.send_message(call.message.chat.id, f"📤 أرسل ملف مادة: {sub}")

@bot.message_handler(content_types=['document'])
def save_doc(m):
    if m.from_user.id in ADMIN_IDS and m.from_user.id in admin_upload_state:
        sub = admin_upload_state[m.from_user.id]
        files = load_json(FILES_JSON, {})
        files[sub] = m.document.file_id
        save_json(FILES_JSON, files)
        del admin_upload_state[m.from_user.id]
        bot.reply_to(m, f"✅ تم الحفظ لـ: {sub}")

@bot.message_handler(func=lambda m: m.text == "🏠 القائمة الرئيسية" or m.text == "🔙 رجوع")
def go_home(m): send_welcome(m)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
