import sys, types
import json
import os
from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

Temporary fix for Python 3.13 (imghdr removed)

fake_imghdr = types.ModuleType("imghdr")
def what(file, h=None):
return None
fake_imghdr.what = what
sys.modules["imghdr"] = fake_imghdr

-------------------- CONFIG --------------------

BOT_TOKEN = "7634622833:AAFNzDehovix8ThntvYrFq5SSV12l2Cr87o"  # <-- Replace with your Bot token
OWNER_USERNAME = "shristi_offical"
DATA_DIR = "bot_data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

RATE_CHART = """🍒 𝐒𝐄𝐑𝐕𝐈𝐂𝐄𝐒

✅20 Nude Pics = 199₹
✅10 Nude Video = 199₹
✅10 my sex video = 399₹
✅30 nude pic + 15 video = 299₹
✅50 Pics + 30 Videos = 499₹

✅ Full body exposure pack 😎 : 50 Nude Pics + 40 Nude Videos + 30 sex video = 899₹

💕 Video Call Romance 👣
🏪10 minutes = ₹499
🏪20 minutes = ₹899

💙MY FAVORITE 🥵
✅SEX CHAT = 299₹(10min+10nude)
✅SEX CHAT WITH NUDES = 399₹ (20min)
😀SEX CHAT WITH UNLIMITED NUDES = ₹799 (30 min)

📸 Type of videos you want 💃
❤️My 10 dildo inside Video   299₹
🔥My 10 fingering video        299₹
😍My 15 my hard sex video   499₹
😀My 15 boobs show video    499₹
💋My 15 Belowjob video       499₹

👑Vip Group: t.me/shristie

"""

CHANNEL_LINK = "https://t.me/+sbGBV04UN9QwN2Q1"  # Proof channel
BRANDING = "\n\n🕶️ Powered Isse pure code me vo line replace karke do

import sys, types
import json
import os
from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

Temporary fix for Python 3.13 (imghdr removed)

fake_imghdr = types.ModuleType("imghdr")
def what(file, h=None):
return None
fake_imghdr.what = what
sys.modules["imghdr"] = fake_imghdr

-------------------- CONFIG --------------------

BOT_TOKEN = "7634622833:AAFNzDehovix8ThntvYrFq5SSV12l2Cr87o"  # <-- Replace with your Bot token
OWNER_USERNAME = "shristi_offical"
DATA_DIR = "bot_data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

RATE_CHART = """🍒 𝐒𝐄𝐑𝐕𝐈𝐂𝐄𝐒

✅20 Nude Pics = 199₹
✅10 Nude Video = 199₹
✅10 my sex video = 399₹
✅30 nude pic + 15 video = 299₹
✅50 Pics + 30 Videos = 499₹

✅ Full body exposure pack 😎 : 50 Nude Pics + 40 Nude Videos + 30 sex video = 899₹

💕 Video Call Romance 👣
🏪10 minutes = ₹499
🏪20 minutes = ₹899

💙MY FAVORITE 🥵
✅SEX CHAT = 299₹(10min+10nude)
✅SEX CHAT WITH NUDES = 399₹ (20min)
😀SEX CHAT WITH UNLIMITED NUDES = ₹799 (30 min)

📸 Type of videos you want 💃
❤️My 10 dildo inside Video   299₹
🔥My 10 fingering video        299₹
😍My 15 my hard sex video   499₹
😀My 15 boobs show video    499₹
💋My 15 Belowjob video       499₹

👑Vip Group: t.me/shristie

"""

CHANNEL_LINK = "https://t.me/+sbGBV04UN9QwN2Q1"  # Proof channel
BRANDING = "\n\n🕶️ Powered by @shristi_offical"  # Small branding footer

PAYMENT_UPI = "pt9497@ptyes"
PAYMENT_INSTRUCTION_TEXT = f"Click the UPI ID to copy and send payment screenshot:\n{PAYMENT_UPI}"

PAYMENT_KEYWORDS = [
"paid", "payment", "txn", "upi", "transfer", "transfered",
"screenshot", "txid", "tx", "paid to", "done"
]

