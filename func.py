import datetime
import json
from tqdm import tqdm

week = ["月", "火", "水", "木", "金", "土", "日"]
exam = ["pre_first_exam", "pre_second_exam", "lat_first_exam", "lat_second_exam"]
exam_name = ["前期中間", "前期定期", "後期中間", "後期定期"]

def get_date():
    now = datetime.datetime.now()
    now -= datetime.timedelta(days=38)
    date = str(now.month) + "月" + str(now.day) + "日"
    date += "(" + week[now.weekday()] + ")"
    return date

def shape(origin):
    if "→" in origin:
        origin = origin.split("　")
        dest = origin[1] + "\n" + origin[3] + origin[5] + "\n"
    else:
        dest = origin
    return dest

def test_count(path):
    with open(path) as fp:
        data = json.load(fp)
    for i in range(4):
        exam[i] = data[exam[i]]
    for i in range(4):
        test_date = datetime.datetime.strptime(exam[i], "%Y年%m月%d日")
        test_date = datetime.date(year=test_date.year, month=test_date.month, day=test_date.day)
        now = datetime.date.today()
        
        if 0 < (test_date - now).days <= 14:
            return {"exam_name": exam_name[i], "days_left": (test_date - now).days}
    
    return None

def get_class_change(bs):
    output = get_date() + "\n"
    not_change = "現在のところ\n休講・変更の予定はありません．"
    
    for p in bs.select("p"):
        if "現在のところ休講・変更の予定はありません" in p.text:
            print("授業変更情報は見つかりませんでした．")
            output += not_change
            return output

    print("授業変更情報の存在を確認．探索します．")
    select_td = bs.select("td")

    index = 0
    for td in select_td:
        if "科　目　名" in td.text:
            break
        else:
            index += 1

    console_output = ""
    flag = False
    for i, td in enumerate(tqdm(select_td[index:])):
        if get_date() in td.text:
            if flag is False:
                output += "<!channel>" + "\n"
                flag = True
            output += select_td[i+index].text.replace(get_date(), "") + "\n"
            output += shape(select_td[i+index+1].text)
            console_output += select_td[i+index+1].text + "\n"

    print(console_output, end="")
    if flag is False:
        output += not_change
        print("授業変更情報は見つかりませんでした．")
    
    return output
