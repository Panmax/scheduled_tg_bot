import time
import os

import telegram
import json
import requests

from datetime import datetime

# TOKEN = "993312022:AAEItLb3ksINtmISJyrlOf9gUQDskLuo4C8"
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = -1001156324531


_cache = {}


def forward_message(event, context):
    bot = telegram.Bot(token=os.environ['TELEGRAM_BAYMAX_TOKEN'])
    body = json.loads(event['body'])

    print('## ENVIRONMENT VARIABLES')
    print(os.environ)
    print('## EVENT')
    print(event)
    print('## myid')
    myid = body['message']['from']['id']
    print("%s is me: %s", myid, myid == 427665003)

    key = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
    key += str(myid)
    counter = _cache.get(key, 0)
    counter += 1
    _cache[key] = counter

    print('## cache')
    print(_cache)

    text = ''
    bark_message = ''
    if counter == 1:
        text = '已召唤 Panmax'
        bark_message = 'NewTgMessage'
    elif counter == 3:
        text = '三连发，紧急召唤 Panmax'
        bark_message = 'NewTgMessage x 3'
    elif counter == 7:
        text = '七连发，十万火急，Panmax 马上到'
        bark_message = 'NewTgMessage x 7'

    if text and body['message'].get('text') and body['message']['from']['id'] != 427665003:
        requests.get('https://api.day.app/RTb5xKEuMS5bKX5HpBUiha/' + bark_message)
        bot.sendMessage(chat_id=body['message']['chat']['id'], text=text)
    return {
        "statusCode": 200,
    }


def send_message(event, context):
    bot = telegram.Bot(token=TOKEN)
    bot.sendMessage(chat_id=CHAT_ID, text='Hello World!')
    return {
        "statusCode": 200,
    }


def send_custom_message(event, context):
    bot = telegram.Bot(token=os.environ['TELEGRAM_BOSSKU_TOKEN'])
    bot.sendMessage(chat_id=-423948345, text=event['body'])
    return {
        "statusCode": 200,
        "body": json.dumps(event)
    }


def print_now(event, contxt):
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')
            }
        )
    }


def handle_command(event, context):
    bot = telegram.Bot(token=os.environ['TELEGRAM_BOSSKU_TOKEN'])
    body = json.loads(event['body'])
    if body['message'].get('text'):
        r = requests.get('https://bossku.cn/api/actuator/reg_statistic').json()
        if body['message']['text'].startswith('/reg_today'):
            bot.sendMessage(chat_id=body['message']['chat']['id'], text='回报主子，今日注册用户数：%s' % (r['data']['today'],))
        elif body['message']['text'].startswith('/reg_total'):
            bot.sendMessage(chat_id=body['message']['chat']['id'], text='回报主子，注册用户数总数：%s' % (r['data']['total'],))
    return {
        "statusCode": 200,
    }
