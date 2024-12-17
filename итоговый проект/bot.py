import telebot
import sqlite3
import json
from telebot import types

# Инициализация бота
TOKEN = '7253770972:AAEQuLU7BnlO-01FFmrIWG1es4FQYNjhh2U'
bot = telebot.TeleBot(TOKEN)

# Загрузка часто задаваемых вопросов из JSON
def load_faq():
    with open('faq.json', 'r', encoding='utf-8') as f:
        return json.load(f)

faq_data = load_faq()

# Подключение к базе данных
conn = sqlite3.connect('support.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы для хранения запросов
cursor.execute('''CREATE TABLE IF NOT EXISTS user_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    message TEXT,
    response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_message = message.text.lower()

    # Проверка на наличие ответа в FAQ
    response = faq_data.get(user_message)
    if response:
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "К сожалению, я не могу ответить на этот вопрос. Ваш запрос передан специалисту.")
        save_request(user_id, username, user_message, "Передан специалисту")

# Функция сохранения запросов в базу данных
def save_request(user_id, username, message, response):
    cursor.execute("INSERT INTO user_requests (user_id, username, message, response) VALUES (?, ?, ?, ?)",
                   (user_id, username, message, response))
    conn.commit()

# Кнопки для интерфейса
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Частые вопросы")
    btn2 = types.KeyboardButton("Связаться со специалистом")
    markup.add(btn1, btn2)
    bot.reply_to(message, "Добро пожаловать! Выберите опцию:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Частые вопросы")
def send_faq(message):
    faq_list = "\n".join([f"- {q}" for q in faq_data.keys()])
    bot.reply_to(message, f"Вот список частых вопросов:\n{faq_list}")

@bot.message_handler(func=lambda message: message.text == "Связаться со специалистом")
def contact_specialist(message):
    bot.reply_to(message, "Пожалуйста, напишите ваш вопрос, и он будет передан специалисту.")

# Запуск бота
bot.polling(none_stop=True)
