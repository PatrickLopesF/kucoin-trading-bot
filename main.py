from kucoin.client import Client
import config
import json
import time

client = Client(config.api_key, config.api_secret, config.api_passphrase)
btc_usdt = client.get_ticker('BTC-USDT')
action_price = float(btc_usdt['price'])

while True:
    time.sleep(600)
    btc_usdt = client.get_ticker('BTC-USDT')
    price = float(btc_usdt['price'])
    amount = '%f' % (1/action_price)
    if price/action_price <= 0.9975:
        order = client.create_market_order('BTC-USDT', Client.SIDE_BUY, size=amount*10)
        action_price = price
        total = 1
        while total == 1:
            time.sleep(30)
            btc_usdt = client.get_ticker('BTC-USDT')
            price = float(btc_usdt['price'])
            if price/action_price >= 1.005 and total == 1:
                order = client.create_market_order('BTC-USDT', Client.SIDE_SELL, size=amount*10)
                action_price = price
                total = 0
            if price/action_price <= 0.997 and total == 1:
                order = client.create_market_order('BTC-USDT', Client.SIDE_SELL, size=amount*10)
                action_price = price
                total = 0
    else:
        action_price = price

