from binance.client import Client

def setup_binance(api_key, api_secret):
    # Cliente y contras binance
    client = Client(api_key, api_secret)
    print(client)
    print('logged in')
    return client
