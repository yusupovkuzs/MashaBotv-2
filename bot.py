import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Replace with your bot token and server URL
BOT_TOKEN = "7503889932:AAEDqiX5NjRHeT4lIAIkwRyhLdt0lDB6O0s"
SERVER_URL = "https://your-server-url.com/api"


# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Отправьте мне вопрос, и я постараюсь найти ответ.")


# Function to handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_question = update.message.text
    chat_id = update.message.chat_id

    try:
        # Send HTTP request to the external server
        response = requests.post(SERVER_URL, json={"question": user_question})
        response.raise_for_status()

        # Extract the server's answer
        server_answer = response.json().get("answer", "Не удалось получить ответ.")
    except Exception as e:
        logging.error(f"Ошибка при запросе к серверу: {e}")
        server_answer = "Произошла ошибка при обработке вашего запроса."

    # Send the server's answer back to the user
    await context.bot.send_message(chat_id=chat_id, text=server_answer)


# Main function to start the bot
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling for updates
    application.run_polling()


if __name__ == "__main__":
    main()
