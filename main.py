import sys, types, qrcode, json, os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# --- Fix for Python 3.13 ---
fake_imghdr = types.ModuleType("imghdr")
def what(file, h=None): return None
fake_imghdr.what = what
sys.modules["imghdr"] = fake_imghdr

# -------------------- CONFIG --------------------
BOT_TOKEN = "7634622833:AAFNzDehovix8ThntvYrFq5SSV12l2Cr87o"
OWNER_USERNAME = "shristi_offical"
DATA_DIR = "bot_data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
QR_CODE_FILE = os.path.join(DATA_DIR, "upi_qr.png")

PAYMENT_UPI = "pt9497@ptyes"

RATE_CHART = """🍒 𝐒𝐄𝐑𝐕𝐈𝐂𝐄𝐒 

✅ 20 Nude Pics = 199₹ 
✅ 10 Nude Video = 199₹
✅ 10 my sex video = 399₹
✅ 30 nude pic + 15 video = 299₹
✅ 50 Pics + 30 Videos = 499₹

✅ 𝐅𝐮𝐥𝐥 𝐛𝐨𝐝𝐲 𝐩𝐚𝐜𝐤 😎 
50 Nude Pics + 40 Nude Videos + 30 sex video = 899₹ 

💕 𝐕𝐢𝐝𝐞𝐨 𝐂𝐚𝐥𝐥 𝐑𝐨𝐦𝐚𝐧𝐜𝐞 👣
🏪 10 min = ₹499
🏪 20 min = ₹899

💙 𝐌𝐘 𝐅𝐀𝐕𝐎𝐑𝐈𝐓𝐄 🥵
✅ 𝐒𝐄𝐗 𝐂𝐇𝐀𝐓 = ₹299 (10min + 10nude)
✅ 𝐒𝐄𝐗 𝐂𝐇𝐀𝐓 𝐖𝐈𝐓𝐇 𝐍𝐔𝐃𝐄𝐒 = ₹399 (20min)
✅ 𝐒𝐄𝐗 𝐂𝐇𝐀𝐓 𝐖𝐈𝐓𝐇 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃 𝐍𝐔𝐃𝐄𝐒 = ₹799 (30min)

𝐓𝐲𝐩𝐞 𝐨𝐟 𝐯𝐢𝐝𝐞𝐨𝐬 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 💃
❤️My 10 dildo inside Video   299₹
🔥My 10 fingering video        299₹
😍My 15 my hard sex video   499₹
😀My 15 boobs show video    499₹
💋My 15 Belowjob video       499₹

👑 VIP Group: t.me/shristie

For proof t.me/+sbGBV04UN9QwN2Q1

🕶️ Owned by @shristi_offical
"""

PAYMENT_INSTRUCTION = (
    "💰 *Payment Instructions:*\n\n"
    "Scan the QR code below or use this UPI ID:\n"
    f"`{PAYMENT_UPI}`\n\n"
    "📸 After payment, send the screenshot here for verification."
)

PAYMENT_KEYWORDS = [
    "paid", "payment", "txn", "upi", "transfer", "screenshot", "done", "txid"
]

# -------------------- Helper Functions --------------------
def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def generate_qr():
    if not os.path.exists(QR_CODE_FILE):
        qr = qrcode.make(f"upi://pay?pa={PAYMENT_UPI}&pn=Payment")
        qr.save(QR_CODE_FILE)

def load_json(path, default):
    if not os.path.exists(path): return default
    with open(path, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def looks_like_payment_message(update: Update):
    if update.message.photo or update.message.document:
        return True
    text = (update.message.text or "").lower()
    return any(kw in text for kw in PAYMENT_KEYWORDS)

# -------------------- Message Sending --------------------
def send_rate_chart(update: Update):
    update.message.reply_text(RATE_CHART)

def send_payment_qr(update: Update, context: CallbackContext):
    update.message.reply_text(PAYMENT_INSTRUCTION, parse_mode="Markdown")
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(QR_CODE_FILE, "rb"))

def forward_to_owner(update: Update, context: CallbackContext):
    owner_id = config.get("owner_id")
    if not owner_id:
        update.message.reply_text("Owner not set. Please ask the owner to run /setowner.")
        return
    try:
        context.bot.forward_message(
            chat_id=owner_id,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )
        update.message.reply_text(
            "✅ Payment proof forwarded to owner for verification.\n"
            f"Also contact: @{OWNER_USERNAME}"
        )
    except Exception as e:
        print("Forward failed:", e)
        update.message.reply_text("❌ Failed to forward to owner. Contact manually.")

# -------------------- Commands --------------------
def start(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    if chat_id not in users:
        users[chat_id] = {"step": 1}
    save_json(USERS_FILE, users)
    handle_cyclic_message(update, context)

def setowner(update: Update, context: CallbackContext):
    sender_username = update.effective_user.username or ""
    if sender_username.lower() == OWNER_USERNAME.lower():
        config["owner_id"] = update.effective_chat.id
        save_json(CONFIG_FILE, config)
        update.message.reply_text("✅ Owner saved successfully.")
    else:
        update.message.reply_text("❌ Unauthorized access.")

# -------------------- Cycle Logic --------------------
def handle_cyclic_message(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    user = users.get(chat_id, {"step": 1})
    step = user["step"]

    if step == 1:
        send_rate_chart(update)
        user["step"] = 2
    elif step == 2:
        send_payment_qr(update, context)
        user["step"] = 3
    elif step == 3:
        if looks_like_payment_message(update):
            forward_to_owner(update, context)
            user["step"] = 1
        else:
            update.message.reply_text("📸 Please send your payment proof (screenshot).")

    users[chat_id] = user
    save_json(USERS_FILE, users)

def handle_message(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    if chat_id not in users:
        users[chat_id] = {"step": 1}
        save_json(USERS_FILE, users)
    handle_cyclic_message(update, context)

# -------------------- Main --------------------
def main():
    ensure_data_dir()
    generate_qr()

    global users, config
    users = load_json(USERS_FILE, {})
    config = load_json(CONFIG_FILE, {})

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setowner", setowner))
    dp.add_handler(MessageHandler(Filters.all & (~Filters.command), handle_message))

    print("🚀 Bot started successfully.")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
