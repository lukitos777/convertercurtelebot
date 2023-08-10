import telebot
from currency_converter import CurrencyConverter
from telebot import types
import time


bot = telebot.TeleBot('6464556302:AAEeXJwMUEstHOdgV0uR1XIMLGIQkV0UPuA')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi!')
    time.sleep(0.2)
    bot.send_message(message.chat.id, 'Enter the amount')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount

    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid value ⚠️')
        time.sleep(0.2)
        bot.send_message(message.chat.id, 'Try again')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)

        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        bnt4 = types.InlineKeyboardButton('other', callback_data='else')

        markup.add(btn1, btn2, btn3, bnt4)

        bot.send_message(message.chat.id, 'choose pair of currency', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Amount should be larger than 0 ⚠️')
        time.sleep(0.2)
        bot.send_message(message.chat.id, 'Try again')
        bot.register_next_step_handler(message, summa)
        return


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        res_string = f'{amount} {values[0]} => {round(res, 2)} {values[1]}'

        bot.send_message(call.message.chat.id, res_string)
        time.sleep(0.2)
        bot.send_message(call.message.chat.id, 'Enter new amount')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Enter pair of currency')
        bot.send_message(call.message.chat.id, 'Example: CUR1/CUR2')

        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        res_string = f'{amount} {values[0]} => {round(res, 2)} {values[1]}'

        bot.send_message(message.chat.id, res_string)
        time.sleep(0.2)
        bot.send_message(message.chat.id, 'Enter new amount')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Invalid input ⚠️')
        time.sleep(0.2)
        bot.send_message(message.chat.id, 'Try again')
        bot.register_next_step_handler(message, summa)


bot.polling(none_stop=True)