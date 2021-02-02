import os
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import numpy as np
from Telegram.sendmessage import SendMessage
from Telegram.sendmarkdown import SendMarkdown

cryptos = pd.read_csv("data/cryptos.csv")

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

#print(cryptos.dtypes)

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  api_result = json.loads(response.text)
  #print(data)


except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

def trade_action(latest_trade_price, current_price):
  if current_price <= latest_trade_price / 1.095:
    return "Buy"
  elif current_price >= latest_trade_price * 1.095:
    return "Sell"
  else:
    return "Hodl" 


for ix, coinmarketcap_id in cryptos.coinmarketcap_id.iteritems():
  cryptos.loc[ix, "current_price"] = round(api_result["data"][str(coinmarketcap_id)]["quote"]["EUR"]["price"],2)
  cryptos.loc[ix, "action"] = trade_action(cryptos.loc[ix, "latest_trade_price"], cryptos.loc[ix, "current_price"])
  if cryptos.loc[ix, "action"] != "Hodl":
    current_price = str(cryptos.loc[ix, 'current_price']).replace('.',',')
    text = f"*Alert {cryptos.loc[ix, 'action']}* `{cryptos.loc[ix, 'name']}` _@ {current_price}€_ per *{cryptos.loc[ix, 'symbol']}*"
    SendMarkdown(chat_id='509161525', text=text, token=os.environ.get('TELEGRAM_API_TOKEN'))
    cryptos.loc[ix, "latest_trade_price"] = cryptos.loc[ix, "current_price"]

cryptos.to_csv("data/cryptos.csv", index=False)