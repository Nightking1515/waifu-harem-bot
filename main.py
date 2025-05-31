import random
import asyncio
from telegram.ext import MessageHandler, filters
import time

# Waifu list (tum baad me isme aur add kar sakte ho)
waifus = [
    {"name": "Rem", "image": "https://i.imgur.com/u8fFZQy.jpeg"},
    {"name": "Emilia", "image": "https://i.imgur.com/fSuhzG8.jpeg"},
    {"name": "Zero Two", "image": "https://i.imgur.com/8cvZyKR.jpeg"},
    {"name": "Asuna", "image": "https://i.imgur.com/1FfQKn5.jpeg"},
    {"name": "Hinata", "image": "https://i.imgur.com/ZJ3J1Bh.jpeg"},
    {"name": "Rias Gremory", "image": "https://i.imgur.com/D6Bpx91.jpeg"},
    {"name": "Kurumi Tokisaki", "image": "https://i.imgur.com/fHK2nHL.jpeg"},
    {"name": "Mikasa", "image": "https://i.imgur.com/HZyoLKH.jpeg"},
    {"name": "Nezuko", "image": "https://i.imgur.com/0DrxwjW.jpeg"},
    {"name": "Mai Sakurajima", "image": "https://i.imgur.com/w2gMj5S.jpeg"}
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
# ✅ Waifu spawn logic
async def spawn_waifu(context: ContextTypes.DEFAULT_TYPE, chat_id):
    waifu = random.choice(waifus)
    await context.bot.send_message(chat_id=chat_id, text=f"A wild waifu appeared! ✨\nName: {waifu}\nType /grab to grab her!")

# ✅ Message count-based spawn logic
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_message_count, spawn_mode, message_count_target, last_spawn_time

    if spawn_mode == "message":
        current_message_count += 1
        if current_message_count >= message_count_target:
            await spawn_waifu(context, update.effective_chat.id)
            current_message_count = 0
    elif spawn_mode == "time":
        if time.time() - last_spawn_time >= spawn_interval:
            await spawn_waifu(context, update.effective_chat.id)
            last_spawn_time = time.time()

# ✅ Command to change to message-based mode
async def changetime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global spawn_mode, message_count_target
    try:
        count = int(context.args[0])
        spawn_mode = "message"
        message_count_target = count
        await update.message.reply_text(f"Auto-spawn mode set to message-based: every {count} messages.")
    except:
        await update.message.reply_text("Usage: /changetime <number>")

# ✅ Command to change to time-based mode
async def changemode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global spawn_mode, spawn_interval
    try:
        minutes = int(context.args[0])
        spawn_mode = "time"
        spawn_interval = minutes * 60
        await update.message.reply_text(f"Auto-spawn mode set to time-based: every {minutes} minutes.")
    except:
        await update.message.reply_text("Usage: /changemode <minutes>")
app.add_handler(CommandHandler("changetime", changetime))
app.add_handler(CommandHandler("changemode", changemode))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
claimed_waifus = {}

async def grab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Agar waifu recently spawn hui thi
    if 'last_waifu' in context.chat_data:
        waifu = context.chat_data['last_waifu']
        if chat_id not in claimed_waifus:
            claimed_waifus[chat_id] = {}
        if waifu not in claimed_waifus[chat_id]:
            claimed_waifus[chat_id][waifu] = user_id
            await update.message.reply_text(f"🎉 You claimed {waifu} successfully!")
            del context.chat_data['last_waifu']
        else:
            await update.message.reply_text("❌ Someone already claimed this waifu.")
    else:
        await update.message.reply_text("⚠️ No waifu to grab right now.")

# Update spawn_waifu function
async def spawn_waifu(context: ContextTypes.DEFAULT_TYPE, chat_id):
    waifu = random.choice(waifus)
    context.chat_data['last_waifu'] = waifu
    await context.bot.send_message(chat_id=chat_id, text=f"A wild waifu appeared! ✨\nName: {waifu}\nType /grab to grab her!")

# Add handler
app.add_handler(CommandHandler("grab", grab))
app.run_polling()
