import datetime

week = ["月", "火", "水", "木", "金", "土", "日"]

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

