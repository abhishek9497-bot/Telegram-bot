from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8588021900:AAGcQjK4BOL2b7UaoYlKEwzlEkY8MX-KBpQ"

QR_IMAGE_URL = "https://yourlink.com/qr.png"

KEYWORDS = [
    "qr", "qr code", "scanner",
    "scanner for payment", "payment", "upi", "pay"
]

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        text = update.message.text.lower()

        if any(word in text for word in KEYWORDS):
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=QR_IMAGE_URL,
                caption="📲 Payment ke liye QR scan karo\n\n✅ Pay and send screenshot"
            )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

print("Bot running...")
app.run_polling()
