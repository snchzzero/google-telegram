from config import telegram_token
from script import db_google_sheets
import telebot
import time
from multiprocessing import *
import schedule

global flag
flag =False
bot =telebot.TeleBot(telegram_token)

def start_process(msg):  # Запуск Process
    global USER_ID
    USER_ID = msg.chat.id
    global p1
    p1 = Process(target=start_schedule(USER_ID), args=()).start()

def start_schedule(USER_ID):
    if flag == False:
        l1 = db_google_sheets("Telegram")
        message_string = "Cрок поставки прошел по следующим позициям: (сортировка по дате) \n"
        for l in l1:
            message_string += f"№{l[0]}, Заказ №{l[1]}, Срок: {l[2]} \n"
        bot.send_message(USER_ID, message_string)
    schedule.every(3600).seconds.do(send_message1)  #3600
    #schedule.every().day.at("11:02").do(send_message1)
    while True:  # Запуск цикла
        schedule.run_pending()
        time.sleep(1)

def send_message1():
    flag = True
    l1 = db_google_sheets("Telegram")
    message_string = "Cрок поставки прошел по следующим позициям: (сортировка по дате) \n"
    for l in l1:
        message_string += f"№{l[0]}, Заказ №{l[1]}, Срок: {l[2]} \n"
    bot.send_message(USER_ID, message_string)

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, f'Уведомления по срокам поставки - \n'
                                            f'Включено (раз в час) \n'
                                            f'для отмены введите "/stop"')
    bot.register_next_step_handler(msg, start_process(msg))

@bot.message_handler(commands=['stop'])
def start(message):
    msg = bot.send_message(message.chat.id, f'Расылка уведомлений выключена')
    p1.join()


bot.polling(none_stop=True)