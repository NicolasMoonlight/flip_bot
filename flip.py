import logging, random
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
from config import TOKEN, create_new_user, check_user, set_user_values, get_stats_user

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# translation of words to display to the user
mapping = {
    'heads': 'Орел',
    'tails': 'Решка'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    #adding a user to the database if it is not found there
    if not check_user(user.id):
        create_new_user(user.id)

    await update.message.reply_html(
        rf"Привітик {user.mention_html()}! 😁"
        "\nЯ знаю лише дві команди: 🪙/coin та 📃/stats")


async def coin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Flip a coin when the command /coin is issued."""
    coin = random.choice(['heads', 'tails'])
    user = update.effective_user

    set_user_values(user.id, coin)

    await update.message.reply_text(
        "Випадає..  " + mapping.get(coin)
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show flip statistics when the command /stats is issued."""
    user = update.effective_user

    heads, tails = get_stats_user(user.id)

    await update.message.reply_text(
        "Статистика 🪙 кидків\n"
        rf"🪙 Орлів: {heads}" "\n"
        rf"🪙 Решок: {tails}" "\n"
        rf"🪙 Всього кидків: {int(heads) + int(tails)}"
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