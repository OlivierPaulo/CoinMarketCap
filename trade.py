import os
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import numpy as np


cryptos = pd.DataFrame(np.array([
    [1, "Bitcoin", "BTC", 27127.62],
    [1207, "Ethereum", "ETH", 1200], 
    [7083, "Uniswap", "UNI", 15.14],
    [328, "Monero", "XMR", 85],
    [7278, "Aave", "AAVE", 250]
  ]), columns=["coinmarketcap_id", "name", "symbol", "latest_trade_price"])
cryptos["coinmarketcap_id"] = cryptos["coinmarketcap_id"].astype("int64")
cryptos["latest_trade_price"] = cryptos["latest_trade_price"].astype("float64")

url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
parameters = {
  'id': ",".join(map(str,[coinmarketcap_id for coinmarketcap_id in cryptos.coinmarketcap_id])),  ## Retrieve the ID of each crypto to pass them as argument in the API call
  'convert':'EUR'
}
headers = {
  'Accepts': 'application/json',
  'Accept-Encoding': 'deflate, gzip',
  'X-CMC_PRO_API_KEY': os.environ.get('COINMARKETCAP_TOKEN'),
}

print(cryptos.dtypes)

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  api_result = json.loads(response.text)
  #print(data)
  for coinmarketcap_id in cryptos.coinmarketcap_id:
    cryptos["current_price"] = round(api_result["data"][str(coinmarketcap_id)]["quote"]["EUR"]["price"],2)

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

def trade_action(latest_price, current_price):
  if current_price == latest_price / 1.1:
    return "Buy"
  elif current_price == latest_price * 1.1:
    return "Sell"
  else:
    return "Hold" 

cryptos["action"] = cryptos.apply(lambda x: trade_action(cryptos["latest_trade_price"], cryptos["current_price"]), axis=1)

print(cryptos)