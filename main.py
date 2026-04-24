import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Замените 'YOUR_TOKEN' на токен вашего бота
TOKEN = '8757617326:AAEdd880agjWm894vXHe8Zv-6BbS4fMJ-yQ'
OWNER_ID = '6066824309'  # Замените на ID владельца бота

# Список рандомных фраз для ответа


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет, это бот желтого чата, здесь ты можешь рассказать о своих проблемах, поделиться своими секретами или просто пожаловаться. А так же предложить свои идеи. Бот полностью анонимный :))\n\n<blockquote><i>Создано с помощью @ReFatherBot</i></blockquote>",
        parse_mode='HTML'
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Получаем имя пользователя
        username = update.message.from_user.username or "Без имени"
        user_id = update.message.from_user.id
        message_text = update.message.text

        # Формируем сообщение для владельца
        owner_message = f"@{username} (ID: {user_id}): {message_text}"
        await context.bot.send_message(chat_id=OWNER_ID, text=owner_message)

        # Отвечаем пользователю в том же чате
        reply_message = await update.message.reply_text("✅ Сообщение успешно отправлено")

        # Ждем 2 секунды и удаляем сообщение
        await asyncio.sleep(2)
        await context.bot.delete_message(chat_id=reply_message.chat.id, message_id=reply_message.message_id)


    except Exception as e:
        logger.error(f"Ошибка в обработке сообщения: {e}")

def main() -> None:
    # Создаем приложение и передаем ему токен бота
    application = ApplicationBuilder().token(TOKEN).build()

    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
