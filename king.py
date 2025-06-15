import telebot
import requests
import time
import json
import re
from telebot import types

bot = telebot.TeleBot('7823158391:AAHsuGiNw_tGx6OKCR7KlySXjulT2soxCFE')

PHONE, PASSWORD = range(2)
current_state = {}
started_users = set()
channel_username = "mabowaged_eg"

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    try:
        member = bot.get_chat_member(f"@{channel_username}", chat_id)
        if member.status not in ['member', 'creator', 'administrator']:
            raise Exception("User not subscribed")
    except:
        markup = types.InlineKeyboardMarkup()
        subscribe_button = types.InlineKeyboardButton("📢 اضغط هنا للاشتراك", url=f"https://t.me/{channel_username}")
        markup.add(subscribe_button)
        bot.send_message(chat_id, f"""اشترك في قناة العتاولة نت لاستخدام البوت ☠️

🔻 اشترك من الزر التالي ثم أعد إرسال /start ✅""", reply_markup=markup)
        return

    current_state[chat_id] = PHONE
    msg = bot.send_message(chat_id, """تيم العتاولة نت 🔥
عرض ال5G فودافون
قم بإرسال رقم هاتفك""")
    bot.register_next_step_handler(msg, process_phone_step)

def process_phone_step(message):
    chat_id = message.chat.id
    if len(message.text) != 11 or not message.text.isdigit():
        msg = bot.send_message(chat_id, """تيم العتاولة نت 🔥
عرض ال5G فودافون
قم بإرسال رقم هاتفك""")
        bot.register_next_step_handler(msg, process_phone_step)
        return
    current_state[chat_id] = PASSWORD
    phone_number = message.text
    current_state['nu'] = phone_number
    msg = bot.send_message(chat_id, "قم بإدخال كلمة مرور حسابك في فودافون")
    bot.register_next_step_handler(msg, process_password_step)

def process_password_step(message):
    chat_id = message.chat.id
    if message.text == "/start":
        start(message)
        return

    current_state['pas'] = message.text
    nu = current_state['nu']
    pas = current_state['pas']

    url = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
    payload = {
        'username': nu,
        'password': pas,
        'grant_type': "password",
        'client_secret': "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
        'client_id': "my-vodafone-app"
    }
    headers = {
        'User-Agent': "okhttp/4.9.1",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate",
        'Content-Type': "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)
    
    

    try:
        result = response.json()
    except ValueError:
        bot.send_message(chat_id, "❌ حدث خطأ في استلام البيانات من الخادم، يرجى المحاولة لاحقًا.")
        print("Response status:", response.status_code)
        print("Response text:", response.text)
        return

    if 'access_token' not in result:
        msg = bot.send_message(chat_id, "الرقم او كلمة السر غلط ❌")
        return
    else:
        token = result['access_token']
        bot.send_message(chat_id, "✅ تم تسجيل الدخول بنجاح")
        time.sleep(2)
        bot.send_message(chat_id, "⏳ جاري الحصول على العرض...")


if __name__ == '__main__':
    print("✅ تم تشغيل البوت بنجاح")
    bot.polling(none_stop=True)
