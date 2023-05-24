import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import random

TOKEN = "YOUR_TOKEN_HERE"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

#creating a "database"
users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    #adding a user to the database if it is not found there
    if user.id not in users:
        users[user.id] = {'Орел': 0, 'Решка': 0}

    await update.message.reply_html(
        rf"Привітик {user.mention_html()}! 😁"
        "\nЯ знаю лише дві команди: 🪙/coin та 📃/stats")


async def coin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Flip a coin when the command /coin is issued."""
    coin = random.choice(['Орел', 'Решка'])
    user = update.effective_user

    #adding the flip result for user
    users[user.id][coin] += 1

    await update.message.reply_text(coin)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show flip statistics when the command /stats is issued."""
    user = update.effective_user

    #getting the flips for the user
    for k, v in users[user.id].items():
        if k == "Орел":
            heads = v
        elif k == "Решка":
            tails = v

    await update.message.reply_text(
        "Статистика 🪙 кидків\n"
        rf"🪙 Орлів: {heads}" "\n"
        rf"🪙 Решок: {tails}" "\n"
        rf"🪙 Всього кидків: {heads + tails}"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text("Я тебе не розумію 😢 /start")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("coin", coin))
    application.add_handler(CommandHandler("stats", stats))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()