import telebot
import webbrowser
from telebot import types
import os
import random
import sqlite3

TOKEN = "7413230054:AAFvZCtaepLHMtm7OtLS3hq_rp2oi0HkNQQ"

bot = telebot.TeleBot(TOKEN)

user_name = ""
user_pass = ""

@bot.message_handler(commands=["start", "go"])
def main(incoming_message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Все команды"))
    bot.send_message(incoming_message.chat.id, "Hello!", reply_markup=markup)

@bot.message_handler(commands=["help"])
def help(incoming_message):
    bot.send_message(incoming_message.chat.id, "Мы Вам обязательно поможем в скором времени!")

@bot.message_handler(commands=["site", "website"])
def open_site(incoming_message):
    webbrowser.open("https://student.skyeng.ru/home")



@bot.message_handler(content_types=['photo'])
def main(incoming_message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Удалить фото', callback_data='delete'))
    bot.reply_to(incoming_message, 'Какое красивое фото!', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)# Указывает, что функция будет вызываться всякий раз,
# когда бот получает callback-запрос (нажатие любой кнопки в чате)
# Параметр func=lambda callback: True означает, что обработчик будет срабатывать на все callback-запросы.
# Если нужно, чтобы обработчик срабатывал только на определенные запросы,
# можно задать более специфическое условие
def btn_click_handler(callback):
    if callback.data == "delete":
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
    elif callback.data == "reg":
        conn = sqlite3.connect("db.sql") # Подключение к БД (Если еще нет, будет создана)
        cur = conn.cursor()  # Создание курсора (помощник в работе с БД)
        cur.execute(
            'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
        # Создание таблицы(если еще не создана) с тремя столбцами:
        # 1) id - целочисленное автоматически-изменяющиеся значение.
        # primary key - системный столбец для идентификации пользоватеоей
        # 2) name - Имя пользователя, строковое значение, максимум 50 символов
        # 3) pass - Пароль, строковое значение, максимум 50 символов
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(callback.message.chat.id, "Сейчас мы Вас зарегистрируем. Введите ваше имя:")
        bot.register_next_step_handler(callback.message, get_name)

def get_name(incoming_message):
    global user_name
    user_name = incoming_message.text.strip()
    bot.send_message(incoming_message.chat.id, "Введите ваш пароль:")
    bot.register_next_step_handler(incoming_message, get_pass)

def get_pass(incoming_message):
    global user_pass
    user_pass = incoming_message.text.strip()
    reg_user(incoming_message)

def reg_user(incoming_message):
    conn = sqlite3.connect("db.sql")
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, pass) VALUES ("%s", "%s")' % (user_name, user_pass))  # Добавление введенных пользователем значений в БД.
    # f-строка не работает по какой-то причине, поэтому синтаксис с "%"
    # синтаксис с "%" является более старым способом форматирования строк в Python, аналогичный f-строкам.
    cur.execute('SELECT * FROM users')
    user_list = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    users = ""
    for i, a in enumerate(user_list):
        i += 1
        users += str(i) + ") " + a[1] + "\n"
    bot.send_message(incoming_message.chat.id, f"Вы успешно зарегистрировались!\nВот все наши пользователи:\n{users}")

@bot.message_handler(commands="delete")
def delete_user(incoming_message):
    conn = sqlite3.connect("db.sql")
    cur = conn.cursor()
    user_name = 'ороророророророоооооооооооооорроооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооо'
    cur.execute('DELETE FROM users WHERE name = ?', (user_name,))
    conn.commit()
    cur.close()
    conn.close()

@bot.message_handler(commands=["sites"])
def show_sites(incoming_message):
    markup = types.InlineKeyboardMarkup()  # создание маркапа (места для кнопок в ответном сообщении)
    # markup.add(types.InlineKeyboardButton("Skyeng", "https://student.skyeng.ru/home"))
    # markup.add(types.InlineKeyboardButton("Google", "https://www.google.ru/"))
    # markup.add(types.InlineKeyboardButton("Яндекс", "https://yandex.ru"))
    btn1 = types.InlineKeyboardButton("Skyeng", "https://student.skyeng.ru/home")
    btn2 = types.InlineKeyboardButton("Google", "https://www.google.ru/")
    btn3 = types.InlineKeyboardButton("Яндекс", "https://yandex.ru")
    markup.row(btn1)
    markup.row(btn3, btn2)
    bot.send_message(incoming_message.chat.id, "Вот такие сайты у нас есть:", reply_markup=markup)



@bot.message_handler(commands=["picture"])
def get_picture(incoming_message):
    list_names_pictures = os.listdir("Pictures")
    print(list_names_pictures)
    with open(f"Pictures/{random.choice(list_names_pictures)}", "rb") as pic:
        bot.send_photo(incoming_message.chat.id, pic)



















@bot.message_handler()
def answer(incoming_message):
    if incoming_message.text.lower() == "привет":
        bot.send_message(incoming_message.chat.id, f"Привет, {incoming_message.from_user.first_name}")
    elif incoming_message.text.lower() == "id":
        bot.reply_to(incoming_message, f"Ваш id: {incoming_message.from_user.id}")
    elif incoming_message.text == "Все команды":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Регистрация", callback_data="reg"))
        commands = """
        Доступные команды:
        /start - начать работу с ботом
        /help- получить помощь
        /site - открыть сайт
        /sites - показать список сайтов
        /picture - получить случайную картинку
         """
        bot.send_message(incoming_message.chat.id, commands, reply_markup=markup)
    else:
        bot.reply_to(incoming_message, "Ваше сообщение не разпознано!")



bot.infinity_polling() # Запускаем бота и указываем, чтобы он постоянно проверял наличие новых сообщений

