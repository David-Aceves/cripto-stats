from binance.client import Client
from config import api_key, api_secret

client = Client(api_key, api_secret)
print(client)
print('logged in')