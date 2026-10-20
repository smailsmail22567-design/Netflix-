import json
import os
import urllib.parse
import urllib.request
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

TOKEN = "8882053235:AAHfSGD0w2xPHlXWs3qax_NAtHBjCzjjScE"
ADMIN_CHANNEL = "@prov_ed"
DATA_FILE = "bot_data.json"
TASK_IMAGE_URL = "https://i.postimg.cc/Wz1RbxV5/IMG-20261018-154729-251.jpg"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = {}
    else:
        data = {}
    
    if "settings" not in data:
        data["settings"] = {"tak": "on", "tawgeh": "on", "bott": "on", "premium": "off"}
    if "banned" not in data:
        data["banned"] = []
    if "admins" not in data:
        data["admins"] = [7300916931]
    if "vips" not in data:
        data["vips"] = []
    if "eshterak" not in data:
        data["eshterak"] = {}
    if "tasks_progress" not in data:
        data["tasks_progress"] = {}
    if "devices" not in data:
        data["devices"] = {}
    if "verify_tokens" not in data:
        data["verify_tokens"] = {}
    if "verified_users" not in data:
        data["verified_users"] = []
    
    data["custom_tasks"] = [
        {
            "id": 1,
            "text": "👋 أهلاً بك في قسم المهام المجانية!\n\n📌 **الشرط الأول (1/3):**\nانضم للقناة عبر الرابط الخاص:\nhttps://t.me/+4jDGJ8ZM2XI2NzQ0\n\nوصور سكرين شوت أنك انضممت وأرسل الصورة إلى حسابي: @tawsiatKE\n\nبعد إرسالها، اضغط الزر أدناه:",
            "type": "text",
            "button_text": "✅ متابعة 1/3"
        },
        {
            "id": 2,
            "text": "🎉 ممتاز! أتممت الشرط الأول.\n\n📌 **الشرط الثاني (2/3):**\nصور سكرين شوت يظهر فيه البروفايل حقك و ID حسابك وانه موثق (كما في الصورة أعلاه)، وارسله في حسابي @tawsiatKE\n(عشان أقدر أكشف الحسابات الوهمية أو الفوتوشوب بطريقتي)\n\nبعد إرسالها اضغط الزر أدناه:",
            "type": "photo",
            "photo_url": TASK_IMAGE_URL,
            "button_text": "✅ متابعة 2/3"
        },
        {
            "id": 3,
            "text": "🔥 رائع جداً! بقيت الخطوة الأهم.\n\n📌 **الشرط الثالث والأهم (3/3):**\nممنوع مغادرة القناة بعد حصولك على الجائزة لأنك إنتهكت الشروط وربحك غير مباح\n\nإذا قرأت الشرط وتعهدت به، اضغط الزر أدناه:",
            "type": "text",
            "button_text": "✅ متابعة 3/3"
        }
    ]

    if "balances" not in data:
        data["balances"] = {}
    if "referrals" not in data:
        data["referrals"] = {}
    if "stats" not in data:
        data["stats"] = {"users": []}
    if "twasol" not in data:
        data["twasol"] = {}
    if "mode" not in data:
        data["mode"] = {}
        
    return data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()
save_data(data)

def api_request(method, params={}):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    data_encoded = urllib.parse.urlencode(params).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data_encoded)
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"API Error ({method}): {e}")
        return None

def send_message(chat_id, text, reply_markup=None, parse_mode="Markdown"):
    params = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup)
    return api_request("sendMessage", params)

def edit_message(chat_id, message_id, text, reply_markup=None, parse_mode="Markdown"):
    params = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": parse_mode}
    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup)
    return api_request("editMessageText", params)

def answer_callback(callback_query_id, text="", show_alert=False):
    params = {"callback_query_id": callback_query_id, "text": text}
    if show_alert:
        params["show_alert"] = True
    api_request("answerCallbackQuery", params)

