import requests
import time
import enum
from tqdm import tqdm
from pytz import timezone

base_url = "https://www.alphavantage.co/query?"
api_key = "YWK61NRAYQA1IKQ0"
call_interval = 15
eastern = timezone('US/Eastern')


class TimeFlag(enum.Enum):
    DAILY = 0
    MONTHLY = 1


def make_alphavantage_request_url(function_name, symbol):
    request_url = base_url
    request_url += "function=" + function_name
    request_url += "&symbol=" + symbol
    request_url += "&apikey=" + api_key

    return request_url


def request_to_alphavantage(url):
    response = requests.get(url)
    data = response.json()
    return data


def get_monthly_adj_price_by_ticker(ticker):
    result = {}
    global base_data

    try:
        content_key = "Monthly Adjusted Time Series"
        base_data = request_to_alphavantage(make_alphavantage_request_url('TIME_SERIES_MONTHLY_ADJUSTED', ticker))
        monthly_data = base_data[content_key]
        for date in monthly_data:
            result[date] = monthly_data[date]['5. adjusted close']
        first_key = list(result.keys())[0]
        result.pop(first_key)
    except Exception:
        print("{} {}".format(ticker, base_data))

    # for alphavantage policy
    # time.sleep(call_interval)
    wait_for_call(call_interval)
    return result


def get_daily_adj_price_daily(ticker):
    result = {}
    global base_data

    try:
        content_key = "Time Series (Daily)"
        base_data = request_to_alphavantage(make_alphavantage_request_url('TIME_SERIES_DAILY_ADJUSTED', ticker))
        daily_data = base_data[content_key]
        # refresh_date = base_data["Meta Data"]["3. Last Refreshed"]
        # refresh_date = eastern.localize(datetime.strptime(base_data["Meta Data"]["3. Last Refreshed"], "%Y-%m-%d"))
        for date in daily_data:
            result[date] = daily_data[date]['5. adjusted close']
        first_key = list(result.keys())[0]
        result.pop(first_key)
    except Exception:
        print("{} {}".format(ticker, base_data))

    # for alphavantage policy
    # time.sleep(call_interval)
    wait_for_call(call_interval)
    return result


def wait_for_call(interval):
    for _ in tqdm(range(0, interval)):
        time.sleep(1)



