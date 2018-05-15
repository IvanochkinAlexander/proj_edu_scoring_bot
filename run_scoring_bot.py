# -*- coding: utf-8 -*-

import time
import catboost
import telebot
from telebot import types
import pickle
import pandas as pd

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)
clf = catboost.CatBoostClassifier()
model = clf.load_model('model')

@bot.message_handler(commands=['help', 'start'])

def send_welcome(message):

    """Initial message"""

    try:
        msg = bot.reply_to(message, """\
    Привет, я рассчитаю для тебя вероятности страхового случая
    """)

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Расчитать скоринг', 'Показать методологию')
        msg = bot.reply_to(message, 'Выберите действие', reply_markup=markup)
        bot.register_next_step_handler(msg, process_variant_step)
        time.sleep(2)
    except:
        bot.send_message(message.chat.id, 'ошибка попробуйте еще раз /start')
        time.sleep(5)


def process_variant_step(message):

    """Second answer"""

    try:
        global variant
        variant = message.text
        if (variant == 'Расчитать скоринг') or (variant == 'Показать методологию'):
            choice = variant
        else:
            raise Exception()
        if choice == 'Расчитать скоринг':
            msg = bot.reply_to(message, 'Введите скоринговые данные: 10 целых чисел через пробел')
            bot.register_next_step_handler(msg, process_name_step)
            time.sleep(2)
        elif choice =='Показать методологию':
            bot.send_message(message.chat.id, 'Методология:скоринг считается моделью catboost на основе 10 переменных - информация о водителе и его семье')
            time.sleep(2)
            bot.send_message(message.chat.id, 'Для повторного выбора нажмите /start')
            time.sleep(2)
    except:
        bot.send_message(message.chat.id, 'ошибка попробуйте еще раз /start')
        time.sleep(2)


def process_name_step(message):

    """Second answer. Catboost scoring"""
    
    try:
        global result
        result = []
        for i in message.text.split(' '):
            result.append(i)
        result_model = model.predict_proba(pd.DataFrame(result).T)[0][0]
        bot.send_message(message.chat.id, 'Вероятность наступления страхового случая составляет : {} процентов'.format(round(result_model, 3)))
        time.sleep(2)
        bot.send_message(message.chat.id, 'Для повторного выбора нажмите /start')
        time.sleep(5)
    except:
        bot.send_message(message.chat.id, 'ошибка попробуйте еще раз /start')
        time.sleep(5)

while True:

    try:

        bot.polling(none_stop=True)


    except Exception as e:

        logger.error(e)

        time.sleep(15)
