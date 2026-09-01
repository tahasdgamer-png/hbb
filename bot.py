import os
import json
import asyncio
import requests
from sseclient import SSEClient

# =========================================================
# تنظیمات - با توکن و رمزهای جدیدت ⭐
# =========================================================

BOT_TOKEN = "69698541:IwcaAx2v8jYPhBOZoCZhw5uRUqLcTZ-t9K0"

# رمزهای جدیدت اینجا مستقیم قرار داده شد
M_PASSWORD = "Melalestanadmingame"  # رمز مدیریت
A_PASSWORD = "TAHA1389110313"        # رمز ادمین

# آیدی/یوزرنیم مقصد پیام‌های /sendmassage
MESSAGE_TARGET = "@Mojaheds"

DATA_FILE = "heydareye_data.json"
MAP_FILE = "map.jpg"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


# =========================================================
# داده اولیه کشور
# =========================================================

DEFAULT_DATA = {
    "country_info": """🇮🇷 جمهوری اسلامی حیدریه

پایتخت: کرار
نوع حکومت: جمهوری اسلامی
زبان رسمی: فارسی
دین رسمی: اسلام
مذهب: شیعه دوازده امامی

رهبر: آیت‌الله العظمی طاها خلیلانی
رئیس دولت: آیت‌الله جوادی
""",

    "money": 0,

    "military_assets": """⚔️ دارایی‌های نظامی جمهوری اسلامی حیدریه

• تانک: 0
• نفربر: 0
• توپخانه: 0
• هواگرد: 0
• پهپاد: 0
• ناو/شناور: 0
""",

    "weapon_permissions": """🏭 مجوزهای تسلیحاتی حیدریه

هنوز هیچ مجوزی ثبت نشده است.
"""
}


# =========================================================
# مدیریت فایل داده
# =========================================================

def load_data():

    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for key, value in DEFAULT_DATA.items():
            if key not in data:
                data[key] = value

        return data

    except Exception:
        return DEFAULT_DATA.copy()


def save_data(data):

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


data = load_data()


# =========================================================
# احراز هویت موقت
# =========================================================

authenticated = {}


def get_access(user_id):

    return authenticated.get(str(user_id))


def is_manager(user_id):

    return get_access(user_id) in ["m", "a"]


def is_admin(user_id):

    return get_access(user_id) == "a"


# =========================================================
# ارسال پیام
# =========================================================

def send_message(chat_id, text):

    payload = {
        "type": "TEXT",
        "to": chat_id,
        "body": text
    }

    url = f"https://bot.splus.ir/{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json=payload,
        headers=HEADERS,
        timeout=20
    )

    return response


def send_photo(chat_id, photo_path):

    send_message(
        chat_id,
        "🗺️ قابلیت ارسال مستقیم فایل نقشه باید با endpoint آپلود فایل API سروش‌پلاس متصل شود."
    )


# =========================================================
# منوی عمومی
# =========================================================

def public_help():

    return """🤖 بات مدیریت جمهوری اسلامی حیدریه

دستورات عمومی:

/info
📋 اطلاعات کشور

/map
🗺️ نقشه حیدریه

/sendmassage
📨 ارسال پیام به حیدریه

/ms
🏭 مشاهده مجوزهای تسلیحاتی
"""


# =========================================================
# پنل M
# =========================================================

def manager_panel():

    return """🛡️ پنل مدیریت مللستان

دستورات قابل استفاده:

/ems
✏️ ویرایش مجوزهای تسلیحاتی

/emoney
💰 ویرایش مقدار پول

/eml
⚔️ ویرایش دارایی‌های نظامی
"""


# =========================================================
# پنل A
# =========================================================

def admin_panel():

    return """👑 پنل مدیریت ارشد حیدریه

دستورات:

/ems
✏️ ویرایش مجوزهای تسلیحاتی

/emoney
💰 ویرایش پول

/eml
⚔️ ویرایش دارایی‌های نظامی

/einfo
🏛️ ویرایش اطلاعات کشور

/emap
🗺️ تغییر نقشه
"""


# =========================================================
# پردازش پیام
# =========================================================

