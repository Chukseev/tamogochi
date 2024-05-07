import telebot
from telebot import types
import time
import threading
import schedule
import yaml
from working_in_the_db import (insert_user, insert_pet, insert_inventory, cheking_pet, select_pet,
                               feed_pet, cheking_user, select_inventory, select_balance, update_satiety_and_mood)
import working_in_the_minio as h

with open('config1.yaml', 'r') as file:
    config = yaml.safe_load(file)

telegram = config['telegram']

bot = telebot.TeleBot(telegram['token'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if cheking_user(message.from_user.id):
        bot.send_message(message.chat.id, 'Вы уже авторизованы')
    else:
        insert_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                    message.from_user.username)
        bot.reply_to(message, f"Привет,{message.from_user.first_name}")
        bot.send_message(message.chat.id, '/create_pet - Создать питомца')


@bot.message_handler(commands=['create_pet'])
def creating_pet(message):
    if cheking_user(message.from_user.id):

        if cheking_pet(message.from_user.id):
            bot.send_message(message.chat.id, 'У вас уже есть питомец')

        else:
            bot.send_message(message.chat.id, 'Напиши имя своего животного')
            bot.register_next_step_handler(message, pet_name)
    else:
        bot.send_message(message.chat.id, 'Авторизируйтесь с помощью команды: \n/start')


def pet_name(message):
    if message.text[0] in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '[', ']',
                           '{', '}', '|', '\\'[0], ';', ':', "'", '"', ',', '.', '<', '>', '/', '?', '`',
                           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        bot.reply_to(message, 'Некорректное имя')
        bot.send_message(message.chat.id, 'Напиши имя своего животного')
        bot.register_next_step_handler(message, pet_name)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🐈‍⬛')
        btn2 = types.KeyboardButton('🦮')
        markup.add(btn1, btn2)

        bot.send_message(message.chat.id, 'Кем будет твой питомец?', reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: finally_reg(msg, message.text))


def finally_reg(message, name):
    markup = types.ReplyKeyboardRemove()
    pet_type = 'cat' if message.text == '🐈‍⬛' else 'dog' if message.text == '🦮' else None
    if pet_type is None:
        bot.reply_to(message, 'Такого животного нет,пока что 🐈‍⬛, 🦮', reply_markup=markup)
        bot.register_next_step_handler(message, finally_reg)
    else:
        insert_pet(message.from_user.id, name, pet_type)
        insert_inventory(message.from_user.id)
        bot.send_message(message.chat.id, 'Ваш питомец создан успешно', reply_markup=markup)


@bot.message_handler(commands=['view'])
def view_pet(message):
    if cheking_pet(message.from_user.id):
        pet = select_pet(message.from_user.id)
        name = pet[0]
        dog_or_cat = pet[1]
        satiety = pet[2]
        mood = pet[3]
        if mood + satiety >= 170:
            if dog_or_cat == 'dog':
                image = h.get_img('2.jpg')
            elif dog_or_cat == 'cat':
                image = h.get_img('10.jpg')
        elif mood + satiety >= 140:
            if dog_or_cat == 'dog':
                image = h.get_img('1.jpg')
            elif dog_or_cat == 'cat':
                image = h.get_img('9.jpg')

        elif mood + satiety >= 90:
            if dog_or_cat == 'dog':
                image = h.get_img('5.jpg')
            elif dog_or_cat == 'cat':
                image = h.get_img('13.jpg')

        elif mood + satiety >= 40:
            if dog_or_cat == 'dog':
                image = h.get_img('7.jpg')
            elif dog_or_cat == 'cat':
                image = h.get_img('15.jpg')

        elif mood + satiety >= 0:
            if dog_or_cat == 'dog':
                image = h.get_img('8.jpg')
            elif dog_or_cat == 'cat':
                image = h.get_img('16.jpg')

        bot.send_photo(message.chat.id, image, f'Имя: <b>{name}</b>\nСытость: <b>{satiety}</b>\nНастроение:<b>{mood}</b>',
                       parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'У вас нет питомца\nВоспользуйтесь /create_pet')


@bot.message_handler(commands=['inventory'])
def view_inventory(message):
    if cheking_user(message.from_user.id):
        bot.send_message(message.chat.id, f'<b>Инвентарь:</b>\n{select_inventory(message.from_user.id)}',
                         parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Авторизуйтесь с помощью /start')


@bot.message_handler(commands=['balance'])
def view_balance(message):
    bot.send_message(message.chat.id, f'<b>Ваш баланс: {select_balance(message.from_user.id)}р.</b>',
                     parse_mode='html')


@bot.message_handler(commands=['feed'])
def feed(message):
    if cheking_user(message.from_user.id):

        bot.send_message(message.chat.id, f'<b>Инвентарь:</b>\n{select_inventory(message.from_user.id)}',
                         parse_mode='html')

        bot.send_message(message.chat.id, 'Чем вы хотите кормить: ')
        bot.register_next_step_handler(message, next_step)
    else:
        bot.send_message(message.chat.id, 'Авторизуйтесь с помощью /start')


def next_step(message):
    for_user = feed_pet(message.text, message.from_user.id)
    bot.send_message(message.chat.id, for_user)


schedule.every(1).hours.do(update_satiety_and_mood)


def check_schedule():
    while True:
        schedule.run_pending()  # Проверяем расписание
        time.sleep(1)  # Ждем 1 секунду


# Функция для запуска бота и ожидания сообщений в отдельном потоке
def bot_polling():
    bot.infinity_polling()  # Ожидаем сообщений


# Запуск бота и проверки расписания в отдельных потоках
if __name__ == "__main__":
    schedule_thread = threading.Thread(target=check_schedule)
    bot_thread = threading.Thread(target=bot_polling)
    schedule_thread.start()
    bot_thread.start()