def get_main_menu():
    return {
        "inline_keyboard": [
            [{"text": "✨ إتمام المهام", "callback_data": "start_tasks"}],
            [{"text": "👤 الملف الشخصي ورابط الإحالة", "callback_data": "profile"}],
            [{"text": "💰 سحب الأرباح ($)", "callback_data": "withdraw"}]
        ]
    }

def get_admin_keyboard():
    st = data["settings"]
    tak_icon = "✅" if st["tak"] == "on" else "❌"
    taw_icon = "✅" if st["tawgeh"] == "on" else "❌"
    bot_status = "يعمل ✅" if st["bott"] == "on" else "معطل ❌"
    prem_icon = "✅" if st["premium"] == "on" else "❌"

    return {
        "inline_keyboard": [
            [{"text": f"تنبيه دخول الاعضاء  {tak_icon}", "callback_data": "toggle_tak"}],
            [{"text": f"توجيه الرسائل  {taw_icon}", "callback_data": "toggle_tawgeh"}],
            [{"text": f"وضع البوت  {bot_status}", "callback_data": "toggle_bott"}],
            [{"text": f" الوضع المدفوع  {prem_icon}", "callback_data": "toggle_premium"}],
            [{"text": "• قسم الاشتراك الإجباري •", "callback_data": "sec_eshterak"}],
            [{"text": "• احصائيات البوت •", "callback_data": "sec_stats"}]
        ]
    }

def check_user_subscriptions(user_id):
    esh_list = data["eshterak"]
    if not esh_list:
        return []
    missing = []
    for ch in esh_list:
        if not isinstance(esh_list[ch], list):
            esh_list[ch] = []
        chk = api_request("getChatMember", {"chat_id": ch, "user_id": user_id})
        if not chk or not chk.get("ok") or chk["result"]["status"] in ["left", "kicked"]:
            missing.append(ch)
            if user_id in esh_list[ch]:
                esh_list[ch].remove(user_id)
                data["balances"][str(user_id)] = data["balances"].get(str(user_id), 0.0) - 0.005
                save_data(data)
        else:
            if user_id not in esh_list[ch]:
                esh_list[ch].append(user_id)
                save_data(data)
    return missing

class DeviceVerifyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/verify-device':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                req_data = json.loads(post_data.decode('utf-8'))
                token = req_data.get("token")
                user_id = str(req_data.get("user_id"))
                fingerprint = req_data.get("fingerprint")
                
                global data
                if not user_id or not fingerprint:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": "بيانات غير صالحة"}).encode('utf-8'))
                    return

                # فحص تكرار الجهاز بحساب آخر
                if fingerprint in data["devices"] and data["devices"][fingerprint] != user_id:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": "⛔ هذا الجهاز مسجل مسبقاً بحساب آخر ولا يمكن فتح حسابات متعددة!"}).encode('utf-8'))
                    return

                data["devices"][fingerprint] = user_id
                if user_id not in data["verified_users"]:
                    data["verified_users"].append(user_id)
                save_data(data)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(('', port), DeviceVerifyHandler).serve_forever()

threading.Thread(target=run_http_server, daemon=True).start()

bot_info = api_request("getMe")
BOT_USERNAME = bot_info["result"]["username"] if bot_info and bot_info.get("ok") else "YourBot"

print("🤖 البوت يعمل الآن بكفاءة تامة...")
offset = 0