def process_message(message):

    global data

    user_id = str(message.get("from", ""))
    body = str(message.get("body", "")).strip()

    if not user_id:
        return None

    # -----------------------------------------------------
    # دستورات عمومی
    # -----------------------------------------------------

    if body == "/start":

        return public_help()

    if body == "/help":

        return public_help()

    if body == "/p":

        return public_help()

    if body == "/info":

        return data["country_info"]

    if body == "/ms":

        return data["weapon_permissions"]

    if body == "/map":

        if os.path.exists(MAP_FILE):
            return "__MAP__"

        return "❌ هنوز نقشه‌ای برای حیدریه ثبت نشده است."

    # -----------------------------------------------------
    # /m
    # -----------------------------------------------------

    if body == "/m":

        authenticated.pop(user_id, None)

        return """🔐 احراز هویت مدیریت

رمز مدیریت را ارسال کنید.
"""

    # -----------------------------------------------------
    # /a
    # -----------------------------------------------------

    if body == "/a":

        authenticated.pop(user_id, None)

        return """🔐 احراز هویت مدیر ارشد

رمز مدیر ارشد را ارسال کنید.
"""

    # -----------------------------------------------------
    # اگر کاربر در مرحله ورود رمز باشد
    # -----------------------------------------------------

    if get_access(user_id) is None:

        if M_PASSWORD and body == M_PASSWORD:

            authenticated[user_id] = "m"

            return manager_panel()

        if A_PASSWORD and body == A_PASSWORD:

            authenticated[user_id] = "a"

            return admin_panel()

    # -----------------------------------------------------
    # دستورات مدیریتی
    # -----------------------------------------------------

    access = get_access(user_id)

    # /ems
    if body == "/ems":

        if access not in ["m", "a"]:
            return "❌ شما اجازه استفاده از این دستور را ندارید."

        return """✏️ ویرایش مجوزهای تسلیحاتی

متن جدید لیست مجوزها را در پیام بعدی ارسال کنید.
"""

    # /emoney
    if body == "/emoney":

        if access not in ["m", "a"]:
            return "❌ شما اجازه استفاده از این دستور را ندارید."

        return f"""💰 مقدار فعلی پول:

{data["money"]}

برای تغییر مقدار، عدد جدید را ارسال کنید.
"""

    # /eml
    if body == "/eml":

        if access not in ["m", "a"]:
            return "❌ شما اجازه استفاده از این دستور را ندارید."

        return """⚔️ ویرایش دارایی نظامی

لیست جدید دارایی‌های نظامی را در پیام بعدی ارسال کنید.
"""

    # /einfo
    if body == "/einfo":

        if access != "a":
            return "❌ فقط مدیر ارشد اجازه استفاده از این دستور را دارد."

        return """🏛️ ویرایش اطلاعات کشور

اطلاعات جدید کشور را در پیام بعدی ارسال کنید.
"""

    # /emap
    if body == "/emap":

        if access != "a":
            return "❌ فقط مدیر ارشد اجازه استفاده از این دستور را دارد."

        return """🗺️ تغییر نقشه

در پیام بعدی عکس جدید نقشه را ارسال کنید.
"""

    # -----------------------------------------------------
    # دریافت مقدار پول
    # -----------------------------------------------------

    if access in ["m", "a"]:

        if body.isdigit():

            data["money"] = int(body)
            save_data(data)

            return f"""✅ مقدار پول با موفقیت تغییر کرد.

💰 موجودی جدید:
{data["money"]:,}
"""

    return None


# =========================================================
# حلقه دریافت پیام‌ها
# =========================================================

def run_bot():

    if not BOT_TOKEN:
        raise RuntimeError(
            "SPLUS_BOT_TOKEN تنظیم نشده است."
        )

    url = f"https://bot.splus.ir/v2/{BOT_TOKEN}/getMessage"

    print("================================")
    print("🇮🇷 Heydareye Bot")
    print("🤖 Bot started")
    print("================================")
    print(f"✅ رمز مدیریت (M): {M_PASSWORD}")
    print(f"✅ رمز ادمین (A): {A_PASSWORD}")
    print("================================")

    response = requests.get(
        url,
        stream=True,
        headers=HEADERS,
        timeout=None
    )

    client = SSEClient(response)

    for event in client.events():

        if not event.data:
            continue

        try:

            message = json.loads(event.data)

            result = process_message(message)

            if result is None:
                continue

            user_id = message.get("from")

            if result == "__MAP__":

                send_photo(user_id, MAP_FILE)

            else:

                send_message(
                    user_id,
                    result
                )

        except Exception as e:

            print("ERROR:", e)


# =========================================================
# اجرای بات
# =========================================================

if __name__ == "__main__":

    while True:

        try:

            run_bot()

        except KeyboardInterrupt:

            print("Bot stopped.")
            break

        except Exception as e:

            print("Connection error:", e)

            asyncio.run(asyncio.sleep(5))