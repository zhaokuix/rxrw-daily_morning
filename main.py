from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']),math.floor(weather['low']),math.floor(weather['high'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  
  words = words.json()['data']['text']
  if len(words) > 120:
    return get_words()
  words1 = words
  words2 = ''
  words3 = ''
  words4 = ''
  words5 = ''
  words6 = ''
  if len(words) > 20:
        words1 = words[:20]
        words2 = words[20:]
        if len(words2) > 20:
          words3 = words2[:20]
          words4 = words2[20:]
          if len(words4) > 20:
            words5 = words4[:20]
            words6 = words4[20:]

  return words1,words2,words3,words4,words5,words6

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature,lowTemp,highTemp = get_weather()
words1,words2,words3,words4,words5,words6 = get_words();
data = {"weather":{"value":wea},"city":{"value":city},"temperature":{"value":temperature},"lowest":{"value":lowTemp},
        "highest":{"value":highTemp},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},
        "words1":{"value":words1},"words2":{"value":words2},"words3":{"value":words3},"words4":{"value":words4},
        "words5":{"value":words5},"words6":{"value":words6}
        }
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data)
  print(res)
