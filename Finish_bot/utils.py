import requests
import json
from config import keys

# Отлавливание ошибок
class ConvertionExeption(Exception):
	pass

# Конвертация валюты
class CryptoConverter:
	@staticmethod
	def convert(quote: str, base: str, amount: str):

	# отлов ошибки одинаковой валюты
		if quote == base:
			raise ConvertionExeption(f'Невозможно перевести одинаковые валюты {base}')

	# проверка есть ли валюта в списке доступных

		try:
			quote_ticker = keys[quote]
		except KeyError:
			raise ConvertionExeption(f'Не удалось обработать валюту {quote}')

		try:
			base_ticker = keys[base]
		except KeyError:
			raise ConvertionExeption(f'Не удалось обработать валюту {base}')

	# проверка корректного числа валюты
		try:
			amount = float(amount)
		except ValueError:
			raise ConvertionExeption(f"Не удалось обработать количество {amount}")

		r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
		total_base = json.loads(r.content)[keys[base]]

		return total_base * float(amount)