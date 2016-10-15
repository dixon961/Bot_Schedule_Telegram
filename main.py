import telebot
import parse
from telebot import types
from time import sleep
import baseutil

f = open('../bot_token.txt')

token = f.read()
bot = telebot.TeleBot(token)
is_group_set = True

keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button_today = types.KeyboardButton(text='Сегодня')
button_tomorrow = types.KeyboardButton(text='Завтра')
button_week = types.KeyboardButton(text='Неделя')
button_change = types.KeyboardButton(text='Сменить группу')
button_date = types.KeyboardButton(text='Расписание по дате')
keyboard.add(button_today, button_tomorrow, button_week, button_change, button_date)

while (True):
    @bot.message_handler(commands=['help', 'start'])
    def send_welcome(message):
        baseutil.add_user(message.chat.id, 'МП-10')
        bot.send_message(message.chat.id, 'Привет! Я Бот с расписанием! Введите свою группу(прим. МП-10)')


    @bot.message_handler(content_types=['text'])
    def handle_text(message, is_group_set=is_group_set):
        if message.text == 'Неделя' and is_group_set:
            parse.parse_all_schedule(baseutil.get_group_by_user(message.chat.id))
            bot.send_message(message.chat.id, parse.parse_week() + '.')
        elif message.text == 'Сегодня' and is_group_set:
            parse.parse_all_schedule(baseutil.get_group_by_user(message.chat.id))
            bot.send_message(message.chat.id, parse.parse_today() + '.')
        elif message.text == 'Завтра' and is_group_set:
            parse.parse_all_schedule(baseutil.get_group_by_user(message.chat.id))
            bot.send_message(message.chat.id, parse.parse_tomorrow() + '.')
        elif message.text == 'Сменить группу':
            bot.send_message(message.chat.id, 'Введите новую группу')
            parse.clean_schedule()
        elif message.text == 'Расписание по дате':
            bot.send_message(message.chat.id, 'Пока что не работает :з')
            pass
        else:
            bot.send_message(message.chat.id, 'Вы выбрали группу ' + message.text + '.\nВыберите расписание:',
                             reply_markup=keyboard)
            baseutil.change_group(message.chat.id, message.text)
            parse.parse_all_schedule(baseutil.get_group_by_user(message.chat.id))


    try:
        bot.polling(none_stop=True)
    except Exception:
        pass
