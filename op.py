import telebot
import base64
import requests
import xml.etree.ElementTree as Et
from telebot import types

bot = telebot.TeleBot('7872275930:AAHO_nyMF0t-0cWvHF3w8TbUGIKjC37ob6s')

PHONE, PASSWORD = range(2)
current_state = {}
started_users = set()
channel_username = "mabowaged_eg"  # اسم القناة بدون @

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    try:
        member = bot.get_chat_member(f"@{channel_username}", chat_id)
        if member.status not in ['member', 'creator', 'administrator']:
            raise Exception("User not subscribed")
    except:
        markup = types.InlineKeyboardMarkup()
        subscribe_button = types.InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{channel_username}")
        check_button = types.InlineKeyboardButton("✅ تحقّق من الاشتراك", callback_data="check_subscription")
        markup.add(subscribe_button)
        markup.add(check_button)
        bot.send_message(chat_id, f"""اشترك في قناة العتاولة نت لاستخدام البوت ☠️

🔻 اشترك من الزر التالي ثم اضغط على "تحقق من الاشتراك" ✅""", reply_markup=markup)
        return

    if chat_id not in started_users:
        started_users.add(chat_id)
        current_state[chat_id] = PHONE
        msg = bot.send_message(chat_id, """العتاولة نت 🔥
        ساعتين اتصالات سوشيال 
        ارسل رقم هاتفك اتصالات""")
        bot.register_next_step_handler(msg, process_phone_step)

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    chat_id = call.message.chat.id
    try:
        member = bot.get_chat_member(f"@{channel_username}", chat_id)
        if member.status in ['member', 'creator', 'administrator']:
            bot.delete_message(chat_id, call.message.message_id)
            if chat_id not in started_users:
                started_users.add(chat_id)
                current_state[chat_id] = PHONE
                msg = bot.send_message(chat_id, """✅ تم التحقق من الاشتراك بنجاح!
العتاولة نت 🔥
ساعتين اتصالات سوشيال 
ارسل رقم هاتفك اتصالات""")
                bot.register_next_step_handler(msg, process_phone_step)
        else:
            raise Exception("Not subscribed")
    except:
        markup = types.InlineKeyboardMarkup()
        subscribe_button = types.InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{channel_username}")
        check_button = types.InlineKeyboardButton("✅ تحقّق من الاشتراك", callback_data="check_subscription")
        markup.add(subscribe_button)
        markup.add(check_button)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
            text=f"""اشترك في قناة العتاولة نت لاستخدام البوت ☠️

🔻 اشترك من الزر التالي ثم اضغط على "تحقق من الاشتراك" ✅""", reply_markup=markup)

def process_phone_step(message):
    chat_id = message.chat.id
    if len(message.text) != 11 or not message.text.isdigit():
        msg = bot.send_message(chat_id, "قم بإدخال رقم هاتف اتصالات المكون من 11 رقم ")
        bot.register_next_step_handler(msg, process_phone_step)
        return
    current_state[chat_id] = PASSWORD
    phone_number = message.text
    current_state['nu'] = phone_number
    msg = bot.send_message(chat_id, "قم بإدخال كلمة مرور تطبيق اتصالات")
    bot.register_next_step_handler(msg, process_password_step)

def process_password_step(message):
    chat_id = message.chat.id
    if message.text == "/start":
        msg = bot.send_message(chat_id, "قم بإدخال رقم هاتف اتصالات المكون من 11 رقم")
        bot.register_next_step_handler(msg, process_phone_step)
        return
    password = message.text
    current_state['pas'] = password
    msg = bot.send_message(chat_id, "قم بإدخال الإيميل الخاص بتطبيق اتصالات")
    bot.register_next_step_handler(msg, process_email_step)

