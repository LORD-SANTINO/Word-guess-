import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Word list
words = ['python', 'coding', 'snake', 'death', 'blood', 'happy' 'ocean', 'crane', 'paint', 'music']

# Store active games per user
games = {}

def new_game():
    word = random.choice(words)
    return {
        "word": word,
        "guessed": ["_"] * len(word),
        "attempts": 6
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    games[user_id] = new_game()
    await update.message.reply_text("🎮 Word Guessing Game Started!\nGuess one letter at a time.")
    await show_word(update, user_id)

async def show_word(update: Update, user_id):
    game = games[user_id]
    word_display = " ".join(game["guessed"])
    await update.message.reply_text(f"Word: {word_display}\nAttempts left: {game['attempts']}")

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in games:
        await update.message.reply_text("Type /start to begin a new game 🎯")
        return

    game = games[user_id]
    letter = update.message.text.lower()

    # Validate single letter
    if len(letter) != 1 or not letter.isalpha():
        await update.message.reply_text("⚠️ Please guess a single letter (a-z).")
        return

    if letter in game["word"]:
        for i, char in enumerate(game["word"]):
            if char == letter:
                game["guessed"][i] = letter
    else:
        game["attempts"] -= 1
        await update.message.reply_text(f"❌ Wrong! Attempts left: {game['attempts']}")

    # Check win/lose
    if "_" not in game["guessed"]:
        await update.message.reply_text(f"🎉 You won! The word was '{game['word']}'.")
        del games[user_id]
    elif game["attempts"] <= 0:
        await update.message.reply_text(f"💀 You lost! The word was '{game['word']}'.")
        del games[user_id]
    else:
        await show_word(update, user_id)

def main():
    app = Application.builder().token("8404374100:AAGQEvGMMerNmy5hXoKx0GmrC54LgqP4dD0").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess))

    app.run_polling()

if __name__ == "__main__":
    main()