while True:
    try:
        res = api_request("getUpdates", {"offset": offset, "timeout": 30})
        if not res or not res.get("ok"):
            time.sleep(2)
            continue

        for update in res.get("result", []):
            offset = update["update_id"] + 1

            if "callback_query" in update:
                cq = update["callback_query"]
                cq_id = cq["id"]
                user_id = cq["from"]["id"]
                data_call = cq["data"]
                msg = cq["message"]
                chat_id = msg["chat"]["id"]
                msg_id = msg["message_id"]

                if user_id in data["admins"]:
                    if data_call == "sec_stats":
                        total_users = len(data["stats"]["users"])
                        kb = {"inline_keyboard": [[{"text": "• رجوع •", "callback_data": "back_home"}]]}
                        edit_message(chat_id, msg_id, f"📊 **الإحصائيات:**\n\n- إجمالي المستخدمين: `{total_users}`", kb)
                        answer_callback(cq_id)

                if data_call == "profile":
                    balance = data["balances"].get(str(user_id), 0.0)
                    ref_count = len(data["referrals"].get(str(user_id), []))
                    ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
                    text_profile = f"👤 **الملف الشخصي:**\n\n💰 رصيدك الحالي: `{balance}$`\n👥 عدد الأشخاص الذين دعوتهم: `{ref_count}` شخص\n\n🔗 **رابط الإحالة:**\n`{ref_link}`"
                    edit_message(chat_id, msg_id, text_profile, {"inline_keyboard": [[{"text": "🔙 القائمة الرئيسية", "callback_data": "back_home"}]]})
                    answer_callback(cq_id)

                elif data_call == "withdraw":
                    balance = data["balances"].get(str(user_id), 0.0)
                    edit_message(chat_id, msg_id, f"💰 **سحب الأرباح:**\n\nرصيدك الحالي: `{balance}$`\n\n⚠️ الحد الأدنى للسحب هو `0.05$`.", {"inline_keyboard": [[{"text": "🔙 القائمة الرئيسية", "callback_data": "back_home"}]]})
                    answer_callback(cq_id)

                elif data_call == "back_home":
                    edit_message(chat_id, msg_id, "👋 أهلاً بك في القائمة الرئيسية للبوت، اختر ما يناسبك:", get_main_menu())
                    answer_callback(cq_id)

                elif data_call == "start_tasks":
                    data["tasks_progress"][str(user_id)] = {"step": 0, "status": "in_progress"}
                    save_data(data)
                    send_message(chat_id, "👋 أهلاً بك في قسم المهام المجانية!\n\n📌 **الشرط الأول:** انضم للقناة عبر الرابط الخاص وصور سكرين شوت وأرسله إلى: @tawsiatKE", {
                        "inline_keyboard": [
                            [{"text": "🔗 انضم للقناة", "url": "https://t.me/+4jDGJ8ZM2XI2NzQ0"}],
                            [{"text": "✅ متابعة", "callback_data": "next_task_step"}]
                        ]
                    })
                    answer_callback(cq_id)

            elif "message" in update:
                msg = update["message"]
                if "text" not in msg:
                    continue
                text = msg["text"]
                chat_id = msg["chat"]["id"]
                user_id = msg["from"]["id"]

                if chat_id > 0:
                    if user_id not in data["stats"]["users"]:
                        data["stats"]["users"].append(user_id)
                        save_data(data)

                    if text.startswith("/start"):
                        parts = text.split(" ")
                        if len(parts) > 1:
                            referrer_id = parts[1]
                            if referrer_id.isdigit() and int(referrer_id) != user_id:
                                ref_key = str(referrer_id)
                                if ref_key not in data["referrals"]:
                                    data["referrals"][ref_key] = []
                                if user_id not in data["referrals"][ref_key]:
                                    data["referrals"][ref_key].append(user_id)
                                    save_data(data)

                        if str(user_id) not in data.get("verified_users", []):
                            verify_token = str(int(time.time() * 1000)) + str(user_id)
                            data["verify_tokens"][verify_token] = user_id
                            save_data(data)

                            web_app_keyboard = {
                                "inline_keyboard": [
                                    [{"text": "🔒 تحقق من الجهاز للمتابعة", "web_app": {"url": f"https://smailsmail22567-design.github.io/Mini-app/?t={verify_token}"}}]
                                ]
                            }
                            send_message(chat_id, "👋 أهلاً بك! يرجى النقر على زر التحقق الأمني أدناه لبدء استخدام البوت:", web_app_keyboard)
                        else:
                            send_message(chat_id, "👋 أهلاً بك في بوت المهام المجانية وأرباح الدولار ($)!", get_main_menu())
    except Exception as e:
        print(f"Error in main loop: {e}")
        time.sleep(3)
