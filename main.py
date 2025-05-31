import random
import asyncio
from telegram.ext import MessageHandler, filters
import time

# Waifu list (tum baad me isme aur add kar sakte ho)
waifus = [
    "Rem", "Emilia", "Zero Two", "Asuna", "Hinata", "Rias Gremory", "Kurumi Tokisaki", "Mikasa", "Nezuko", "Mai Sakurajima"
]

# Mode and timers
spawn_mode = "time"  # "time" or "message"
spawn_interval = 120  # seconds (2 minutes)
message_count_target = 100
current_message_count = 0
last_spawn_time = 0
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