def process_email_step(message):
    chat_id = message.chat.id
    if message.text == "/start":
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, "قم بإدخال رقم هاتف اتصالات المكون من 11 رقم")
        bot.register_next_step_handler(msg, process_phone_step)
        return
    email = message.text
    current_state['em'] = email
    jo14 = current_state['nu']
    jo13 = current_state['pas']
    jo12 = current_state['em']
    jo16 = jo12 + ":" + jo13
    jo17 = jo16.encode("ascii")
    jo18 = base64.b64encode(jo17)
    jo19 = jo18.decode("ascii")
    jo20 = "Basic" + " " + jo19
    if "011" in jo14:
        jo15 = jo14[+1:]
    else:
        jo15 = jo14

    jo21 = "https://mab.etisalat.com.eg:11003/Saytar/rest/authentication/loginWithPlan"

    jo22 = {
        "applicationVersion": "2",
        "applicationName": "MAB",
        "Accept": "text/xml",
        "Authorization": jo20,
        "APP-BuildNumber": "964",
        "APP-Version": "27.0.0",
        "OS-Type": "Android",
        "OS-Version": "12",
        "APP-STORE": "GOOGLE",
        "Is-Corporate": "false",
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": "1375",
        "Host": "mab.etisalat.com.eg:11003",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/5.0.0-alpha.11",
        "ADRUM_1": "isMobile:true",
        "ADRUM": "isAjax:true"
    }

    jo23 = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><loginRequest><deviceId></deviceId><firstLoginAttempt>true</firstLoginAttempt><modelType></modelType><osVersion></osVersion><platform>Android</platform><udid></udid></loginRequest>"
    jo24 = requests.post(jo21, headers=jo22, data=jo23)

    if "true" in jo24.text:
        msg = bot.send_message(chat_id, "تم تسجيل الدخول للحساب بنجاح")
        msg = bot.send_message(chat_id, "انتظر🤌🔥")
        st = jo24.headers["Set-Cookie"]
        ck = st.split(";")[0]
        br = jo24.headers["auth"]
    else:
        msg = bot.send_message(chat_id, "رقم الهاتف او كلمة المرور او الايميل خطأ اعد المحاولة مره اخري")
        return

    jo25 = "https://mab.etisalat.com.eg:11003/Saytar/rest/zero11/offersV3?req=<dialAndLanguageRequest><subscriberNumber>%s</subscriberNumber><language>1</language></dialAndLanguageRequest>" % (jo15)

    jo26 = {
        'applicationVersion': "2",
        'Content-Type': "text/xml",
        'applicationName': "MAB",
        'Accept': "text/xml",
        'Language': "ar",
        'APP-BuildNumber': "10459",
        'APP-Version': "29.9.0",
        'OS-Type': "Android",
        'OS-Version': "11",
        'APP-STORE': "GOOGLE",
        'auth': "Bearer " + br,
        'Host': "mab.etisalat.com.eg:11003",
        'Is-Corporate': "false",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'User-Agent': "okhttp/5.0.0-alpha.11",
        'Cookie': ck
    }

    jo27 = requests.get(jo25, headers=jo26)

    if jo27.status_code == 200:
        root = Et.fromstring(jo27.text)
        jo28 = None
        for category in root.findall('.//mabCategory'):
            for product in category.findall('.//mabProduct'):
                for parameter in product.findall('.//fulfilmentParameter'):
                    if parameter.find('name').text == 'Offer_ID':
                        jo28 = parameter.find('value').text
                        msg = bot.send_message(chat_id, f"تم الوصول إلى العرض. آيدي العرض: {jo28}. انتظر، جاري تفعيل العرض حالًا ❤️‍🔥")
                        break
                if jo28:
                    break
            if jo28:
                break
    else:
        msg = bot.send_message(chat_id, "عفوا هذا العرض غير متاح لخطك النهارده جرب تاني بكرة")
        return

    jo29 = "https://mab.etisalat.com.eg:11003/Saytar/rest/zero11/submitOrder"

    jo30 = {
        "applicationVersion": "2",
        "applicationName": "MAB",
        "Accept": "text/xml",
        "Cookie": ck,
        "Language": "ar",
        "APP-BuildNumber": "964",
        "APP-Version": "27.0.0",
        "OS-Type": "Android",
        "OS-Version": "12",
        "APP-STORE": "GOOGLE",
        "auth": "Bearer " + br + "",
        "Is-Corporate": "false",
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": "1375",
        "Host": "mab.etisalat.com.eg:11003",
        "Connection": "Keep-Alive",
        "User-Agent": "okhttp/5.0.0-alpha.11"
    }

    jo31 = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><submitOrderRequest><mabOperation></mabOperation><msisdn>%s</msisdn><operation>ACTIVATE</operation><parameters><parameter><name>GIFT_FULLFILMENT_PARAMETERS</name><value>Offer_ID:%s;ACTIVATE:True;isRTIM:Y</value></parameter></parameters><productName>FAN_ZONE_HOURLY_BUNDLE</productName></submitOrderRequest>" % (jo15, jo28)

    jo32 = requests.post(jo29, headers=jo30, data=jo31).text
    if "true" in jo32:
        msg = bot.send_message(chat_id, "تم الحصول علي الساعتين سوشيال بنجاح")
    else:
        msg = bot.send_message(chat_id, "انت اخدت العرض ده  النهاردة حاول بكرة تاني")

if __name__ == '__main__':
    bot.polling(none_stop=True)
