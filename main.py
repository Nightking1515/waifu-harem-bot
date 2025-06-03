import logging
import random
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Dictionary to track each user's game state
user_games = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    number = random.randint(1, 100)
    user_games[user_id] = {'number': number, 'tries': 0}
    await update.message.reply_text(
        "🎯 I’ve picked a number between 1 and 100. Can you guess it? Send your guess!"
    )

# /giveup command
async def giveup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_games:
        answer = user_games[user_id]['number']
        del user_games[user_id]
        await update.message.reply_text(f"😅 The number was {answer}. Game over!")
    else:
        await update.message.reply_text("You haven’t started a game yet. Use /start")

# Handling guesses
async def handle_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_games:
        await update.message.reply_text("Please start a game using /start")
        return

    if not text.isdigit():
        await update.message.reply_text("Please send a valid number.")
        return

    guess = int(text)
    game = user_games[user_id]
    game['tries'] += 1

    if guess < game['number']:
        await update.message.reply_text("📉 Too low! Try again.")
    elif guess > game['number']:
        await update.message.reply_text("📈 Too high! Try again.")
    else:
        await update.message.reply_text(
            f"🎉 Correct! You guessed it in {game['tries']} tries!"
        )
        del user_games[user_id]

# Create and run bot
app = ApplicationBuilder().token("7692706456:AAEB7jphJNSOpbBl7bzxSnausRZ01viIEbY").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("giveup", giveup))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guess))

# Run directly without asyncio.run()
if __name__ == '__main__':
    app.run_polling()
