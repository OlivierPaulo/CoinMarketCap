import os
import requests


## Get Telegram API Token
token = os.environ.get('TELEGRAM_API_TOKEN')

### Function to sendMessage to Telegram
def SendMessage(chat_id='509161525', text='Hello', token=token):
    params = {
        'api_url':"https://api.telegram.org",
        'action':"sendMessage",
        'token': token,
        'chat_id':chat_id,
        'text':text
    }
    req = requests.get(f"{params['api_url']}/bot{params['token']}/{params['action']}?chat_id={params['chat_id']}&text={params['text']}")
    return req.json()

if __name__ == '__main__':
    
    print(SendMessage(text="This is \U0001F3C0", token=token)) ## \U0001F3C0 unicode value for Basketball ball