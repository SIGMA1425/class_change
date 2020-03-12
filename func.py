import datetime
import json
from tqdm import tqdm

week = ["月", "火", "水", "木", "金", "土", "日"]
exam = ["pre_first_exam", "pre_second_exam", "lat_first_exam", "lat_second_exam"]
exam_name = ["前期中間", "前期定期", "後期中間", "後期定期"]

def get_date():
    now = datetime.datetime.now()
    now -= datetime.timedelta(days=40)
    date = str(now.month) + "月" + str(now.day) + "日"
    date += "(" + week[now.weekday()] + ")"
    return date

def shape(origin):
    origin = origin.split("　")
    dest = origin[1] + "\n" + origin[3] + origin[5] + "\n"
    return dest

def test_count():
    with open("./data.json") as fp:
        data = json.load(fp)
    for i in range(4):
        exam[i] = data[exam[i]]
    for i in tqdm(range(4)):
        test_date = datetime.datetime.strptime(exam[i], "%Y年%m月%d日")
        test_date = datetime.date(year=test_date.year, month=test_date.month, day=test_date.day)
        now = datetime.date.today()
        
        if 0 < (test_date - now).days <= 14:
            return {"exam_name": exam_name[i], "days_left": (test_date - now).days}
    
    return
