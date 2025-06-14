import telebot
import requests
import time
import json
import re

bot = telebot.TeleBot('7823158391:AAHsuGiNw_tGx6OKCR7KlySXjulT2soxCFE')

PHONE, PASSWORD = range(2)
current_state = {}
started_users = set()

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id not in started_users:
        started_users.add(chat_id)
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
    result = response.json()

    if 'access_token' not in result:
        bot.send_message(chat_id, "الرقم او كلمة السر غلط ❌")
        return

    token = result['access_token']
    bot.send_message(chat_id, "✅ تم تسجيل الدخول بنجاح")
    time.sleep(2)
    bot.send_message(chat_id, "⏳ جاري الحصول على العرض...")

    number = nu
    url2 = "https://web.vodafone.com.eg/services/dxl/promo/promotion"
    params2 = {
        "@type": "Promo",
        "$.context.type": "5G_Promo",
        "$.characteristics[@name=customerNumber].value": number
    }
    headers2 = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 14; RMX3890) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.61 Mobile Safari/537.36",
        'Accept': "application/json",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'sec-ch-ua-platform': "\"Android\"",
        'Authorization': f"Bearer {token}",
        'Accept-Language': "AR",
        'msisdn': number,
        'sec-ch-ua': "\"Android WebView\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        'clientId': "WebsiteConsumer",
        'sec-ch-ua-mobile': "?1",
        'channel': "APP_PORTAL",
        'Content-Type': "application/json",
        'X-Requested-With': "mark.via.gp",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://web.vodafone.com.eg/portal/bf/5gGame",
    }

    response2 = requests.get(url2, headers=headers2, params=params2)
    data = response2.json()

    played_levels = []
    locked_today = False
    current_level = None

    for item in data[0]['characteristics']:
        if item['name'] == 'playedLevels':
            played_levels = list(map(int, item['value'].split(','))) if item['value'] else []
        elif item['name'] == 'playedToday':
            locked_today = item['value'] == "1"
        elif item['name'] == 'currentLevel':
            current_level = int(item['value'])

    next_level = max(played_levels) + 1 if played_levels else 1

    if locked_today or next_level > current_level:
        bot.send_message(chat_id, "❌ انت اخدت العرض النهارده")
        return

    url3 = "https://web.vodafone.com.eg/services/dxl/promo/promotion"
    payload3 = {
        "@type": "Promo",
        "channel": {"id": "APP_PORTAL"},
        "context": {"type": "5G_Promo"},
        "pattern": [{
            "characteristics": [
                {"name": "level", "value": current_level},
                {"name": "score", "value": 50},
                {"name": "customerNumber", "value": number}
            ]
        }]
    }
    headers3 = headers2.copy()
    headers3['Referer'] = f"https://web.vodafone.com.eg/portal/bf/5gGame/game-page?currentLevel={current_level}&gameLevel={current_level}"

    response3 = requests.post(url3, data=json.dumps(payload3), headers=headers3)
    match = re.search(r'"actionValue"\s*:\s*([\d.]+)', response3.text)
    match_id = re.search(r'"id"\s*:\s*"([^"]+)"', response3.text)

    if match and match_id:
        MB = float(match.group(1))
        id = match_id.group(1)
        if MB == 0:
            bot.send_message(chat_id, "ملكش هدايا انهارده")
            return
        else:
            bot.send_message(chat_id, f"✅ كسبت {MB} ميجا مبروك")

        ugift = 'https://web.vodafone.com.eg/services/dxl/promo/promotion/' + id
        hgift = {
            "Host": "web.vodafone.com.eg",
            "Connection": "keep-alive",
            "Content-Length": "159",
            "sec-ch-ua-platform": "\"Android\"",
            "Authorization": f"Bearer {token}",
            "Accept-Language": "AR",
            "msisdn": number,
            "x-dtpc": "5$209503482_534h43vROPHBGIURHGCTKKFICPPWPSUHKLMMUHM-0e0",
            "clientId": "WebsiteConsumer",
            "sec-ch-ua": "\"Android WebView\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 15; ELI-NX9 Build/HONORELI-N39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.61 Mobile Safari/537.36",
            "Accept": "application/json",
            "channel": "APP_PORTAL",
            "Content-Type": "application/json",
            "Origin": "https://web.vodafone.com.eg",
            "X-Requested-With": "mark.via.gp",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://web.vodafone.com.eg/portal/bf/5gGame",
            "Accept-Encoding": "gzip, deflate, br, zstd",
        }
        dgift = {
            "@type": "Promo",
            "channel": {"id": "APP_PORTAL"},
            "context": {"type": "5G_Promo"},
            "pattern": [{
                "characteristics": [{
                    "name": "customerNumber",
                    "value": number
                }]
            }]
        }

        tgift = requests.patch(ugift, headers=hgift, json=dgift)
        if tgift.status_code == 204:
            bot.send_message(chat_id, "✅ تم الحصول على العرض بنجاح 🔥")
        else:
            bot.send_message(chat_id, "❌ حصل خطأ، حاول لاحقًا")
    else:
        bot.send_message(chat_id, "❌ لم يتم العثور على بيانات العرض أو حصل خطأ.")

if __name__ == '__main__':
    print("✅ تم تشغيل البوت بنجاح")
    bot.polling(none_stop=True)