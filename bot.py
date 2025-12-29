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

# ضع معرفك (ID) هنا لتكون أنت الوحيد القادر على الرفع
ADMIN_IDS = [1015861625]

# ملف تخزين معرفات الملفات
FILES_JSON = "files.json"

# ================= هيكلية البيانات (كما هي) =================
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

# ================= إدارة الملفات والحالة =================
# متغير مؤقت لتخزين حالة الأدمن (أي مادة يريد رفعها حالياً)
admin_upload_state = {} 

def load_files():
    if os.path.exists(FILES_JSON):
        try:
            with open(FILES_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_file_id(subject_name, file_id):
    files = load_files()
    files[subject_name] = file_id
    with open(FILES_JSON, 'w', encoding='utf-8') as f:
        json.dump(files, f, ensure_ascii=False, indent=2)

def get_file_id(subject_name):
    files = load_files()
    return files.get(subject_name)

# ================= دوال القوائم (تسهل الرجوع) =================

def main_menu_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for college in DATA.keys():
        markup.add(types.KeyboardButton(college))
    return markup

def years_menu_markup(college):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for year in DATA[college].keys():
        markup.add(types.KeyboardButton(f"{college} - {year}"))
    markup.add(types.KeyboardButton("🏠 القائمة الرئيسية"))
    return markup

def semester_menu_markup(college, year):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for semester in DATA[college][year].keys():
        markup.add(types.KeyboardButton(f"{college} | {year} | {semester}"))
    markup.add(types.KeyboardButton("🔙 رجوع"), types.KeyboardButton("🏠 القائمة الرئيسية"))
    return markup

def subjects_menu_markup(college, year, semester):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    subjects = DATA[college][year][semester]
    
    if isinstance(subjects, dict): # للمجموعات
        for group in subjects.keys():
            markup.add(types.KeyboardButton(f"{college} || {year} || {semester} || {group}"))
    else:
        for sub in subjects:
            # إضافة علامة صح إذا الملف موجود
            prefix = "✅ " if get_file_id(sub) else "📝 "
            markup.add(types.KeyboardButton(f"{prefix}{sub}"))
            
    markup.add(types.KeyboardButton("🔙 رجوع"), types.KeyboardButton("🏠 القائمة الرئيسية"))
    return markup

def group_subjects_menu_markup(college, year, semester, group):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    subjects = DATA[college][year][semester][group]
    for sub in subjects:
        prefix = "✅ " if get_file_id(sub) else "📝 "
        markup.add(types.KeyboardButton(f"{prefix}{sub}"))
    markup.add(types.KeyboardButton("🔙 رجوع"), types.KeyboardButton("🏠 القائمة الرئيسية"))
    return markup

# ================= معالجة الرسائل =================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # تفريغ حالة الرفع للأدمن عند البدء من جديد
    if message.from_user.id in admin_upload_state:
        del admin_upload_state[message.from_user.id]
        
    bot.send_message(message.chat.id, 
                     "📚 *أهلاً بك في مكتبة الشام الافتراضية*\n\nاختر الكلية:", 
                     reply_markup=main_menu_markup(), parse_mode="Markdown")

# --- 1. اختيار الكلية ---
@bot.message_handler(func=lambda message: message.text in DATA.keys())
def handle_college(message):
    college = message.text
    bot.send_message(message.chat.id, f"🏛 {college}\nاختر السنة الدراسية:", 
                     reply_markup=years_menu_markup(college))

# --- 2. اختيار السنة ---
@bot.message_handler(func=lambda message: " - " in message.text and " | " not in message.text)
def handle_year(message):
    try:
        college, year = message.text.split(" - ")
        if college in DATA and year in DATA[college]:
            bot.send_message(message.chat.id, f"📅 {year}\nاختر الفصل:", 
                             reply_markup=semester_menu_markup(college, year))
    except:
        bot.send_message(message.chat.id, "حدث خطأ، يرجى العودة للقائمة الرئيسية", reply_markup=main_menu_markup())

# --- 3. اختيار الفصل ---
@bot.message_handler(func=lambda message: " | " in message.text and " || " not in message.text)
def handle_semester(message):
    try:
        parts = message.text.split(" | ")
        college, year, semester = parts[0], parts[1], parts[2]
        bot.send_message(message.chat.id, f"📖 {semester}\nاختر المادة:", 
                         reply_markup=subjects_menu_markup(college, year, semester))
    except:
        bot.send_message(message.chat.id, "حدث خطأ، يرجى العودة للقائمة الرئيسية", reply_markup=main_menu_markup())

# --- 4. اختيار المجموعة (للسنة الرابعة حقوق) ---
@bot.message_handler(func=lambda message: " || " in message.text)
def handle_group(message):
    try:
        parts = message.text.split(" || ")
        college, year, semester, group = parts[0], parts[1], parts[2], parts[3]
        bot.send_message(message.chat.id, f"📂 {group}\nاختر المادة:", 
                         reply_markup=group_subjects_menu_markup(college, year, semester, group))
    except:
        bot.send_message(message.chat.id, "حدث خطأ، يرجى العودة للقائمة الرئيسية", reply_markup=main_menu_markup())

# --- 5. النقر على مادة (تحميل أو رفع) ---
@bot.message_handler(func=lambda message: message.text.startswith(("✅ ", "📝 ")))
def handle_subject_click(message):
    subject_name = message.text[2:] # حذف الرمز من البداية
    file_id = get_file_id(subject_name)
    user_id = message.from_user.id
    
    # إذا كان المستخدم هو المشرف (أنت)
    if user_id in ADMIN_IDS:
        markup = types.InlineKeyboardMarkup()
        if file_id:
            markup.add(types.InlineKeyboardButton("📥 تحميل الملف للتجربة", callback_data=f"dl_{subject_name}"))
            markup.add(types.InlineKeyboardButton("♻️ تغيير الملف", callback_data=f"up_{subject_name}"))
            bot.reply_to(message, f"👨‍✈️ **لوحة التحكم بالمادة:** {subject_name}\nالملف موجود حالياً. ماذا تريد أن تفعل؟", reply_markup=markup, parse_mode="Markdown")
        else:
            markup.add(types.InlineKeyboardButton("📤 رفع الملف الآن", callback_data=f"up_{subject_name}"))
            bot.reply_to(message, f"👨‍✈️ **لوحة التحكم بالمادة:** {subject_name}\n⚠️ لا يوجد ملف لهذه المادة.\nاضغط الزر بالأسفل لرفع الملف.", reply_markup=markup, parse_mode="Markdown")
    
    # إذا كان المستخدم طالب عادي
    else:
        if file_id:
            bot.send_chat_action(message.chat.id, 'upload_document')
            bot.send_document(message.chat.id, file_id, caption=f"📚 مادة: {subject_name}\n\n🤖 مكتبة الشام الافتراضية")
        else:
            bot.reply_to(message, f"⏳ عذراً، ملف مادة *{subject_name}* غير متوفر حالياً. سيتم رفعه قريباً.", parse_mode="Markdown")

# --- معالجة أزرار الأدمن (الرفع) ---
@bot.callback_query_handler(func=lambda call: True)
def admin_callbacks(call):
    if call.data.startswith("dl_"): # تحميل للتجربة
        subject = call.data[3:]
        file_id = get_file_id(subject)
        bot.send_document(call.message.chat.id, file_id, caption=f"تجربة تحميل: {subject}")
    
    elif call.data.startswith("up_"): # طلب رفع
        subject = call.data[3:]
        admin_upload_state[call.from_user.id] = subject # حفظ الحالة أن هذا الأدمن يريد رفع ملف لهذه المادة
        bot.send_message(call.message.chat.id, f"📤 **وضع الرفع:**\n\nقم الآن بإرسال ملف PDF الخاص بمادة: \n*{subject}*\n\n(أرسل الملف مباشرة هنا في المحادثة)", parse_mode="Markdown")

# --- استقبال الملف من الأدمن وحفظه ---
@bot.message_handler(content_types=['document'])
def save_uploaded_file(message):
    user_id = message.from_user.id
    # التحقق هل هذا الملف مرسل من الأدمن وهل الأدمن في وضع الرفع؟
    if user_id in ADMIN_IDS and user_id in admin_upload_state:
        subject = admin_upload_state[user_id]
        file_id = message.document.file_id
        
        # الحفظ
        save_file_id(subject, file_id)
        
        # تنظيف الحالة
        del admin_upload_state[user_id]
        
        bot.reply_to(message, f"✅ **تم الحفظ بنجاح!**\n\nتم ربط هذا الملف بمادة: {subject}\nالآن يستطيع الطلاب تحميله.", parse_mode="Markdown")
    else:
        # إذا أرسل شخص عادي ملفاً
        if user_id not in ADMIN_IDS:
            bot.reply_to(message, "عذراً، لا يمكنك رفع الملفات هنا.")

# --- أزرار التنقل العامة ---
@bot.message_handler(func=lambda message: message.text == "🔙 رجوع")
def handle_back(message):
    # هذه دالة ذكية تحاول تخمين القائمة السابقة بناءً على النص الأخير (اختياري)
    # لكن الأفضل هنا توجيه المستخدم للقائمة الرئيسية لتجنب الأخطاء، أو بناء منطق تتبع
    # للتبسيط وضمان عدم توقف البوت، زر الرجوع هنا سيعيد للقائمة الرئيسية كخيار آمن
    # أو يمكنك استخدام logic بسيط:
    bot.send_message(message.chat.id, "العودة للقائمة الرئيسية...", reply_markup=main_menu_markup())

@bot.message_handler(func=lambda message: message.text == "🏠 القائمة الرئيسية")
def go_home(message):
    send_welcome(message)

# تشغيل البوت
if __name__ == "__main__":
    print("🚀 البوت يعمل الآن 24/7...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
