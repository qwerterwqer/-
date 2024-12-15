import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка часто задаваемых вопросов
def load_faqs():
    with open('faqs.json', 'r', encoding='utf-8') as f:
        return json.load(f)

faqs = load_faqs()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Добро пожаловать в службу технической поддержки!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()  # Приведение к нижнему регистру
    
    # Поиск ответа на вопрос
    response = faqs.get(user_message)
    if response:
        await update.message.reply_text(response)
    else:
        await update.message.reply_text('Извините, я не знаю ответа на этот вопрос.')

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Обработка голосовых сообщений (простой ответ, можно расширить)
    await update.message.reply_text('Я не могу обработать голосовые сообщения, только текстовые.')

if __name__ == '__main__':
    application = ApplicationBuilder().token('7253770972:AAExz7-vPlqmvP6hGf2zCTIMHV4ACHG9g1s').build() 

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Text,filters.Command, handle_message))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))  # Обработка голосовых сообщений

    # Запуск бота
    application.run_polling()
