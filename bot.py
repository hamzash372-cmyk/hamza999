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

# ================ DATA STRUCTURE ================
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
    }
}

# ================ وظائف النظام ================
admin_upload_state = {}

def load_files():
    if os.path.exists(FILES_JSON):
        try:
            with open(FILES_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return {}
    return {}

def save_file_id(subject_name, file_id):
    files = load_files()
    files[subject_name] = file_id
    with open(FILES_JSON, 'w', encoding='utf-8') as f:
        json.dump(files, f, ensure_ascii=False, indent=2)

# ================ القوائم ================
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for college in DATA.keys(): markup.add(types.KeyboardButton(college))
    return markup

def years_menu(college):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for year in DATA[college].keys(): markup.add(types.KeyboardButton(f"🎓 {college} - {year}"))
    markup.add(types.KeyboardButton("🏠 الرئيسية"))
    return markup

def semester_menu(college, year):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for sem in DATA[college][year].keys(): markup.add(types.KeyboardButton(f"📅 {college} | {year} | {sem}"))
    markup.add(types.KeyboardButton(f"🔙 للسنوات ({college})"))
    return markup

def subjects_menu(college, year, sem):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    files = load_files()
    items = DATA[college][year][sem]
    if isinstance(items, dict):
        for group in items.keys(): markup.add(types.KeyboardButton(f"📂 {college} || {year} || {sem} || {group}"))
    else:
        for sub in items:
            prefix = "✅ " if files.get(sub) else "📝 "
            markup.add(types.KeyboardButton(f"{prefix}{sub}"))
    markup.add(types.KeyboardButton(f"🔙 للفصول ({college}-{year})"))
    return markup

# ================ المعالجات ================
@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "📚 أهلاً بك في مكتبة الحقوق، اختر الكلية:", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text in DATA.keys())
def college_select(m):
    bot.send_message(m.chat.id, "اختر السنة الدراسية:", reply_markup=years_menu(m.text))

@bot.message_handler(func=lambda m: m.text.startswith("🎓 "))
def year_select(m):
    clean_text = m.text.replace("🎓 ", "")
    college, year = clean_text.split(" - ")
    bot.send_message(m.chat.id, "اختر الفصل الدراسي:", reply_markup=semester_menu(college, year))

@bot.message_handler(func=lambda m: m.text.startswith("📅 "))
def sem_select(m):
    clean_text = m.text.replace("📅 ", "")
    college, year, sem = clean_text.split(" | ")
    bot.send_message(m.chat.id, "اختر المادة:", reply_markup=subjects_menu(college, year, sem))

@bot.message_handler(func=lambda m: m.text.startswith(("✅ ", "📝 ")))
def file_handle(m):
    sub = m.text[2:]
    file_id = load_files().get(sub)
    if m.from_user.id in ADMIN_IDS:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📤 رفع/تغيير الملف", callback_data=f"up_{sub}"))
        if file_id: markup.add(types.InlineKeyboardButton("📥 تجربة تحميل", callback_data=f"dl_{sub}"))
        bot.reply_to(m, f"إدارة مادة: {sub}", reply_markup=markup)
    else:
        if file_id: bot.send_document(m.chat.id, file_id, caption=f"📚 {sub}")
        else: bot.reply_to(m, "⏳ المادة ستتوفر قريباً.")

@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    if call.data.startswith("up_"):
        sub = call.data[3:]
        admin_upload_state[call.from_user.id] = sub
        bot.send_message(call.message.chat.id, f"قم بإرسال ملف PDF لـ: {sub}")
    elif call.data.startswith("dl_"):
        bot.send_document(call.message.chat.id, load_files().get(call.data[3:]))

@bot.message_handler(content_types=['document'])
def receive_doc(m):
    if m.from_user.id in ADMIN_IDS and m.from_user.id in admin_upload_state:
        sub = admin_upload_state[m.from_user.id]
        save_file_id(sub, m.document.file_id)
        del admin_upload_state[m.from_user.id]
        bot.reply_to(m, f"✅ تم حفظ {sub}")

# --- أزرار الرجوع الذكية ---
@bot.message_handler(func=lambda m: m.text.startswith("🔙 "))
def back_logic(m):
    if "للأسنوات" in m.text:
        college = m.text.split("(")[1].replace(")", "")
        college_select(telebot.types.Message(m.message_id, m.from_user, m.date, m.chat, m.content_type, {'text': college}, m.json))
    else:
        start(m)

@bot.message_handler(func=lambda m: m.text == "🏠 الرئيسية")
def go_home(m): start(m)

# ================ التشغيل ================
if __name__ == "__main__":
    # تشغيل Flask في خيط منفصل لـ Render
    Thread(target=run_flask).start()
    print("🚀 البوت يعمل الآن...")
    bot.infinity_polling()
