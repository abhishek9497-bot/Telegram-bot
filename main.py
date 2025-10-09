# Telegram-bot

# Temporary fix for python-telegram-bot on Python 3.13 (imghdr removed)
import sys, types
fake_imghdr = types.ModuleType("imghdr")
def what(file, h=None):
    return None
fake_imghdr.what = what
sys.modules["imghdr"] = fake_imghdr


"""
Telegram Payment-forwarding Bot for Android (PyDroid3)
Uses python-telegram-bot v13.15 (synchronous, Updater/Dispatcher)
Author: (you)
"""

import json
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# -------------------- CONFIG: Replace these before running --------------------
BOT_TOKEN = "7634622833:AAG3Y_MnSANKnlN3E2GBf2XCQ49kMBefR-0"   # <-- Replace with token from @BotFather
OWNER_USERNAME = "shristi_offical"  # <-- WITHOUT the leading @, e.g. "Abhishek123"
DATA_DIR = "bot_data"   # directory to store JSONs
USERS_FILE = os.path.join(DATA_DIR, "users.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
# ------------------------------------------------------------------------------

# Default payment instruction (change if you want)
PAYMENT_INSTRUCTION = (
    "If you want any service, please make the payment to this UPI ID: pt9497@ptyes "
    "and send the payment screenshot here."
)

WELCOME_MESSAGE = (
    "Welcome! 👋\n\n"
    "Thank you for contacting our shop. Below is our rate chart:\n"
    "— *Replace this with your actual rate chart text later*\n\n"
    "Send me a message if you're interested."
)

# Keywords to auto-detect payment messages (lowercase)
PAYMENT_KEYWORDS = [
    "paid", "payment", "txn", "upi", "transfer", "transfered", "transfered",
    "screenshot", "txid", "tx", "paid to", "done"
]

# -------------------- Helper functions for storage --------------------
def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

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
        json.dump(data, f, indent=2, ensure_ascii=False)

# -------------------- Load/create storage files --------------------
ensure_data_dir()
users = load_json(USERS_FILE, {})    # structure: { "<chat_id>": {"first_seen": "YYYY-MM-DD", ...} }
config = load_json(CONFIG_FILE, {})  # structure: { "owner_id": 123456789 }

# -------------------- Utility: detect payment-like message --------------------
def looks_like_payment_message(update: Update) -> bool:
    # Photo or document => likely a screenshot
    if update.message.photo or update.message.document:
        return True
    # Text containing payment keywords
    text = (update.message.text or "").lower()
    for kw in PAYMENT_KEYWORDS:
        if kw in text:
            return True
    return False

# -------------------- Command: /start --------------------
def start(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    if chat_id not in users:
        # First time user
        users[chat_id] = {"first_seen": update.message.date.isoformat()}
        save_json(USERS_FILE, users)

        # Send welcome + rate chart
        update.message.reply_text(WELCOME_MESSAGE, parse_mode="Markdown")
    else:
        # Returning user -> give payment instruction
        update.message.reply_text(PAYMENT_INSTRUCTION)

# -------------------- Command: /setowner --------------------
def setowner(update: Update, context: CallbackContext):
    """
    This command sets the owner chat id automatically, but it only works if the
    Telegram username of the person issuing this command matches OWNER_USERNAME
    you put in the config above. This prevents others from hijacking.
    """
    sender_username = update.effective_user.username or ""
    if sender_username.lower() == OWNER_USERNAME.lower():
        owner_id = update.effective_chat.id
        config["owner_id"] = owner_id
        save_json(CONFIG_FILE, config)
        update.message.reply_text(f"✅ Owner saved. Owner chat id = {owner_id}")
        print("Owner set to", owner_id)
    else:
        update.message.reply_text("❌ You are not authorized to set owner. Username mismatch.")

# -------------------- Command: /whoami (optional) --------------------
def whoami(update: Update, context: CallbackContext):
    update.message.reply_text(f"Your chat id is: {update.effective_chat.id}\nYour username: @{update.effective_user.username}")

# -------------------- Generic message handler --------------------
def handle_message(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    # If first time contact (no /start), treat similarly:
    if chat_id not in users:
        users[chat_id] = {"first_seen": update.message.date.isoformat()}
        save_json(USERS_FILE, users)
        update.message.reply_text(WELCOME_MESSAGE, parse_mode="Markdown")
        return

    # If message looks like payment evidence (photo/document or payment text)
    if looks_like_payment_message(update):
        # Grab owner id from config
        owner_id = config.get("owner_id")
        if not owner_id:
            update.message.reply_text(
                "Thanks — I received your message. But owner chat id is not set yet. "
                "Please ask the owner to run /setowner in this bot (owner uses their account)."
            )
            return

        # Forward the actual message (photo/text/document) to owner
        try:
            context.bot.forward_message(
                chat_id=owner_id,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.message_id
            )
            update.message.reply_text("✅ Thank you. Your payment evidence has been forwarded for verification   so please share the screenshot of payment here 👉 @shristi_offical.")
        except Exception as e:
            update.message.reply_text("❌ Failed to forward to owner. Please contact owner directly owner user id : @shristi_offical.")
            print("Forward failed:", e)
        return

    # Default: ask to pay (second message and onward)
    update.message.reply_text(PAYMENT_INSTRUCTION)

# -------------------- Main: run the bot --------------------
def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("ERROR: Please set BOT_TOKEN in the code.")
        return

    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setowner", setowner))
    dp.add_handler(CommandHandler("whoami", whoami))

    # Message handler for all text/photos/documents
    dp.add_handler(MessageHandler(Filters.all & (~Filters.command), handle_message))

    print("Bot started. Press Ctrl+C to stop.")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
