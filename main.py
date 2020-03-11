import json
import requests
from bs4 import BeautifulSoup
import slackweb
import func

with open("./data.json") as fp:
    data = json.load(fp)

slack = slackweb.Slack(url=data["test_slack"])

response = requests.get(data["TNCT_URL"])
bs = BeautifulSoup(response.content, "html.parser")

output = func.get_date() + "\n"
not_change = "現在のところ\n休講・変更の予定はありません"

print("授業変更情報を取得中")
for p in bs.select("p"):
    if "現在のところ休講・変更の予定はありません" in p.text:
        print("授業変更情報は見つかりませんでした")
        output += not_change
        slack.notify(text=output)
        exit()

print("授業変更情報の存在を確認．探索します")
select_td = bs.select("td")

index = 0
for td in select_td:
    if "科　目　名" in td.text:
        break
    else:
        index += 1

flag = False
for i, td in enumerate(select_td[index:]):
    if func.get_date() in td.text:
        if flag is False:
            output += "<!channel>" + "\n"
            flag = True
        output += select_td[i+index].text.replace(func.get_date(), "") + "\n"
        print(select_td[i+index+1].text)
        output += func.shape(select_td[i+index+1].text)

if flag is False:
    output += not_change
    print("授業変更情報は見つかりませんでした")

slack.notify(text=output)


