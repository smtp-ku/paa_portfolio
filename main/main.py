import requests
from datetime import datetime
from enum import Enum
import calendar


class TimeFlag(Enum):
    DAILY = 0
    MONTHLY = 1


def month_delta(date, delta):
    m, y = (date.month+delta) % 12, date.year + (date.month + delta - 1) // 12
    if not m:
        m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d, month=m, year=y)


def calc_sma(lookback_period, time_flag):
    fetch_data = requests.get('http://127.0.0.1:8000/price/monthly/?lb='+str(lookback_period)).content
    print(fetch_data)


calc_sma(3, TimeFlag.MONTHLY)

