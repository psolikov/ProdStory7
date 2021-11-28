import telebot

import requests
from enum import Enum
import os

# ON_HEROKU = os.environ.get('ON_HEROKU')



# from forex_python.converter import CurrencyRates

TOKEN = 'secret'
EXCHANGE_TOKEN = "secret2"

class Currency(Enum):
    EUR = 1
    USD = 2
    GBP = 3

# currency_rates = CurrencyRates()

bot = telebot.TeleBot(TOKEN)#, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, этот бот позволит узнать текущий курс € $ £.")

def retreive_currency(message):
    message = message.text.lower()
    if "курс" not in message.lower() or len(message.split()) > 5:
        return None
    has_eur = 0
    has_usd = 0
    has_gbp = 0
    if "евро" in message or \
        "€" in message:
        has_eur = 1
    if "доллар" in message or \
        "бакс" in message or \
        "$" in message:
        has_usd = 1
    if "фунт" in message or \
        "£" in message:
        has_gbp = 1
    if has_eur + has_gbp + has_usd != 1:
        return None
    if has_eur == 1:
        return Currency.EUR
    if has_usd == 1:
        return Currency.USD
    if has_gbp == 1:
        return Currency.GBP
    return None

def get_currency_rate(currency):
    RUB = "RUB"
    url = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_TOKEN}/latest/{currency.name}'
    response = requests.get(url)
    if not response:
        return None
    data = response.json()
    return data["conversion_rates"][RUB]

def currency_to_word(currency):
    if currency == Currency.EUR:
        return "Евро"
    elif currency == Currency.USD:
        return "Доллара"
    elif currency == Currency.GBP:
        return "Фунта"
    else:
        return None

def is_greating(message):
    tokens = ["здорова", "хеллоу", "как дела", "привет", "йоу", "хай", "здравствуйте", "здравствуй"]
    for token in tokens:
        if token in message.lower():
            return True
    return False

def is_bye(message):
    tokens = ["пока", "понял", "до свидания", "чао", "пока)", "завершить", "закончить", "стоп", "ок"]
    for token in tokens:
        if token in message.lower():
            return True
    return False

def generate_answer(message):
    if is_greating(message.text):
        return send_welcome(message)
    if is_bye(message.text):
        return "Пока!"
    currency = retreive_currency(message)
    if not currency:
        return "Прости, я тебя не понял."
    rate = get_currency_rate(currency)
    if not rate:
        return "Я сломался."
    answer = f"Текущий курс {currency_to_word(currency)}: {rate}."
    return answer

@bot.message_handler(content_types=['text'])#(func=lambda message: True)
def echo_all(message):
    chat_id = message.chat.id
    if not message or not message.text:
        return
    answer = generate_answer(message)
    bot.send_message(chat_id, answer)

if __name__ == '__main__':
    # bot.infinity_polling()
    bot.polling(none_stop=True)