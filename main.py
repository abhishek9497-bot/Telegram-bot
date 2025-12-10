import sys, types, qrcode, json, os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# --- Fix for Python 3.13 ---
fake_imghdr = types.ModuleType("imghdr")
def what(file, h=None): return None
fake_imghdr.what = what
sys.modules["imghdr"] = fake_imghdr

# -------------------- CONFIG --------------------
BOT_TOKEN = "8435196961:AAHsJI-a09w8p8rXKBdPPv2psW-fJf7IzWs"
OWNER_USERNAME = "Sexy_Kashishh"
DATA_DIR = "bot_data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
QR_CODE_FILE = os.path.join(DATA_DIR, "upi_qr.png")

PAYMENT_UPI = "pt9497@ptyes"

RATE_CHART = """✅20 nude pics = 199₹
50 Nude Pics = 299₹ 
✅10 Nude Video = 299₹
✅10 my sex video = 399₹
✅50 Pics + 10 Videos = 499₹

💌 𝐅𝐮𝐥𝐥 𝐛𝐨𝐝𝐲 𝐞𝐱𝐩𝐨𝐬𝐮𝐫𝐞 𝐩𝐚𝐜𝐤 😀 : 50 Nude Pics + 10 Nude Videos + 10 sex video = 899₹ 

🔥 𝐕𝐢𝐝𝐞𝐨 𝐂𝐚𝐥𝐥 𝐑𝐨𝐦𝐚𝐧𝐜𝐞 💋
😀7 minutes = ₹699
🏪10 minutes = ₹999

✨ Audio Call  ☄️
15 minutes = ₹499
30 minutes = ₹799

✅𝐒𝐄𝐗 𝐂𝐇𝐀𝐓 = 299₹ ( 10min)
✅𝐒𝐄𝐗 𝐂𝐇𝐀𝐓 𝐖𝐈𝐓𝐇 𝐍𝐔𝐃𝐄𝐒 = 399₹ ( 10min)
✅𝐒𝐄𝐗 𝐂𝐇𝐀𝐓 𝐖𝐈𝐓𝐇 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃 𝐍𝐔𝐃𝐄𝐒 = ₹999 ( 20 min 
🔴𝐍𝐎𝐓𝐄 :-
𝗜𝗳 𝘆𝗼𝘂 𝗱𝗼𝗻'𝘁 𝘁𝗿𝘂𝘀𝘁 𝗺𝗲, 𝘆𝗼𝘂 𝗺𝗮𝘆 𝗹𝗲𝗮𝘃𝗲! 

⚠️   𝙉𝙊 𝙍𝙀𝘼𝙇 𝙈𝙀𝙀𝙏  ⚠️
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
    if not os.path.exists(path): 
        return default
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def looks_like_payment_message(update: Update):
    if update.message.photo or update.message.document:
        return True
    text = (update.message.text or "").lower()
    return any(kw in text for kw in PAYMENT_KEYWORDS)

# -------------------- Sending Messages --------------------
def send_rate_chart(update: Update):
    update.message.reply_text(RATE_CHART)

def send_payment_qr(update: Update, context: CallbackContext):
    update.message.reply_text(PAYMENT_INSTRUCTION, parse_mode="Markdown")
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(QR_CODE_FILE, "rb")
    )

def forward_to_owner(update: Update, context: CallbackContext):
    owner_id = config.get("owner_id")
    if not owner_id:
        update.message.reply_text("Owner not set. Ask the owner to run /setowner.")
        return

    try:
        context.bot.forward_message(
            chat_id=owner_id,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )
        update.message.reply_text(
            "✅ Payment forwarded to the owner.\n"
            f"Contact: {OWNER_USERNAME}"
        )
    except Exception as e:
        print("Forward error:", e)
        update.message.reply_text("❌ Could not forward to owner. Contact manually.")

# -------------------- Commands --------------------
def start(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)

    # Reset flow for the user
    users[chat_id] = {"step": 1}
    save_json(USERS_FILE, users)

    update.message.reply_text("Welcome! Sending details...")
    send_rate_chart(update)
    users[chat_id]["step"] = 2
    save_json(USERS_FILE, users)

def setowner(update: Update, context: CallbackContext):
    if (update.effective_user.username or "").lower() == OWNER_USERNAME.lower():
        config["owner_id"] = update.effective_chat.id
        save_json(CONFIG_FILE, config)
        update.message.reply_text("✅ Owner saved.")
    else:
        update.message.reply_text("❌ You are not authorized.")

# -------------------- Main Logic --------------------
def handle_message(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)

    if chat_id not in users:
        users[chat_id] = {"step": 1}

    step = users[chat_id]["step"]

    # Step 1 - First message → Rate Chart
    if step == 1:
        send_rate_chart(update)
        users[chat_id]["step"] = 2

    # Step 2 - Second message → Payment Instruction + QR
    elif step == 2:
        send_payment_qr(update, context)
        users[chat_id]["step"] = 3

    # Step 3 - Waiting for screenshot
    elif step == 3:
        if looks_like_payment_message(update):
            forward_to_owner(update, context)
            users[chat_id]["step"] = 1   # Reset for future
        else:
            update.message.reply_text("📸 Please send payment screenshot.")

    save_json(USERS_FILE, users)

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

    print("🚀 Bot Running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
