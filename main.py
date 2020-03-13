import json
import requests
from bs4 import BeautifulSoup
import slackweb
import func

# jsonファイルにwebhookURLやらテストの日やら全部入っている
with open("./data.json") as fp:
    data = json.load(fp)

slack = slackweb.Slack(url=data["test_slack"])

response = requests.get(data["TNCT_URL"])
bs = BeautifulSoup(response.content, "html.parser")

print("授業変更情報を取得します")
output = func.get_class_change(bs)

print("テストまでの日数を検索します．")
test_count = func.test_count()

if test_count is not None:
    print(test_count["exam_name"] + "がヒットしました．")
    print(test_count["exam_name"] + "テストまであと" + str(test_count["days_left"]) + "日です．")
    output += "\n" + test_count["exam_name"] + "テストまであと" + str(test_count["days_left"]) + "日です．"

else:
    print("該当するテストは見つかりませんでした")

slack.notify(text=output)

