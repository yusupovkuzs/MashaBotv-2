import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "7503889932:AAEDqiX5NjRHeT4lIAIkwRyhLdt0lDB6O0s"
SERVER_URL = "http://85.143.167.11:8000/ask"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Отправьте мне вопрос, и я постараюсь найти ответ.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_question = update.message.text
    chat_id = update.message.chat_id

    try:
        response = requests.post(SERVER_URL, json={"text": user_question})
        response.raise_for_status()

        server_answer = response.json().get("text", "Не удалось получить ответ.")
    except Exception as e:
        logging.error(f"Ошибка при запросе к серверу: {e}")
        server_answer = "Произошла ошибка при обработке вашего запроса."

    await context.bot.send_message(chat_id=chat_id, text=server_answer)


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == "__main__":
    main()
