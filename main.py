import sys, types
import time
from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json, os

# -------- Fix imghdr issue --------
fake_imghdr = types.ModuleType("imghdr")
def what(file, h=None): return None
fake_imghdr.what = what
sys.modules["imghdr"] = fake_imghdr

# -------- CONFIG --------
BOT_TOKEN = "7634622833:AAFNzDehovix8ThntvYrFq5SSV12l2Cr87o"
OWNER_USERNAME = "shristi_offical"
CHANNEL_LINK = "https://t.me/shristie"
PAYMENT_UPI = "pt9497@ptyes"

DATA_DIR = "bot_data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

PAYMENT_KEYWORDS = ["paid","payment","txn","upi","transfer","screenshot","txid","done"]

RATE_CHART = f"""🍒 𝐒𝐄𝐑𝐕𝐈𝐂𝐄𝐒 

✅20 Nude Pics = 199₹ 
✅10 Nude Video = 199₹
✅10 my sex video = 399₹
✅30 nude pic + 15 video = 299₹
✅50 Pics + 30 Videos = 499₹

✅ 𝐅𝐮𝐥𝐥 𝐛𝐨𝐝𝐲 𝐞𝐱𝐩𝐨𝐬𝐮𝐫𝐞 𝐩𝐚𝐜𝐤 😎 : 50 Nude Pics + 40 Nude Videos + 30 sex video = 899₹ 

💕 𝐕𝐢𝐝𝐞𝐨 𝐂𝐚𝐥𝐥 𝐑𝐨𝐦𝐚𝐧𝐜𝐞 👣
🏪10 minutes = ₹499
🏪20 minutes = ₹899

💙𝐌𝐘 𝐅𝐀𝐕𝐎𝐑𝐈𝐓𝐄 🥵
✅𝐒𝐄𝐗 𝐂𝐇𝐀𝐓 = 299₹(10min+10nude)
✅𝐒𝐄𝐗 𝐂𝐇𝐀𝐓 𝐖𝐈𝐓𝐇 𝐍𝐔𝐃𝐄𝐒 = 399₹ (20min)
😀𝐒𝐄𝐗 𝐂𝐇𝐀𝐓 𝐖𝐈𝐓𝐇 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃 𝐍𝐔𝐃𝐄𝐒 = ₹799 (30 min)

👑Vip Group: t.me/shristie

🔈𝐍𝐎𝐓𝐄 :-
If you don't trust me, you may leave!
✅ NO REAL MEET ✅
"""

BRANDING = "\n\n— Powered by @shristi_offical 💎"

# -------- Helpers --------
def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_json(path, default):
    if not os.path.exists(path): return default
    with open(path, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def send_typing(update, context, duration=1.3):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    time.sleep(duration)

# -------- Message Functions --------
def send_rate_chart(update: Update, context: CallbackContext):
    send_typing(update, context)
    update.message.reply_text(RATE_CHART + f"\n\n📸 Proofs, Pics & Videos here: {CHANNEL_LINK}" + BRANDING, parse_mode="Markdown")

def send_payment_instruction(update: Update, context: CallbackContext):
    send_typing(update, context)
    msg = f"""💳 *Send Payment to UPI:*

`{PAYMENT_UPI}`

📋 *Tap and Hold to Copy UPI ID*

After payment, send screenshot here for verification 👇
""" + BRANDING
    update.message.reply_text(msg, parse_mode="Markdown")

def forward_to_owner(update: Update, context: CallbackContext):
    send_typing(update, context)
    owner_id = config.get("owner_id")
    if not owner_id:
        update.message.reply_text("❌ Owner not set. Run /setowner" + BRANDING)
        return
    try:
        context.bot.forward_message(chat_id=owner_id, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
        update.message.reply_text(f"✅ Payment proof sent to owner.\nContact: @{OWNER_USERNAME}" + BRANDING)
    except Exception as e:
        update.message.reply_text("❌ Could not forward payment proof." + BRANDING)
        print("Forward failed:", e)

# -------- Commands --------
def start(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    if chat_id not in users:
        users[chat_id] = {"step": 1}
        save_json(USERS_FILE, users)
        send_rate_chart(update, context)
    else:
        handle_cycle(update, context)

def setowner(update: Update, context: CallbackContext):
    sender_username = update.effective_user.username or ""
    if sender_username.lower() == OWNER_USERNAME.lower():
        config["owner_id"] = update.effective_chat.id
        save_json(CONFIG_FILE, config)
        update.message.reply_text("✅ Owner saved successfully!" + BRANDING)
    else:
        update.message.reply_text("❌ Not authorized to set owner." + BRANDING)

# -------- Message Flow --------
def looks_like_payment_message(update: Update):
    if update.message.photo or update.message.document:
        return True
    text = (update.message.text or "").lower()
    return any(kw in text for kw in PAYMENT_KEYWORDS)

def handle_cycle(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    user = users.get(chat_id, {"step": 1})
    step = user.get("step", 1)

    if step == 1:
        send_rate_chart(update, context)
        users[chat_id]["step"] = 2
    elif step == 2:
        send_payment_instruction(update, context)
        users[chat_id]["step"] = 3
    elif step == 3:
        if looks_like_payment_message(update):
            forward_to_owner(update, context)
        else:
            update.message.reply_text("📤 Please send your payment proof (screenshot or text)." + BRANDING)
            return
        users[chat_id]["step"] = 1

    save_json(USERS_FILE, users)

def handle_message(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    if chat_id not in users:
        users[chat_id] = {"step": 1}
    save_json(USERS_FILE, users)
    handle_cycle(update, context)

# -------- Main --------
ensure_data_dir()
users = load_json(USERS_FILE, {})
config = load_json(CONFIG_FILE, {})

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setowner", setowner))
    dp.add_handler(MessageHandler(Filters.all & (~Filters.command), handle_message))

    print("🤖 Bot Running Smoothly 24/7...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
