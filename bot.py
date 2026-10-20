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

def send_photo(chat_id, photo_url, caption, reply_markup=None, parse_mode="Markdown"):
    params = {"chat_id": chat_id, "photo": photo_url, "caption": caption, "parse_mode": parse_mode}
    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup)
    return api_request("sendPhoto", params)

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
                try:
                    send_message(user_id, f"⚠️ **تنبيه:** لقد قمت بمغادرة قناة الاشتراك الإجباري `{ch}`, ولهذا تم خصم `0.005$` من رصيدك!")
                except:
                    pass
        else:
            if user_id not in esh_list[ch]:
                esh_list[ch].append(user_id)
                save_data(data)
    return missing

class DeviceVerifyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/verify':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                req_data = json.loads(post_data.decode('utf-8'))
                token = req_data.get("token")
                components = req_data.get("components", {})
                
                global data
                if not token or token not in data.get("verify_tokens", {}):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Invalid or expired token")
                    return

                user_id = str(data["verify_tokens"][token])
                fingerprint_string = f"{components.get('canvas')}_{components.get('webgl')}_{components.get('screen')}_{components.get('platform')}"
                
                if fingerprint_string in data["devices"] and data["devices"][fingerprint_string] != user_id:
                    self.send_response(409)
                    self.end_headers()
                    self.wfile.write(b"Device already registered with another account")
                    return

                data["devices"][fingerprint_string] = user_id
                del data["verify_tokens"][token]
                save_data(data)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Verified successfully")
            except Exception as e:
                print(f"API Verify Error: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, DeviceVerifyHandler)
    print(f"🌐 سيرفر التحقق يعمل على المنفذ {port}...")
    httpd.serve_forever()

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
                    if data_call == "toggle_tak":
                        data["settings"]["tak"] = "off" if data["settings"]["tak"] == "on" else "on"
                        save_data(data)
                        edit_message(chat_id, msg_id, "⚙️ **لوحة التحكم الرئيسية:**", get_admin_keyboard())
                        answer_callback(cq_id, "تم التعديل")
                    elif data_call == "toggle_tawgeh":
                        data["settings"]["tawgeh"] = "off" if data["settings"]["tawgeh"] == "on" else "on"
                        save_data(data)
                        edit_message(chat_id, msg_id, "⚙️ **لوحة التحكم الرئيسية:**", get_admin_keyboard())
                        answer_callback(cq_id, "تم التعديل")
                    elif data_call == "toggle_bott":
                        data["settings"]["bott"] = "off" if data["settings"]["bott"] == "on" else "on"
                        save_data(data)
                        edit_message(chat_id, msg_id, "⚙️ **لوحة التحكم الرئيسية:**", get_admin_keyboard())
                        answer_callback(cq_id, "تم التعديل")
                    elif data_call == "toggle_premium":
                        data["settings"]["premium"] = "off" if data["settings"]["premium"] == "on" else "on"
                        save_data(data)
                        edit_message(chat_id, msg_id, "⚙️ **لوحة التحكم الرئيسية:**", get_admin_keyboard())
                        answer_callback(cq_id, "تم التعديل")
                    elif data_call == "sec_stats":
                        total_users = len(data["stats"]["users"])
                        kb = {"inline_keyboard": [[{"text": "• رجوع •", "callback_data": "back_home"}]]}
                        edit_message(chat_id, msg_id, f"📊 **الإحصائيات:**\n\n- إجمالي المستخدمين: `{total_users}`", kb)
                        answer_callback(cq_id)
                    elif data_call == "sec_eshterak":
                        kb = {
                            "inline_keyboard": [
                                [{"text": "+ اضف قناة +", "callback_data": "add_esh"}, {"text": "👁 عرض القنوات", "callback_data": "view_esh"}],
                                [{"text": "❗ حذف الكل", "callback_data": "clear_esh"}],
                                [{"text": "• رجوع •", "callback_data": "back_home"}]
                            ]
                        }
                        edit_message(chat_id, msg_id, "📌 **قسم إدارة الاشتراك الإجباري:**", kb)
                        answer_callback(cq_id)
                    elif data_call == "add_esh":
                        data["mode"][str(user_id)] = "waiting_channel"
                        save_data(data)
                        kb = {"inline_keyboard": [[{"text": "• إلغاء •", "callback_data": "sec_eshterak"}]]}
                        edit_message(chat_id, msg_id, "👤 أرسل الآن معرف القناة أو يوزرها (مثلاً `@Channel`):", kb)
                        answer_callback(cq_id)
                    elif data_call == "view_esh":
                        esh_list = data["eshterak"]
                        text_esh = "📋 **قنوات الاشتراك الإجباري (خصم 0.005$ عند المغادرة):**\n\n"
                        if esh_list:
                            for ch in esh_list:
                                text_esh += f"🔹 `{ch}`\n"
                        else:
                            text_esh += "❌ لا توجد قنوات مضافة حالياً."
                        kb = {"inline_keyboard": [[{"text": "• رجوع •", "callback_data": "sec_eshterak"}]]}
                        edit_message(chat_id, msg_id, text_esh, kb)
                        answer_callback(cq_id)
                    elif data_call == "clear_esh":
                        data["eshterak"] = {}
                        save_data(data)
                        answer_callback(cq_id, "تم حذف القنوات")
                        edit_message(chat_id, msg_id, "✅ تم حذف جميع قنوات الاشتراك الإجباري.", {"inline_keyboard": [[{"text": "• رجوع •", "callback_data": "sec_eshterak"}]]})

                if data_call == "check_subs":
                    missing = check_user_subscriptions(user_id)
                    if missing:
                        answer_callback(cq_id, "❌ لم تقم بالاشتراك في جميع القنوات بعد!")
                    else:
                        answer_callback(cq_id, "✅ تم التحقق بنجاح!")
                        edit_message(chat_id, msg_id, "🎉 **أهلاً بك! لقد أتممت الاشتراك الإجباري بنجاح.**\n\nاختر ما ترغب به من الأزرار أدناه:", get_main_menu())

                if data_call == "profile":
                    check_user_subscriptions(user_id)
                    balance = data["balances"].get(str(user_id), 0.0)
                    ref_count = len(data["referrals"].get(str(user_id), []))
                    ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
                    
                    text_profile = (
                        f"👤 **الملف الشخصي:**\n\n"
                        f"💰 رصيدك الحالي: `{balance}$`\n"
                        f"👥 عدد الأشخاص الذين دعوتهم: `{ref_count}` شخص\n\n"
                        f"🔗 **رابط الإحالة الخاص بك:**\n`{ref_link}`\n\n"
                        f"💡 _كل شخص يدخل من رابطك ويتم المهمة تكسب 0.025$_"
                    )
                    kb = {"inline_keyboard": [[{"text": "🔙 القائمة الرئيسية", "callback_data": "back_home"}]]}
                    edit_message(chat_id, msg_id, text_profile, kb)
                    answer_callback(cq_id)

                elif data_call == "withdraw":
                    balance = data["balances"].get(str(user_id), 0.0)
                    kb = {"inline_keyboard": [[{"text": "🔙 القائمة الرئيسية", "callback_data": "back_home"}]]}
                    edit_message(chat_id, msg_id, f"💰 **سحب الأرباح:**\n\nرصيدك الحالي: `{balance}$`\n\n⚠️ الحد الأدنى للسحب هو `0.05$`.\nعند وصولك للحد الأدنى تواصل مع الإدارة للسحب.", kb)
                    answer_callback(cq_id)

                elif data_call == "back_home":
                    missing = check_user_subscriptions(user_id)
                    if missing:
                        btns = []
                        for ch in missing:
                            btns.append([{"text": f"انضم إلى القناة: {ch}", "url": f"https://t.me/{ch.lstrip('@')}"}])
                        btns.append([{"text": "🔄 تحقق من الاشتراك", "callback_data": "check_subs"}])
                        
                        verify_token = str(int(time.time() * 1000)) + str(user_id)
                        data["verify_tokens"][verify_token] = user_id
                        save_data(data)
                        
                        web_app_keyboard = {
                            "inline_keyboard": [
                                [{"text": "🔒 تحقق من الجهاز للمتابعة", "web_app": {"url": f"https://smailsmail22567-design.github.io/Mini-app/?t={verify_token}"}}],
                                *btns
                            ]
                        }
                        edit_message(chat_id, msg_id, "⚠️ **تنبيه أمني:**\nيجب عليك فتح واجهة التحقق والاشتراك في القنوات للاستخدام:", web_app_keyboard)
                    else:
                        edit_message(chat_id, msg_id, "👋 أهلاً بك في القائمة الرئيسية للبوت، اختر ما يناسبك:", get_main_menu())
                    answer_callback(cq_id)

                elif data_call == "start_tasks":
                    current_status = data["tasks_progress"].get(str(user_id), {"step": 0, "status": "none"})
                    if current_status["status"] == "completed" or current_status["status"] == "pending":
                        answer_callback(cq_id, "⚠️ لقد أتممت المهام بالفعل ولا يمكنك إعادتها حتى تتوفر مهام جديدة!", show_alert=True)
                        continue
                    
                    tasks = data["custom_tasks"]
                    if not tasks:
                        answer_callback(cq_id, "⚠️ لا توجد مهام مضافة حالياً من قبل الإدارة.", show_alert=True)
                        continue

                    data["tasks_progress"][str(user_id)] = {"step": 0, "status": "in_progress"}
                    save_data(data)
                    
                    t = tasks[0]
                    kb = {
                        "inline_keyboard": [
                            [{"text": "🔗 انضم للقناة (رابط الخاص)", "url": "https://t.me/+4jDGJ8ZM2XI2NzQ0"}],
                            [{"text": t["button_text"], "callback_data": "next_task_step"}],
                            [{"text": "🔙 رجوع", "callback_data": "back_home"}]
                        ]
                    }
                    send_message(chat_id, t['text'], kb)
                    answer_callback(cq_id)

                elif data_call == "next_task_step":
                    user_prog = data["tasks_progress"].get(str(user_id), {"step": 0, "status": "in_progress"})
                    current_step = user_prog["step"] + 1
                    tasks = data["custom_tasks"]

                    if current_step < len(tasks):
                        user_prog["step"] = current_step
                        save_data(data)
                        
                        t = tasks[current_step]
                        if t.get("type") == "photo":
                            kb = {
                                "inline_keyboard": [
                                    [{"text": t["button_text"], "callback_data": "next_task_step"}],
                                    [{"text": "🔙 رجوع", "callback_data": "back_home"}]
                                ]
                            }
                            send_photo(chat_id, t["photo_url"], t["text"], kb)
                        else:
                            kb = {
                                "inline_keyboard": [
                                    [{"text": t["button_text"], "callback_data": "next_task_step"}],
                                    [{"text": "🔙 رجوع", "callback_data": "back_home"}]
                                ]
                            }
                            send_message(chat_id, t["text"], kb)
                    else:
                        user_prog["status"] = "pending"
                        save_data(data)

                        name = cq["from"].get("first_name", "مستخدم")
                        username = f"@{cq['from'].get('username')}" if cq['from'].get('username') else "لا يوجد"
                        admin_kb = {
                            "inline_keyboard": [
                                [
                                    {"text": "✅ موافقة", "callback_data": f"approve_{user_id}"},
                                    {"text": "❌ رفض", "callback_data": f"reject_{user_id}"}
                                ]
                            ]
                        }
                        send_message(ADMIN_CHANNEL, f"🚨 **طلب مهمة مجانية جديد!**\n\n👤 الاسم: {name}\n🔗 المعرف: {username}\n🆔 الايدي: `{user_id}`\n📌 أكمل جميع الشروط والمهام بنجاح.", admin_kb)
                        send_message(chat_id, "✅ **تهانينا!** أتممت جميع الشروط والمهام بنجاح وتم إرسال طلبك لقناة الإدارة للمراجعة.", get_main_menu())
                    
                    answer_callback(cq_id)

                if data_call.startswith("approve_") or data_call.startswith("reject_"):
                    action, target_id_str = data_call.split("_")
                    target_id = int(target_id_str)

                    if action == "approve":
                        data["tasks_progress"][str(target_id)] = {"step": 0, "status": "completed"}

                        for referrer_id, refs in data["referrals"].items():
                            if target_id in refs and f"rewarded_{target_id}" not in refs:
                                data["balances"][referrer_id] = data["balances"].get(referrer_id, 0.0) + 0.025
                                data["referrals"][referrer_id].append(f"rewarded_{target_id}")
                                save_data(data)
                                send_message(int(referrer_id), "🎉 **مبروك!** لقد انضم شخص من رابط إحالتك وأتم الشروط وتمت الموافقة عليه، وتم إضافة `0.025$` إلى رصيدك.")
                                break

                        save_data(data)
                        send_message(target_id, "✅ **تهانينا! تمت الموافقة على طلبك بنجاح.**\n\n💡 _لكسب الأرباح، قم بمشاركة رابط الإحالة الخاص بك ودعوة أصدقائك لإنهاء المهام._")
                        edit_message(chat_id, msg_id, msg["text"] + "\n\n📢 **النتيجة:** تمت الموافقة بنجاح ✅")
                    else:
                        data["tasks_progress"][str(target_id)] = {"step": 0, "status": "none"}
                        save_data(data)
                        send_message(target_id, "❌ **عذراً، تم رفض طلبك.** يرجى التأكد من الشروط وإعادة المحاولة.")
                        edit_message(chat_id, msg_id, msg["text"] + "\n\n📢 **النتيجة:** تم الرفض ❌")
                    
                    answer_callback(cq_id, "تم تنفيذ القرار بنجاح")

            elif "message" in update:
                msg = update["message"]
                if "text" not in msg:
                    continue
                
                text = msg["text"]
                chat_id = msg["chat"]["id"]
                user_id = msg["from"]["id"]
                name = msg["from"].get("first_name", "مستخدم")

                if chat_id > 0:
                    if user_id in data["admins"] and data["mode"].get(str(user_id)) == "waiting_channel":
                        data["eshterak"][text] = []
                        data["mode"][str(user_id)] = None
                        save_data(data)
                        send_message(chat_id, f"✅ تمت إضافة القناة `{text}` بنجاح لقنوات الاشتراك الإجباري (سيتم خصم 0.005$ عند مغادرتها).")
                        continue

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

                        if user_id in data["admins"]:
                            send_message(chat_id, "اهلا بك عزيزي المطور\nاليك لوحة الصانع\n⚙️ — — — — — — — — ⚙️", get_admin_keyboard())
                        else:
                            verify_token = str(int(time.time() * 1000)) + str(user_id)
                            data["verify_tokens"][verify_token] = user_id
                            save_data(data)

                            web_app_keyboard = {
                                "inline_keyboard": [
                                    [{"text": "🔒 تحقق من الجهاز للمتابعة", "web_app": {"url": f"https://smailsmail22567-design.github.io/Mini-app/?t={verify_token}"}}]
                                ]
                            }
                            send_message(chat_id, "👋 أهلاً بك! يرجى النقر على زر التحقق الأمني أدناه لبدء استخدام البوت:", web_app_keyboard)
    except Exception as e:
        print(f"Error in main loop: {e}")
        time.sleep(3)