-------------------- Helper functions --------------------

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

def send_typing(update, context):
context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

def looks_like_payment_message(update: Update) -> bool:
if update.message.photo or update.message.document:
return True
text = (update.message.text or "").lower()
for kw in PAYMENT_KEYWORDS:
if kw in text:
return True
return False

-------------------- Messages --------------------

def send_rate_chart(update: Update, context: CallbackContext):
send_typing(update, context)
update.message.reply_text(RATE_CHART + f"\nProofs here: {CHANNEL_LINK}" + BRANDING)

def send_payment_instruction(update: Update):
update.message.reply_text(PAYMENT_INSTRUCTION_TEXT + BRANDING)

def forward_to_owner(update: Update, context: CallbackContext):
owner_id = config.get("owner_id")
if not owner_id:
update.message.reply_text("Owner not set. Please ask owner to run /setowner.")
return
try:
context.bot.forward_message(chat_id=owner_id,
from_chat_id=update.effective_chat.id,
message_id=update.message.message_id)
update.message.reply_text(f"✅ Payment evidence forwarded to owner for verification.Also Contact Me: @{OWNER_USERNAME}" + BRANDING)
except Exception as e:
update.message.reply_text("❌ Failed to forward to owner. Contact owner directly.")
print("Forward failed:", e)

-------------------- Command Handlers --------------------

def start(update: Update, context: CallbackContext):
chat_id = str(update.effective_chat.id)
if chat_id not in users:
users[chat_id] = {"step": 1}
save_json(USERS_FILE, users)
send_rate_chart(update, context)
else:
handle_cyclic_message(update, context)

def setowner(update: Update, context: CallbackContext):
sender_username = update.effective_user.username or ""
if sender_username.lower() == OWNER_USERNAME.lower():
owner_id = update.effective_chat.id
config["owner_id"] = owner_id
save_json(CONFIG_FILE, config)
update.message.reply_text(f"✅ Owner saved. Owner chat id = {owner_id}")
else:
update.message.reply_text("❌ You are not authorized to set owner.")

def handle_cyclic_message(update: Update, context: CallbackContext):
chat_id = str(update.effective_chat.id)
user = users.get(chat_id, {"step": 1})
step = user.get("step", 1)

# Step 1: Rate chart  
if step == 1:  
    send_rate_chart(update, context)  
    users[chat_id]["step"] = 2  

# Step 2: Payment instruction  
elif step == 2:  
    send_payment_instruction(update)  
    users[chat_id]["step"] = 3  

# Step 3: Forward payment proof  
elif step == 3:  
    if looks_like_payment_message(update):  
        forward_to_owner(update, context)  
    else:  
        update.message.reply_text("Please send your payment proof (text/photo).")  
        return  
    users[chat_id]["step"] = 1  # reset cycle  

save_json(USERS_FILE, users)

def handle_message(update: Update, context: CallbackContext):
chat_id = str(update.effective_chat.id)
if chat_id not in users:
users[chat_id] = {"step": 1}
save_json(USERS_FILE, users)
handle_cyclic_message(update, context)

-------------------- Main --------------------

def main():
if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
print("ERROR: Please set BOT_TOKEN in the code.")
return

ensure_data_dir()  
global users, config  
users = load_json(USERS_FILE, {})  
config = load_json(CONFIG_FILE, {})  

updater = Updater(token=BOT_TOKEN, use_context=True)  
dp = updater.dispatcher  

dp.add_handler(CommandHandler("start", start))  
dp.add_handler(CommandHandler("setowner", setowner))  
dp.add_handler(MessageHandler(Filters.all & (~Filters.command), handle_message))  

print("Bot started. Press Ctrl+C to stop.")  
updater.start_polling()  
updater.idle()

if name == "main":
main()

 @shristi_offical"  # Small branding footer

PAYMENT_UPI = "pt9497@ptyes"
PAYMENT_INSTRUCTION_TEXT = f"Click the UPI ID to copy and send payment screenshot:\n{PAYMENT_UPI}"

