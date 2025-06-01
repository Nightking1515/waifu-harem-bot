import random
import time
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# List of Waifus and Bald characters
characters = [
    {
        "name": "Rem",
        "image": "https://i.imgur.com/u8fFZQy.jpeg"
    },
    {
        "name": "Emilia",
        "image": "https://i.imgur.com/fSuhzG8.jpeg"
    },
    {
        "name": "Zero Two",
        "image": "https://i.imgur.com/8cvZyKR.jpeg"
    },
    {
        "name": "Saitama",
        "image": "https://i.imgur.com/3fJ1P48.jpeg"
    },
    {
        "name": "Krillin",
        "image": "https://i.imgur.com/2fJ1P48.jpeg"
    }
]

# Spawn mode and timer settings
spawn_mode = "time"  # "time" or "message"
spawn_interval = 120  # in seconds (2 minutes)
message_count_target = 100
current_message_count = 0
last_spawn_time = 0

# Currently spawned character
current_character = None

# User harem data
user_harems = {}

# Telegram Bot Token
BOT_TOKEN = "7692706456:AAEB7jphJNSOpbBl7bzxSnausRZ01viIEbY"

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Hello! Waifu Harem Bot is active and ready to serve!")

# Character spawn function
async def spawn_character(context: ContextTypes.DEFAULT_TYPE, chat_id):
    global current_character
    current_character = random.choice(characters)
    context.chat_data['last_character'] = current_character
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=current_character["image"],
        caption="✨ A new character has appeared! ✨\nUse /grab to add it to your harem."
    )

# Message handler
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_message_count, spawn_mode, message_count_target, last_spawn_time

    if spawn_mode == "message":
        current_message_count += 1
        if current_message_count >= message_count_target:
            await spawn_character(context, update.effective_chat.id)
            current_message_count = 0
    elif spawn_mode == "time":
        if time.time() - last_spawn_time >= spawn_interval:
            await spawn_character(context, update.effective_chat.id)
            last_spawn_time = time.time()

# /changetime command handler
async def changetime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global spawn_mode, message_count_target
    try:
        count = int(context.args[0])
        spawn_mode = "message"
        message_count_target = count
        await update.message.reply_text(f"Auto-spawn mode set to message-based: every {count} messages.")
    except:
        await update.message.reply_text("Usage: /changetime <number>")

# /changemode command handler
async def changemode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global spawn_mode, spawn_interval
    try:
        minutes = int(context.args[0])
        spawn_mode = "time"
        spawn_interval = minutes * 60
        await update.message.reply_text(f"Auto-spawn mode set to time-based: every {minutes} minutes.")
    except:
        await update.message.reply_text("Usage: /changemode <minutes>")

# /grab command handler
async def grab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if 'last_character' in context.chat_data:
        character = context.chat_data['last_character']
        if chat_id not in user_harems:
            user_harems[chat_id] = {}
        if user_id not in user_harems[chat_id]:
            user_harems[chat_id][user_id] = []
        if character["name"] not in [c["name"] for c in user_harems[chat_id][user_id]]:
            user_harems[chat_id][user_id].append(character)
            await update.message.reply_text(f"🎉 You claimed {character['name']} to your harem!")
            del context.chat_data['last_character']
        else:
            await update.message.reply_text("❌ You already claimed this character.")
    else:
        await update.message.reply_text("⚠️ No character available to grab right now.")

# /harem command handler
async def harem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if chat_id in user_harems and user_id in user_harems[chat_id]:
        harem_list = user_harems[chat_id][user_id]
        if harem_list:
            message = "💖 Your harem:\n"
            for character in harem_list:
                message += f"- {character['name']}\n"
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("😢 Your harem is empty.")
    else:
        await update.message.reply_text("😢 Your harem is empty.")

# Build app and handlers
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("changetime", changetime))
app.add_handler(CommandHandler("changemode", changemode))
app.add_handler(CommandHandler("grab", grab))
app.add_handler(CommandHandler("harem", harem))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))

# Start the bot
app.run_polling()
