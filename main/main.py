import requests
from datetime import datetime
from enum import Enum
import calendar
import json


class TimeFlag(Enum):
    DAILY = 0
    MONTHLY = 1


def month_delta(date, delta):
    m, y = (date.month+delta) % 12, date.year + (date.month + delta - 1) // 12
    if not m:
        m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d, month=m, year=y)


def get_momentum(lookback_period, time_flag):
    request_url = 'http://127.0.0.1:8000/price'
    if time_flag == TimeFlag.MONTHLY:
        request_url += '/monthly/'
    elif time_flag == TimeFlag.DAILY:
        request_url += '/daily/'
    else:
        raise BaseException

    fetch_data = requests.get(request_url+'?lb='+str(lookback_period)).content
    json_format = fetch_data.decode('utf8').replace("'", '"')
    data = json.loads(json_format)

    momentum = {}
    sma = {}
    lastest_data = data[0]

    data_size = len(data)
    denominator = 0
    for i in range(0, data_size+1):
        denominator += i

    # SMA 계산
    item_cnt = 0
    for item in data:
        # 필요없는 데이터 삭제
        item.pop('id')
        item.pop('price_date')

        for code in item:
            if code not in sma:
                sma[code] = 0
            if item[code] != 0:
                # 지정 범위 내 데이터가 존재할 경우
                sma[code] = (item[code]*(data_size-item_cnt))/denominator + sma[code]
                momentum[code] = 0
            else:
                # 지정 범위 내 데이터가 없을 경우
                momentum[code] = 'NED'
        item_cnt += 1

    # MOM 계산
    for code in lastest_data:
        if momentum[code] != 'NED':
            momentum[code] = (lastest_data[code]/sma[code])-1

    return momentum


mom = get_momentum(12, TimeFlag.MONTHLY)
print(mom)