PAYMENT_KEYWORDS = [
"paid", "payment", "txn", "upi", "transfer", "transfered",
"screenshot", "txid", "tx", "paid to", "done"
]

-------------------- Helper functions --------------------

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

def send_typing(update, context):
context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

def looks_like_payment_message(update: Update) -> bool:
if update.message.photo or update.message.document:
return True
text = (update.message.text or "").lower()
for kw in PAYMENT_KEYWORDS:
if kw in text:
return True
return False

-------------------- Messages --------------------

def send_rate_chart(update: Update, context: CallbackContext):
send_typing(update, context)
update.message.reply_text(RATE_CHART + f"\nProofs here: {CHANNEL_LINK}" + BRANDING)

def send_payment_instruction(update: Update):
update.message.reply_text(PAYMENT_INSTRUCTION_TEXT + BRANDING)

def forward_to_owner(update: Update, context: CallbackContext):
owner_id = config.get("owner_id")
if not owner_id:
update.message.reply_text("Owner not set. Please ask owner to run /setowner.")
return
try:
context.bot.forward_message(chat_id=owner_id,
from_chat_id=update.effective_chat.id,
message_id=update.message.message_id)
update.message.reply_text(f"✅ Payment evidence forwarded to owner for verification.Also Contact Me: @{OWNER_USERNAME}" + BRANDING)
except Exception as e:
update.message.reply_text("❌ Failed to forward to owner. Contact owner directly.")
print("Forward failed:", e)

-------------------- Command Handlers --------------------

def start(update: Update, context: CallbackContext):
chat_id = str(update.effective_chat.id)
if chat_id not in users:
users[chat_id] = {"step": 1}
save_json(USERS_FILE, users)
send_rate_chart(update, context)
else:
handle_cyclic_message(update, context)

def setowner(update: Update, context: CallbackContext):
sender_username = update.effective_user.username or ""
if sender_username.lower() == OWNER_USERNAME.lower():
owner_id = update.effective_chat.id
config["owner_id"] = owner_id
save_json(CONFIG_FILE, config)
update.message.reply_text(f"✅ Owner saved. Owner chat id = {owner_id}")
else:
update.message.reply_text("❌ You are not authorized to set owner.")

def handle_cyclic_message(update: Update, context: CallbackContext):
chat_id = str(update.effective_chat.id)
user = users.get(chat_id, {"step": 1})
step = user.get("step", 1)

# Step 1: Rate chart  
if step == 1:  
    send_rate_chart(update, context)  
    users[chat_id]["step"] = 2  

# Step 2: Payment instruction  
elif step == 2:  
    send_payment_instruction(update)  
    users[chat_id]["step"] = 3  

# Step 3: Forward payment proof  
elif step == 3:  
    if looks_like_payment_message(update):  
        forward_to_owner(update, context)  
    else:  
        update.message.reply_text("Please send your payment proof (text/photo).")  
        return  
    users[chat_id]["step"] = 1  # reset cycle  

save_json(USERS_FILE, users)

def handle_message(update: Update, context: CallbackContext):
chat_id = str(update.effective_chat.id)
if chat_id not in users:
users[chat_id] = {"step": 1}
save_json(USERS_FILE, users)
handle_cyclic_message(update, context)

-------------------- Main --------------------

def main():
if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
print("ERROR: Please set BOT_TOKEN in the code.")
return

ensure_data_dir()  
global users, config  
users = load_json(USERS_FILE, {})  
config = load_json(CONFIG_FILE, {})  

updater = Updater(token=BOT_TOKEN, use_context=True)  
dp = updater.dispatcher  

dp.add_handler(CommandHandler("start", start))  
dp.add_handler(CommandHandler("setowner", setowner))  
dp.add_handler(MessageHandler(Filters.all & (~Filters.command), handle_message))  

print("Bot started. Press Ctrl+C to stop.")  
updater.start_polling()  
updater.idle()

if name == "main":
main() 
