from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.environ.get("7692706456:AAEB7jphJNSOpbBl7bzxSnausRZ01viIEbY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Waifu Harem Bot is live!")

app = ApplicationBuilder().token(7692706456:AAEB7jphJNSOpbBl7bzxSnausRZ01viIEbY).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
