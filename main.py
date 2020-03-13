import json
import requests
from bs4 import BeautifulSoup
import slackweb
import datetime
import func
import quickstart as qk

TODAY = 0
TOMORROW = 1

path = "./data.json"

# jsonファイルにwebhookURLやらテストの日やら全部入っている
with open(path) as fp:
    data = json.load(fp)

slack = slackweb.Slack(url=data["test_slack"])

response = requests.get(data["TNCT_URL"])
bs = BeautifulSoup(response.content, "html.parser")

if datetime.datetime.now().hour < 12:
    today_or_tomorrow = TODAY  
else:
    today_or_tomorrow = TOMORROW

holiday_flag = func.holiday_check(bs, today_or_tomorrow)
output = ""

if holiday_flag is False:
    print("授業変更情報を取得します")
    output += func.get_class_change(bs, today_or_tomorrow)

print("テストまでの日数を検索します．")
output += func.test_count(path)

print("行事予定を取得します")
output += qk.get_event(today_or_tomorrow)

slack.notify(text=output)
print("slackへのメッセージの送信が正常に行われました．")

