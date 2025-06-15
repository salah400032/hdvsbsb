import telebot
import base64
import requests
import xml.etree.ElementTree as Et
from telebot import types

bot = telebot.TeleBot('7872275930:AAHO_nyMF0t-0cWvHF3w8TbUGIKjC37ob6s')

PHONE, PASSWORD, EMAIL = range(3)
user_state = {}
pending_subs = {}
channel_username = "mabowaged_eg"

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    if chat_id in pending_subs:
        try:
            bot.delete_message(chat_id, pending_subs[chat_id])
        except:
            pass
        del pending_subs[chat_id]

    try:
        member = bot.get_chat_member(f"@{channel_username}", chat_id)
        if member.status not in ['member', 'creator', 'administrator']:
            raise Exception("not subscribed")
    except:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{channel_username}")
        btn2 = types.InlineKeyboardButton("✅ تحقّق من الاشتراك", callback_data="check_subscription")
        markup.add(btn1)
        markup.add(btn2)
        msg = bot.send_message(chat_id, """اشترك في قناة العتاولة نت لاستخدام البوت ☠️

🔻 اشترك من الزر التالي ثم اضغط على "تحقق من الاشتراك" ✅""", reply_markup=markup)
        pending_subs[chat_id] = msg.message_id
        return

    user_state[chat_id] = PHONE
    msg = bot.send_message(chat_id, "العتاولة نت 🔥\nساعتين اتصالات سوشيال \nارسل رقم هاتفك اتصالات")
    bot.register_next_step_handler(msg, process_phone)

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    chat_id = call.message.chat.id
    try:
        member = bot.get_chat_member(f"@{channel_username}", chat_id)
        if member.status in ['member', 'creator', 'administrator']:
            try:
                bot.delete_message(chat_id, call.message.message_id)
            except:
                pass
            if chat_id in pending_subs:
                try:
                    bot.delete_message(chat_id, pending_subs[chat_id])
                except:
                    pass
                del pending_subs[chat_id]
            user_state[chat_id] = PHONE
            msg = bot.send_message(chat_id, "✅ تم التحقق من الاشتراك بنجاح!\nالعتاولة نت 🔥\nساعتين اتصالات سوشيال \nارسل رقم هاتفك اتصالات")
            bot.register_next_step_handler(msg, process_phone)
        else:
            raise Exception("still not subscribed")
    except:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{channel_username}")
        btn2 = types.InlineKeyboardButton("✅ تحقّق من الاشتراك", callback_data="check_subscription")
        markup.add(btn1)
        markup.add(btn2)
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text="اشترك في قناة العتاولة نت لاستخدام البوت ☠️\n🔻 اشترك من الزر التالي ثم اضغط على تحقق من الاشتراك ✅",
                                  reply_markup=markup)
        except:
            pass

def process_phone(message):
    chat_id = message.chat.id
    if user_state.get(chat_id) != PHONE:
        return
    phone = message.text.strip()
    if len(phone) != 11 or not phone.isdigit():
        msg = bot.send_message(chat_id, "قم بإدخال رقم هاتف اتصالات المكون من 11 رقم")
        bot.register_next_step_handler(msg, process_phone)
        return
    user_state[chat_id] = PASSWORD
    user_state[f"{chat_id}_phone"] = phone
    msg = bot.send_message(chat_id, "قم بإدخال كلمة مرور تطبيق اتصالات")
    bot.register_next_step_handler(msg, process_password)

def process_password(message):
    chat_id = message.chat.id
    if user_state.get(chat_id) != PASSWORD:
        return
    password = message.text
    user_state[chat_id] = EMAIL
    user_state[f"{chat_id}_pass"] = password
    msg = bot.send_message(chat_id, "قم بإدخال الإيميل الخاص بتطبيق اتصالات")
    bot.register_next_step_handler(msg, process_email)

def process_email(message):
    chat_id = message.chat.id
    if user_state.get(chat_id) != EMAIL:
        return
    email = message.text
    phone = user_state.get(f"{chat_id}_phone")
    password = user_state.get(f"{chat_id}_pass")
    user_state.pop(chat_id, None)

    encoded = base64.b64encode(f"{email}:{password}".encode()).decode()
    auth_header = "Basic " + encoded
    jo15 = phone[1:] if phone.startswith("011") else phone

    login_url = "https://mab.etisalat.com.eg:11003/Saytar/rest/authentication/loginWithPlan"
    login_headers = {
        "applicationVersion": "2",
        "applicationName": "MAB",
        "Accept": "text/xml",
        "Authorization": auth_header,
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
    login_data = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><loginRequest><deviceId></deviceId><firstLoginAttempt>true</firstLoginAttempt><modelType></modelType><osVersion></osVersion><platform>Android</platform><udid></udid></loginRequest>"
    login_res = requests.post(login_url, headers=login_headers, data=login_data)

    if "true" not in login_res.text:
        bot.send_message(chat_id, "رقم الهاتف او كلمة المرور او الايميل خطأ اعد المحاولة مره اخري")
        return

    bot.send_message(chat_id, "تم تسجيل الدخول للحساب بنجاح\nانتظر🤌🔥")

    st = login_res.headers["Set-Cookie"]
    ck = st.split(";")[0]
    br = login_res.headers["auth"]

    offers_url = f"https://mab.etisalat.com.eg:11003/Saytar/rest/zero11/offersV3?req=<dialAndLanguageRequest><subscriberNumber>{jo15}</subscriberNumber><language>1</language></dialAndLanguageRequest>"
    offers_headers = {
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
    offers_res = requests.get(offers_url, headers=offers_headers)

    if offers_res.status_code != 200:
        bot.send_message(chat_id, "عفوا هذا العرض غير متاح لخطك النهارده جرب تاني بكرة")
        return

    root = Et.fromstring(offers_res.text)
    offer_id = None
    for category in root.findall('.//mabCategory'):
        for product in category.findall('.//mabProduct'):
            for parameter in product.findall('.//fulfilmentParameter'):
                if parameter.find('name').text == 'Offer_ID':
                    offer_id = parameter.find('value').text
                    break
            if offer_id:
                break
        if offer_id:
            break

    if not offer_id:
        bot.send_message(chat_id, "لم يتم العثور على عرض مناسب")
        return

    bot.send_message(chat_id, f"تم الوصول إلى العرض. آيدي العرض: {offer_id}. انتظر، جاري تفعيل العرض حالًا ❤️‍🔥")

    activate_url = "https://mab.etisalat.com.eg:11003/Saytar/rest/zero11/submitOrder"
    activate_headers = {
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
        "auth": "Bearer " + br,
        "Is-Corporate": "false",
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": "1375",
        "Host": "mab.etisalat.com.eg:11003",
        "Connection": "Keep-Alive",
        "User-Agent": "okhttp/5.0.0-alpha.11"
    }
    activate_data = f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><submitOrderRequest><mabOperation></mabOperation><msisdn>{jo15}</msisdn><operation>ACTIVATE</operation><parameters><parameter><name>GIFT_FULLFILMENT_PARAMETERS</name><value>Offer_ID:{offer_id};ACTIVATE:True;isRTIM:Y</value></parameter></parameters><productName>FAN_ZONE_HOURLY_BUNDLE</productName></submitOrderRequest>"
    activate_res = requests.post(activate_url, headers=activate_headers, data=activate_data)

    if "true" in activate_res.text:
        bot.send_message(chat_id, "تم الحصول علي الساعتين سوشيال بنجاح")
    else:
        bot.send_message(chat_id, "انت اخدت العرض ده النهاردة حاول بكرة تاني")

if __name__ == "__main__":
    bot.polling(none_stop=True)
