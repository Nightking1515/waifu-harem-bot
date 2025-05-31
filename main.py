from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Telegram Bot Token (testing ke liye direct likh rahe hain)
BOT_TOKEN = "7692706456:AAEB7jphJNSOpbBl7bzxSnausRZ01viIEbY"

# /start command ka handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Hello! Waifu Harem Bot is live and ready to serve waifus!")

# Bot application banana
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

# Bot ko chalu karna
app.run_polling()
