import telebot
from telebot import types

from config import keys, TOKEN
from utils import 	ConvertionExeption, CryptoConverter

def create_markup(quone = None):
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	buttons = []
	for val in keys.keys():
		buttons.append(types.KeyboardButton(val.capitalize()))

	markup.add(*buttons)
	return markup


bot = telebot.TeleBot(TOKEN)

# Смс пользователю инструкции
@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):
	text = 'Что бы начать работу введите комманду боту в следующем формате:\n<имя валюты>\
<в какую валюту перевести>\
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values\
\nНачать общение с ботом: /convert'
	bot.reply_to(message, text)

# Смс пользователю о доступных валютах
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
	text = 'Доступные валюты:'
	for key in keys.keys():
		text = '\n'.join((text, key, ))
	bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
	text = 'Выберите валюту, из которой конвертировать:'
	bot.send_message(message.chat.id, text, reply_markup = create_markup())
	bot.register_next_step_handler(message, quote_handler)

def quote_handler(message: telebot.types.Message):
	quote = message.text.strip().lower()
	text = 'Выберите валюту, в которую конвертировать:'
	bot.send_message(message.chat.id, text, reply_markup = create_markup(quote))
	bot.register_next_step_handler(message, base_handler, quote)

def base_handler(message: telebot.types.Message, quote):
	base = message.text.strip()
	text = 'Выберите количество конвертируемой валюты:'
	bot.send_message(message.chat.id, text,)
	bot.register_next_step_handler(message, amount_handler, quote, base)

def amount_handler(message: telebot.types.Message, quote, base):
	amount = message.text.strip()
	try:
		total_base = CryptoConverter.convert(quote.lower(), base.lower(), amount)
	except ConvertionExeption as e:
		bot.send_message(message.chat.id, f'Ошибка конвертации: \n{e}')
	else:
		text = f'Цена {amount} {quote} в {base} : {total_base}'
		bot.send_message(message.chat.id, text)


bot.polling()