import os
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import numpy as np

url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=1&symbol=BTC&convert=EUR'
parameters = {
  'amount':'1',
  'limit':'5000',
  'convert':'EUR'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': os.environ.get('COINMARKETCAP_TOKEN'),
}

cryptos = pd.DataFrame(np.array([
    [1, "Bitcoin", "BTC", 27127.62],
    [1, "Ethereum", "ETH", 27127.62], 
    [1, "Uniswap", "UNI", 27127.62],
    [1, "Monero", "XMR", 27127.62],
    [1, "Aave", "AAVE", 27127.62]
  ]), columns=["coinmarketcap_id", "name", "symbol", "latest_trade_price"])


print(cryptos)

# session = Session()
# session.headers.update(headers)

# try:
#   response = session.get(url, params=parameters)
#   data = json.loads(response.text)
#   print(data)
# except (ConnectionError, Timeout, TooManyRedirects) as e:
#   print(e)